from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def patch_once(path: Path, old: str, new: str, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    content = path.read_text(encoding="utf-8")
    count = content.count(old)
    if count != 1:
        raise RuntimeError(
            f"{label}: expected one exact match in {path}, found {count}. "
            "No safe automatic replacement was made for this operation."
        )
    path.write_text(content.replace(old, new, 1), encoding="utf-8")


def write_file(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


STATE_PROCESSOR = r'''from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from realtime.models import RealtimeEvent
from state.models import (
    PoolState,
    StateMeta,
    StateStatus,
    TokenState,
    WalletState,
)
from state.service import StateService


STATUS_MAP = {
    "observed": StateStatus.VERIFIED,
    "derived": StateStatus.DERIVED,
    "model_derived": StateStatus.DERIVED,
    "conflict": StateStatus.CONFLICT,
    "unresolved": StateStatus.UNRESOLVED,
    "unavailable": StateStatus.UNAVAILABLE,
    "error": StateStatus.CONFLICT,
    "unknown": StateStatus.UNAVAILABLE,
}


class StateProcessor:
    """Reduce canonical RealtimeEvent objects into Redis/PostgreSQL state.

    RealtimeEvent is the actual object emitted by RealtimeBus. Do not
    convert it to EventEnvelope: those are different schemas.
    """

    TOKEN_FIELDS = {
        "name", "symbol", "decimals", "price_usd", "market_cap_usd",
        "fdv_usd", "total_supply", "circulating_supply", "holders",
        "liquidity_usd", "volume_5m_usd", "volume_1h_usd", "volume_24h_usd",
        "buy_volume_5m_usd", "sell_volume_5m_usd", "transaction_count_5m",
        "launchpad_id", "launchpad_name", "launchpad_rail",
        "launchpad_attribution_status", "primary_pool_id", "pool_ids",
        "metadata_uri", "logo_uri", "creator_address", "mint_authority",
        "freeze_authority",
    }

    WALLET_FIELDS = {
        "native_balance", "token_count", "transaction_count",
        "total_volume_usd", "realized_pnl_usd", "unrealized_pnl_usd",
        "win_rate", "average_hold_seconds", "classification", "smart_money",
        "sniper", "insider", "fresh_wallet", "first_seen_at",
        "last_activity_at", "preferred_launchpads", "preferred_tokens",
    }

    POOL_FIELDS = {
        "base_reserve", "quote_reserve", "price_usd", "liquidity_usd",
        "volume_5m_usd", "volume_1h_usd", "volume_24h_usd",
        "buy_volume_5m_usd", "sell_volume_5m_usd", "fee_bps", "lp_supply",
        "created_at", "last_swap_at", "last_liquidity_change_at",
    }

    def __init__(self, state_service: StateService | None = None) -> None:
        self.state = state_service or StateService()

    @staticmethod
    def _meta(event: RealtimeEvent, version: int) -> StateMeta:
        return StateMeta(
            version=version,
            status=STATUS_MAP.get(event.status, StateStatus.UNAVAILABLE),
            source_id=event.source_id or event.source,
            observed_at=event.observed_at,
            processed_at=datetime.now(timezone.utc),
            last_event_id=event.event_id,
            parser=event.parser_name,
            parser_version=event.parser_version,
        )

    @staticmethod
    def _clean_payload(payload: dict[str, Any], allowed: set[str]) -> dict[str, Any]:
        return {
            key: value
            for key, value in payload.items()
            if key in allowed and value is not None
        }

    async def _process_token(self, event: RealtimeEvent) -> None:
        mint = event.entity_id
        payload = dict(event.payload)
        # Normalize common provider aliases before strict Pydantic validation.
        if "image_uri" in payload and "logo_uri" not in payload:
            payload["logo_uri"] = payload["image_uri"]
        if "launchpad_status" in payload and "launchpad_attribution_status" not in payload:
            payload["launchpad_attribution_status"] = str(payload["launchpad_status"]).upper()
        if "market_cap" in payload and "market_cap_usd" not in payload:
            payload["market_cap_usd"] = payload["market_cap"]

        patch = self._clean_payload(payload, self.TOKEN_FIELDS)
        current = await self.state.get_token(event.chain or "unknown", mint)
        version = current.meta.version + 1 if current else 1

        if current:
            data = current.model_dump()
            data.update(patch)
            data["meta"] = self._meta(event, version)
            updated = TokenState.model_validate(data)
        else:
            updated = TokenState(
                chain=event.chain or "unknown",
                mint=mint,
                **patch,
                meta=self._meta(event, version),
            )
        await self.state.save_token(updated)

    async def _process_wallet(self, event: RealtimeEvent) -> None:
        address = str(
            event.payload.get("wallet_address")
            or event.payload.get("address")
            or event.entity_id
        )
        patch = self._clean_payload(event.payload, self.WALLET_FIELDS)
        current = await self.state.get_wallet(event.chain or "unknown", address)
        version = current.meta.version + 1 if current else 1
        if current:
            data = current.model_dump()
            data.update(patch)
            data["meta"] = self._meta(event, version)
            updated = WalletState.model_validate(data)
        else:
            updated = WalletState(
                chain=event.chain or "unknown",
                address=address,
                **patch,
                meta=self._meta(event, version),
            )
        await self.state.save_wallet(updated)

    async def _process_pool(self, event: RealtimeEvent) -> None:
        payload = event.payload
        pool_id = str(payload.get("pool_address") or payload.get("pool_id") or event.entity_id)
        current = await self.state.get_pool(event.chain or "unknown", pool_id)

        # PoolState requires the pool's DEX and both token addresses.
        # Skip incomplete events rather than storing fabricated identifiers.
        dex_id = payload.get("dex_id") or (current.dex_id if current else None)
        base_token = payload.get("base_token") or payload.get("token0") or (current.base_token if current else None)
        quote_token = payload.get("quote_token") or payload.get("token1") or (current.quote_token if current else None)
        if not dex_id or not base_token or not quote_token:
            return

        patch = self._clean_payload(payload, self.POOL_FIELDS)
        version = current.meta.version + 1 if current else 1
        if current:
            data = current.model_dump()
            data.update(patch)
            data["meta"] = self._meta(event, version)
            updated = PoolState.model_validate(data)
        else:
            updated = PoolState(
                chain=event.chain or "unknown",
                pool_id=pool_id,
                dex_id=str(dex_id),
                base_token=str(base_token),
                quote_token=str(quote_token),
                **patch,
                meta=self._meta(event, version),
            )
        await self.state.save_pool(updated)

    async def process(self, event: RealtimeEvent) -> None:
        if not event.chain:
            return
        if event.event_type == "token.updated" and event.entity_type == "token":
            await self._process_token(event)
        elif event.event_type == "wallet.updated" and event.entity_type == "wallet":
            await self._process_wallet(event)
        elif event.event_type == "pool.updated" and event.entity_type == "pool":
            await self._process_pool(event)
'''

INTELLIGENCE_WORKER = r'''from __future__ import annotations

import logging
import os
from uuid import uuid4

from config.settings import get_settings
from intelligence.orchestrator import IntelligenceOrchestrator
from realtime.bus import get_realtime_bus
from realtime.publisher import publish_event
from realtime.state_processor import StateProcessor

logger = logging.getLogger("sentinel.intelligence.worker")


class IntelligenceWorker:
    """Single ordered consumer: update canonical state, then run intelligence."""

    GROUP = "sentinel-pipeline"

    def __init__(self) -> None:
        self.settings = get_settings()
        self.bus = get_realtime_bus()
        self.state_processor = StateProcessor()
        self.orchestrator = IntelligenceOrchestrator(
            state_service=self.state_processor.state
        )
        self.consumer_name = (
            f"{os.getenv('HOSTNAME', 'sentinel')}-{os.getpid()}-{uuid4().hex[:8]}"
        )

    async def _process(self, stream_id: str, event) -> None:
        # Ordering matters: intelligence reads the state written here.
        await self.state_processor.process(event)
        await self.orchestrator.handle(event)
        await self.bus.ack(
            group_name=self.GROUP,
            stream_id=stream_id,
        )

    async def run(self) -> None:
        if not self.settings.REALTIME_ENABLED:
            logger.warning("Realtime pipeline disabled; worker will not start.")
            return

        event_types = {
            "token.updated",
            "wallet.updated",
            "pool.updated",
            "launchpad.detected",
            "chain.observed",
        }
        logger.info(
            "Starting ordered event worker consumer=%s group=%s",
            self.consumer_name,
            self.GROUP,
        )

        # Claim messages left pending by a previous crashed worker.
        async for stream_id, event in self.bus.recover_pending(
            group_name=self.GROUP,
            consumer_name=self.consumer_name,
            min_idle_ms=0,
            count=100,
        ):
            await self._process(stream_id, event)

        async for stream_id, event in self.bus.consume(
            group_name=self.GROUP,
            consumer_name=self.consumer_name,
            event_types=event_types,
        ):
            try:
                await self._process(stream_id, event)
            except Exception as exc:
                logger.exception(
                    "Pipeline processing failed; event remains pending stream=%s id=%s",
                    stream_id,
                    event.event_id,
                )
                # Do not ACK failed state/intelligence updates. Let container restart
                # and recover this pending message instead of silently dropping it.
                await publish_event(
                    event_type="system.updated",
                    entity_type="pipeline_worker",
                    entity_id=self.consumer_name,
                    chain=event.chain,
                    source="pipeline_worker",
                    source_id=event.event_id,
                    status="error",
                    payload={
                        "failed_stream_id": stream_id,
                        "failed_event_id": event.event_id,
                        "error": str(exc),
                    },
                )
                raise
'''

TOKEN_INGESTION_ENGINE = r'''from __future__ import annotations

import asyncio
import logging
from typing import Any

from ingestion.pumpfun_ingestor import PumpFunIngestor
from realtime.publisher import publish_event

logger = logging.getLogger("sentinel.ingestion.solana")


class TokenIngestionEngine:
    """Polling source for Pump.fun token discoveries.

    This deliberately publishes only the Solana source it actually ingests.
    Elysium events come from the EVM scanner, not Pump.fun or Raydium.
    """

    def __init__(self) -> None:
        self.pumpfun = PumpFunIngestor()
        self._seen: set[str] = set()

    async def run_once(self) -> int:
        raw_tokens = await self.pumpfun.fetch_new_tokens()
        if not isinstance(raw_tokens, list):
            logger.warning("Pump.fun response was not a list; skipping this scan.")
            return 0

        published = 0
        for raw in raw_tokens:
            if not isinstance(raw, dict):
                continue
            normalized = await self.pumpfun.normalize_token(raw)
            address = normalized.get("address")
            if not isinstance(address, str) or not address.strip():
                continue
            address = address.strip()
            if address in self._seen:
                continue

            payload: dict[str, Any] = {
                "token_mint": address,
                "mint": address,
                "name": normalized.get("name"),
                "symbol": normalized.get("symbol"),
                "market_cap_usd": normalized.get("market_cap"),
                "launchpad_id": "pumpfun",
                "launchpad_attribution_status": "VERIFIED",
            }
            await publish_event(
                event_type="token.updated",
                entity_type="token",
                entity_id=address,
                chain="solana",
                source="pumpfun_polling_api",
                source_id=f"pumpfun:{address}",
                status="observed",
                payload=payload,
            )
            self._seen.add(address)
            published += 1

        # Keep this process-local dedupe set bounded.
        if len(self._seen) > 50_000:
            self._seen = set(list(self._seen)[-25_000:])

        logger.info(
            "Pump.fun scan complete raw=%d published=%d",
            len(raw_tokens),
            published,
        )
        return published

    async def run_forever(self, interval_seconds: float = 15.0) -> None:
        while True:
            try:
                await self.run_once()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Pump.fun ingestion scan failed")
            await asyncio.sleep(interval_seconds)
'''

ELYSIUM_SCANNER = r'''from __future__ import annotations

import asyncio
import logging

from chains.evm.client import EVMClient
from chains.models import Chain
from chains.registry import get_chain_config
from config.settings import get_settings
from realtime.bus import get_realtime_bus
from realtime.models import ChainPosition
from realtime.publisher import publish_event

logger = logging.getLogger("sentinel.ingestion.elysium")


class ElysiumDeploymentScanner:
    """Detect top-level EVM contract deployments on Kinetiq Elysium.

    This is a bootstrap feed, not a full DEX indexer. It detects transactions
    with `to == null`, validates deployed contracts as ERC-20-like tokens,
    and publishes token.updated. Factory-created tokens (CREATE/CREATE2 inside
    another transaction), swaps and pool events require verified DEX factory
    addresses/ABIs and are intentionally not guessed here.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = EVMClient(get_chain_config(Chain.ELYSIUM))
        self.bus = get_realtime_bus()
        self.cursor_key = "sentinel:ingestion:elysium:last_block"

    async def _rpc(self, function, *args):
        return await asyncio.to_thread(function, *args)

    async def _publish_deployment(self, block, tx) -> None:
        tx_hash = tx["hash"].hex()
        receipt = await self._rpc(
            self.client.w3.eth.get_transaction_receipt,
            tx_hash,
        )
        contract_address = receipt.get("contractAddress")
        if not contract_address:
            return

        try:
            metadata = await self._rpc(
                self.client.token_metadata,
                contract_address,
            )
        except Exception:
            # Most deployed contracts are not ERC-20 tokens.
            return

        if metadata.get("symbol") == "UNKNOWN" and metadata.get("name") == "Unknown Token":
            return

        payload = {
            "token_address": contract_address,
            "address": contract_address,
            "name": metadata.get("name"),
            "symbol": metadata.get("symbol"),
            "decimals": metadata.get("decimals"),
            "total_supply": metadata.get("total_supply"),
            "creator_address": tx.get("from"),
            "deployment_block": block["number"],
            "transaction_hash": tx_hash,
        }

        await publish_event(
            event_type="token.updated",
            entity_type="token",
            entity_id=contract_address,
            chain="elysium",
            source="alchemy_elysium_block_scanner",
            source_id=tx_hash,
            status="observed",
            chain_position=ChainPosition(
                block_number=int(block["number"]),
                block_hash=block["hash"].hex(),
                transaction_hash=tx_hash,
            ),
            payload=payload,
        )

    async def scan_once(self) -> int:
        self.client.ensure_connected()
        head = int(await self._rpc(lambda: self.client.w3.eth.block_number))
        saved = await self.bus.redis.get(self.cursor_key)

        if saved is None:
            # Start at the current head. Do not silently attempt a huge backfill.
            await self.bus.redis.set(self.cursor_key, str(head))
            logger.info("Elysium scanner initialized at block %d", head)
            return 0

        next_block = int(saved) + 1
        published = 0
        while next_block <= head:
            block = await self._rpc(
                self.client.w3.eth.get_block,
                next_block,
                True,
            )
            for tx in block.get("transactions", []):
                if tx.get("to") is not None:
                    continue
                try:
                    await self._publish_deployment(block, tx)
                    published += 1
                except Exception:
                    logger.exception(
                        "Failed to inspect Elysium deployment tx=%s",
                        tx.get("hash"),
                    )
            await self.bus.redis.set(self.cursor_key, str(next_block))
            next_block += 1

        if published:
            logger.info("Elysium scanner published %d token deployments", published)
        return published

    async def run_forever(self, interval_seconds: float = 2.0) -> None:
        if not self.settings.ELYSIUM_RPC_URL:
            logger.warning("ELYSIUM_RPC_URL is empty; Elysium scanner is disabled.")
            return
        while True:
            try:
                await self.scan_once()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Elysium block scanner failed")
            await asyncio.sleep(interval_seconds)
'''

WORKER_MAIN = r'''from __future__ import annotations

import asyncio
import logging

from config.logging import setup_logging
from config.settings import get_settings
from ingestion.token_ingestion_engine import TokenIngestionEngine
from intelligence.worker import IntelligenceWorker
from ingestion.elysium_deployment_scanner import ElysiumDeploymentScanner


async def main() -> None:
    setup_logging()
    settings = get_settings()

    tasks = [
        asyncio.create_task(
            IntelligenceWorker().run(),
            name="sentinel-event-pipeline",
        ),
        asyncio.create_task(
            TokenIngestionEngine().run_forever(),
            name="sentinel-pumpfun-ingestion",
        ),
    ]

    if settings.ELYSIUM_RPC_URL:
        tasks.append(
            asyncio.create_task(
                ElysiumDeploymentScanner().run_forever(),
                name="sentinel-elysium-ingestion",
            )
        )

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
'''

DOCKER_COMPOSE = r'''services:
  postgres:
    image: postgres:16
    container_name: sentinel-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-sentinel}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-sentinel123}
      POSTGRES_DB: ${POSTGRES_DB:-sentinel}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-sentinel} -d ${POSTGRES_DB:-sentinel}"]
      interval: 5s
      timeout: 5s
      retries: 20

  redis:
    image: redis:7
    container_name: sentinel-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 20

  api:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    container_name: sentinel-api
    restart: unless-stopped
    env_file:
      - .env
    environment:
      POSTGRES_HOST: postgres
      REDIS_HOST: redis
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')"]
      interval: 10s
      timeout: 5s
      retries: 20
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  worker:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    container_name: sentinel-worker
    command: ["python", "-m", "worker_main"]
    restart: unless-stopped
    env_file:
      - .env
    environment:
      POSTGRES_HOST: postgres
      REDIS_HOST: redis
    depends_on:
      api:
        condition: service_healthy
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  web:
    build:
      context: ./apps/web
      dockerfile: Dockerfile
      args:
        NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-http://localhost:8000}
        NEXT_PUBLIC_WS_URL: ${NEXT_PUBLIC_WS_URL:-ws://localhost:8000}
        NEXT_PUBLIC_ELYSIUM_RPC_URL: ${NEXT_PUBLIC_ELYSIUM_RPC_URL:-}
    container_name: sentinel-web
    restart: unless-stopped
    ports:
      - "3000:3000"
    depends_on:
      - api

volumes:
  postgres_data:
'''

API_DOCKERFILE = r'''FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

WEB_DOCKERFILE = r'''FROM node:20-alpine AS dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ARG NEXT_PUBLIC_WS_URL=ws://localhost:8000
ARG NEXT_PUBLIC_ELYSIUM_RPC_URL=
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL \
    NEXT_PUBLIC_WS_URL=$NEXT_PUBLIC_WS_URL \
    NEXT_PUBLIC_ELYSIUM_RPC_URL=$NEXT_PUBLIC_ELYSIUM_RPC_URL
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "run", "start", "--", "--hostname", "0.0.0.0"]
'''


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply SentinelAI realtime and multi-chain integration fixes."
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the Sentinel_ai repository (default: current directory).",
    )
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    if not (root / "apps/api/src").is_dir() or not (root / "apps/web").is_dir():
        raise SystemExit(
            f"{root} does not look like the Sentinel_ai repository root. "
            "Pass --repo C:\\Users\\user\\Sentinel_ai"
        )

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = root / f".sentinel-fix-backup-{stamp}"
    backup.mkdir(parents=True, exist_ok=True)

    # Back up every file this patcher may edit before changing anything.
    targets = [
        "apps/api/src/config/settings.py",
        "apps/api/src/services/wallet_dna/api/lifespan.py",
        "apps/api/src/database/connection.py",
        "apps/api/src/database/session.py",
        "apps/api/src/database/database.py",
        "apps/api/src/database/init_db.py",
        "apps/api/src/models/base.py",
        "apps/api/src/models/watchlist.py",
        "apps/api/src/models/watchlist_item.py",
        "apps/api/src/state/service.py",
        "apps/api/src/state/redis_store.py",
        "apps/api/src/state/postgres_repository.py",
        "apps/api/requirements.txt",
        "apps/api/src/realtime/state_processor.py",
        "apps/api/src/realtime/models.py",
        "apps/api/src/realtime/bus.py",
        "apps/api/src/websocket/events_stream.py",
        "apps/api/src/intelligence/worker.py",
        "apps/api/src/ingestion/token_ingestion_engine.py",
        "apps/api/src/ingestion/elysium_deployment_scanner.py",
        "apps/api/src/worker_main.py",
        "apps/api/Dockerfile",
        "apps/web/Dockerfile",
        "apps/web/public/brand/chains/elysium.svg",
        "apps/api/src/config/settings.py",
        "apps/api/src/intelligence/orchestrator.py",
        "apps/api/src/intelligence/runner.py",
        "apps/api/src/realtime/publisher.py",
        "apps/web/store/realtimeStore.ts",
        "apps/web/hooks/useWebSocket.ts",
        "apps/web/components/ChainSelector/ChainSelector.tsx",
        "apps/web/components/ChainTabs/ChainTabs.tsx",
        "apps/web/app/discover/page.tsx",
        "apps/web/app/layout.tsx",
        "apps/web/types/chain.ts",
        "docker-compose.yml",
        ".env.example",
        "apps/api/.env.example",
    ]
    for rel in targets:
        source = root / rel
        if source.exists():
            destination = backup / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    # Settings: move Redis, CORS and Elysium declarations inside Settings.
    settings_path = root / "apps/api/src/config/settings.py"
    settings = settings_path.read_text(encoding="utf-8")
    redis_marker = '''    REDIS_PORT: int = 6379\n\n    REDIS_DB: int = 0\n'''
    redis_addition = '''    REDIS_PORT: int = 6379\n\n    REDIS_PASSWORD: str = ""\n    REDIS_DB: int = 0\n    REDIS_STREAM_MAXLEN: int = 1_000_000\n    REDIS_STREAM_BLOCK_MS: int = 5_000\n    REDIS_STREAM_READ_COUNT: int = 100\n\n    CORS_ORIGINS: list[str] = Field(\n        default_factory=lambda: ["http://localhost:3000"]\n    )\n'''
    if settings.count(redis_marker) != 1:
        raise RuntimeError("Could not safely locate the Redis settings block.")
    settings = settings.replace(redis_marker, redis_addition, 1)

    evm_marker = '''    ROBINHOOD_SEQUENCER_URL: str = (\n        "https://sequencer.mainnet.chain.robinhood.com"\n    )\n\n    # =========================================================\n    # EXTERNAL MARKET DATA\n'''
    evm_addition = '''    ROBINHOOD_SEQUENCER_URL: str = (\n        "https://sequencer.mainnet.chain.robinhood.com"\n    )\n\n    # ---------------------------------------------------------\n    # KINETIQ ELYSIUM MAINNET\n    # ---------------------------------------------------------\n\n    ELYSIUM_CHAIN_ID: int = 99901\n    ELYSIUM_NATIVE_SYMBOL: str = "HYPE"\n    ELYSIUM_RPC_URL: str = ""\n    ELYSIUM_WSS_URL: str = ""\n\n    # =========================================================\n    # EXTERNAL MARKET DATA\n'''
    if settings.count(evm_marker) != 1:
        raise RuntimeError("Could not safely locate the EVM settings insertion point.")
    settings = settings.replace(evm_marker, evm_addition, 1)

    # Remove the old indented, unreachable settings and module-level ELYSIUM variables
    # that were accidentally placed after return Settings().
    return_marker = '    return Settings()'
    return_index = settings.find(return_marker)
    if return_index < 0:
        raise RuntimeError("Could not find get_settings() return statement.")
    settings = settings[: return_index + len(return_marker)] + "\n"
    compatibility_marker = "    # =========================================================\n    # PRODUCTION VALIDATION\n"
    compatibility_block = (
        "    @property\n"
        "    def environment(self) -> str:\n"
        "        \"\"\"Compatibility alias used by older Wallet DNA modules.\"\"\"\n"
        "        return self.ENVIRONMENT\n\n"
        "" + compatibility_marker
    )
    if settings.count(compatibility_marker) != 1:
        raise RuntimeError("Could not safely add legacy Settings.environment compatibility property.")
    settings = settings.replace(compatibility_marker, compatibility_block, 1)
    settings += "\n\n# Backwards-compatible alias for legacy modules importing `settings`.\nsettings = get_settings()\n"
    settings_path.write_text(settings, encoding="utf-8")

    # Structural indentation defects: methods must be members of their classes.
    patch_once(
        root / "apps/api/src/intelligence/orchestrator.py",
        "        async def _run_score_engine(\n",
        "    async def _run_score_engine(\n",
        "Orchestrator scoring method indentation",
    )
    runner_path = root / "apps/api/src/intelligence/runner.py"
    patch_once(
        runner_path,
        "        async def scoring(\n",
        "    async def scoring(\n",
        "Runner scoring method indentation",
    )
    runner_text = runner_path.read_text(encoding="utf-8")
    old_lp = '''            "lp_burned": features.get(\n                "lp_burned",\n                token.lp_burned,\n            ),\n'''
    new_lp = '''            # TokenState has no lp_burned field. Only use observed feature data.\n            "lp_burned": features.get("lp_burned"),\n'''
    if runner_text.count(old_lp) != 1:
        raise RuntimeError("Could not safely patch the missing TokenState.lp_burned attribute.")
    runner_text = runner_text.replace(old_lp, new_lp, 1)
    old_missing = """        missing = [
            key
            for key in required
            if key not in features
            and not hasattr(token, key)
        ]
"""
    new_missing = """        missing = [
            key
            for key in required
            if features.get(key) is None
            and getattr(token, key, None) is None
        ]
"""
    if runner_text.count(old_missing) != 1:
        raise RuntimeError("Could not safely correct Rug Radar missing-evidence checks.")
    runner_text = runner_text.replace(old_missing, new_missing, 1)
    wallet_anchor = '''        payload = event.payload\n\n        source_address = payload.get(\n'''
    wallet_replacement = '''        payload = event.payload\n\n        # The legacy graph engine stores SOL-denominated transfers.\n        # Do not mislabel EVM token/HYPE amounts as SOL.\n        if event.chain != "solana":\n            return {\n                "status": "unavailable",\n                "missing_fields": ["chain_specific_wallet_amount_normalization"],\n            }\n\n        source_address = payload.get(\n'''
    if runner_text.count(wallet_anchor) != 1:
        raise RuntimeError("Could not safely locate Wallet DNA chain guard insertion point.")
    runner_path.write_text(runner_text.replace(wallet_anchor, wallet_replacement, 1), encoding="utf-8")

    # Repair the PostgreSQL bootstrap chain. The previous imports formed a
    # circular dependency and several modules referenced a nonexistent engine/Base.
    write_file(
        root,
        "apps/api/src/database/connection.py",
        r'''from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from config.settings import get_settings

settings = get_settings()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB,
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)
''',
    )
    write_file(
        root,
        "apps/api/src/database/session.py",
        r'''from __future__ import annotations

from sqlalchemy.orm import sessionmaker

from database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''',
    )
    write_file(
        root,
        "apps/api/src/database/database.py",
        r'''# Backwards-compatible aliases. The engine is defined only in connection.py.
from database.connection import engine
from database.session import SessionLocal

__all__ = ["engine", "SessionLocal"]
''',
    )
    write_file(
        root,
        "apps/api/src/models/base.py",
        r'''from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
''',
    )
    patch_once(
        root / "apps/api/src/state/service.py",
        "from state.postgres_store import PostgresStateStore",
        "from state.postgres_repository import PostgresStateStore",
        "StateService Postgres repository import",
    )
    patch_once(
        root / "apps/api/src/state/postgres_repository.py",
        "from database.connection import SessionLocal",
        "from database.session import SessionLocal",
        "PostgreSQL repository session import",
    )
    patch_once(
        root / "apps/api/src/state/service.py",
        "        else:\n            updater(current)\n\n            current.meta.version += 1\n",
        "        else:\n            current.meta.version += 1\n",
        "StateService update_token duplicate updater call",
    )
    patch_once(
        root / "apps/api/src/state/redis_store.py",
        "            db=settings.REDIS_DB,\n            decode_responses=True,",
        "            db=settings.REDIS_DB,\n            password=settings.REDIS_PASSWORD or None,\n            decode_responses=True,",
        "Redis state store password support",
    )
    patch_once(
        root / "apps/api/src/models/watchlist.py",
        "from apps.api.src.database.connection import Base",
        "from models.base import Base",
        "Watchlist Base import",
    )
    patch_once(
        root / "apps/api/src/models/watchlist_item.py",
        "from apps.api.src.database.connection import Base",
        "from models.base import Base",
        "WatchlistItem Base import",
    )
    patch_once(
        root / "apps/api/src/database/init_db.py",
        "from models.base import Base\n",
        "from models.base import Base\n\n# Import mapped classes so SQLAlchemy registers their tables.\nfrom models.state_history import StateSnapshot  # noqa: F401\nfrom models.watchlist import Watchlist  # noqa: F401\nfrom models.watchlist_item import WatchlistItem  # noqa: F401\n",
        "Database model registration",
    )

    # Add SQLAlchemy and the psycopg 3 PostgreSQL driver to the API image.
    requirements_path = root / "apps/api/requirements.txt"
    requirements = requirements_path.read_text(encoding="utf-8")
    for dependency in ("SQLAlchemy>=2.0,<3.0", "psycopg[binary]>=3.2,<4.0"):
        package_name = dependency.split(">", 1)[0].split("<", 1)[0].strip()
        if package_name.lower() not in requirements.lower():
            requirements += dependency + "\n"
    requirements_path.write_text(requirements, encoding="utf-8")

    # Replace the incompatible EventEnvelope state reducer with RealtimeEvent reducer.
    write_file(root, "apps/api/src/realtime/state_processor.py", STATE_PROCESSOR)
    write_file(root, "apps/api/src/intelligence/worker.py", INTELLIGENCE_WORKER)
    write_file(root, "apps/api/src/ingestion/token_ingestion_engine.py", TOKEN_INGESTION_ENGINE)
    write_file(root, "apps/api/src/ingestion/elysium_deployment_scanner.py", ELYSIUM_SCANNER)
    write_file(root, "apps/api/src/worker_main.py", WORKER_MAIN)

    # Publisher accepts EVM chain position metadata.
    publisher_path = root / "apps/api/src/realtime/publisher.py"
    publisher = publisher_path.read_text(encoding="utf-8")
    publisher = publisher.replace(
        "from realtime.models import RealtimeEvent\n",
        "from realtime.models import ChainPosition, RealtimeEvent\n",
        1,
    )
    sig_old = '''    status: str = "observed",\n) -> RealtimeEvent:\n'''
    sig_new = '''    status: str = "observed",\n    chain_position: ChainPosition | None = None,\n) -> RealtimeEvent:\n'''
    if publisher.count(sig_old) != 1:
        raise RuntimeError("Could not safely extend publish_event() signature.")
    publisher = publisher.replace(sig_old, sig_new, 1)
    event_old = '''        status=status,\n    )\n'''
    event_new = '''        status=status,\n        chain_position=chain_position,\n    )\n'''
    if publisher.count(event_old) != 1:
        raise RuntimeError("Could not safely add chain_position to RealtimeEvent publisher.")
    publisher_path.write_text(publisher.replace(event_old, event_new, 1), encoding="utf-8")

    # Resume Redis Stream delivery from the last cursor received by this browser.
    patch_once(
        root / "apps/api/src/realtime/models.py",
        "    processed_at: datetime | None = None\n\n    chain_position: ChainPosition | None = None\n",
        "    processed_at: datetime | None = None\n\n    stream_cursor: str | None = None\n\n    chain_position: ChainPosition | None = None\n",
        "RealtimeEvent stream cursor field",
    )
    patch_once(
        root / "apps/api/src/realtime/bus.py",
        "                    yield event\n",
        "                    yield event.model_copy(update={\"stream_cursor\": str(stream_id)})\n",
        "Redis event stream cursor",
    )
    ws_path = root / "apps/api/src/websocket/events_stream.py"
    ws_text = ws_path.read_text(encoding="utf-8")
    if ws_text.count("import logging\n") != 1:
        raise RuntimeError("Could not safely import re for WebSocket cursor validation.")
    ws_text = ws_text.replace("import logging\n", "import logging\nimport re\n", 1)
    ws_accept = "    await websocket.accept()\n"
    ws_accept_new = (
        "    last_id = websocket.query_params.get(\"last_id\") or \"$\"\n"
        "    if last_id != \"$\" and re.fullmatch(r\"[0-9]+-[0-9]+\", last_id) is None:\n"
        "        last_id = \"$\"\n\n"
        "    await websocket.accept()\n"
    )
    if ws_text.count(ws_accept) != 1:
        raise RuntimeError("Could not safely insert WebSocket cursor parsing.")
    ws_text = ws_text.replace(ws_accept, ws_accept_new, 1)
    ws_sub = (
        "        async for event in bus.subscribe(\n"
        "            event_types=CLIENT_EVENT_TYPES,\n"
        "        ):\n"
    )
    ws_sub_new = (
        "        async for event in bus.subscribe(\n"
        "            event_types=CLIENT_EVENT_TYPES,\n"
        "            last_id=last_id,\n"
        "        ):\n"
    )
    if ws_text.count(ws_sub) != 1:
        raise RuntimeError("Could not safely pass last_id to Redis subscription.")
    ws_path.write_text(ws_text.replace(ws_sub, ws_sub_new, 1), encoding="utf-8")

    hook_path = root / "apps/web/hooks/useWebSocket.ts"
    hook = hook_path.read_text(encoding="utf-8")
    url_marker = "  url.search = \"\";\n  url.hash = \"\";\n\n  return url;\n"
    url_new = (
        "  url.search = \"\";\n  url.hash = \"\";\n\n"
        "  try {\n"
        "    const cursor = window.localStorage.getItem(\"sentinel-realtime-last-id\");\n"
        "    if (cursor && /^[0-9]+-[0-9]+$/.test(cursor)) {\n"
        "      url.searchParams.set(\"last_id\", cursor);\n"
        "    }\n"
        "  } catch {\n    // Storage can be disabled by browser privacy settings.\n  }\n\n  return url;\n"
    )
    if hook.count(url_marker) != 1:
        raise RuntimeError("Could not safely add last cursor to WebSocket URL.")
    hook = hook.replace(url_marker, url_new, 1)
    event_marker = (
        "    const handleEvent = (event: RealtimeEvent) => {\n"
        "      const store = useRealtimeStore.getState();\n"
    )
    event_new = (
        "    const handleEvent = (event: RealtimeEvent) => {\n"
        "      if (event.stream_cursor) {\n"
        "        try {\n"
        "          window.localStorage.setItem(\"sentinel-realtime-last-id\", event.stream_cursor);\n"
        "        } catch {\n"
        "          // Continue processing if browser storage is unavailable.\n"
        "        }\n"
        "      }\n\n"
        "      const store = useRealtimeStore.getState();\n"
    )
    if hook.count(event_marker) != 1:
        raise RuntimeError("Could not safely persist WebSocket event cursor.")
    hook_path.write_text(hook.replace(event_marker, event_new, 1), encoding="utf-8")

    # Frontend: mount the provider in the root layout.
    layout_path = root / "apps/web/app/layout.tsx"
    layout = layout_path.read_text(encoding="utf-8")
    layout_import = 'import Sidebar from "@/components/Sidebar/Sidebar";\n'
    if layout.count(layout_import) != 1:
        raise RuntimeError("Could not safely add RealtimeProvider import to layout.")
    layout = layout.replace(
        layout_import,
        layout_import + 'import RealtimeProvider from "@/components/realtime/RealtimeProvider";\n',
        1,
    )
    body_marker = '''      <body>\n        <div className="min-h-screen bg-[#070707] text-white">\n'''
    body_replacement = '''      <body>\n        <RealtimeProvider />\n        <div className="min-h-screen bg-[#070707] text-white">\n'''
    if layout.count(body_marker) != 1:
        raise RuntimeError("Could not safely mount RealtimeProvider in layout.")
    layout_path.write_text(layout.replace(body_marker, body_replacement, 1), encoding="utf-8")

    # ChainSelector: HYPE symbol, accurate Robinhood chain ID, Alchemy RPC via public env.
    selector_path = root / "apps/web/components/ChainSelector/ChainSelector.tsx"
    selector = selector_path.read_text(encoding="utf-8")
    if selector.count('symbol: "ELY"') != 1:
        raise RuntimeError("Could not find the old Elysium ELY display symbol.")
    selector = selector.replace('symbol: "ELY"', 'symbol: "HYPE"', 1)
    if selector.count('rpcUrls: [\n    "https://rpc.elysium.kinetiq.xyz",\n  ],') != 1:
        raise RuntimeError("Could not find the old Elysium wallet RPC URL.")
    selector = selector.replace(
        'rpcUrls: [\n    "https://rpc.elysium.kinetiq.xyz",\n  ],',
        'rpcUrls: process.env.NEXT_PUBLIC_ELYSIUM_RPC_URL\n      ? [process.env.NEXT_PUBLIC_ELYSIUM_RPC_URL]\n      : [],',
        1,
    )
    robin_old = '''  robinhood: {\n    chainId: 1,\n    chainName: "Ethereum Mainnet",\n    nativeCurrency: {\n      name: "Ether",\n      symbol: "ETH",\n      decimals: 18,\n    },\n    rpcUrls: ["https://ethereum.publicnode.com"],\n    blockExplorerUrls: ["https://etherscan.io"],\n  },\n'''
    robin_new = '''  robinhood: {\n    chainId: 4663,\n    chainName: "Robinhood Chain",\n    nativeCurrency: {\n      name: "Ether",\n      symbol: "ETH",\n      decimals: 18,\n    },\n    rpcUrls: ["https://rpc.mainnet.chain.robinhood.com"],\n    blockExplorerUrls: ["https://robinhoodchain.blockscout.com"],\n  },\n'''
    if selector.count(robin_old) != 1:
        raise RuntimeError("Could not safely correct Robinhood wallet network configuration.")
    selector = selector.replace(robin_old, robin_new, 1)
    network_guard = '''    if (!network) {\n      setOpen(false);\n      return;\n    }\n'''
    network_guard_new = '''    if (!network) {\n      setOpen(false);\n      return;\n    }\n\n    if (network.rpcUrls.length === 0) {\n      console.warn("Set NEXT_PUBLIC_ELYSIUM_RPC_URL before adding Elysium to the wallet.");\n      setOpen(false);\n      return;\n    }\n'''
    if selector.count(network_guard) != 1:
        raise RuntimeError("Could not safely add missing Elysium browser RPC guard.")
    selector_path.write_text(selector.replace(network_guard, network_guard_new, 1), encoding="utf-8")

    tabs_path = root / "apps/web/components/ChainTabs/ChainTabs.tsx"
    tabs = tabs_path.read_text(encoding="utf-8")
    if tabs.count('name: "Elysium",\n    symbol: "PYR"') != 1:
        raise RuntimeError("Could not locate stale PYR symbol in ChainTabs.")
    tabs_path.write_text(
        tabs.replace('name: "Elysium",\n    symbol: "PYR"', 'name: "Kinetiq Elysium",\n    symbol: "HYPE"', 1),
        encoding="utf-8",
    )

    # Realtime state keys must include chain; expose raw entity ID separately for cards.
    store_path = root / "apps/web/store/realtimeStore.ts"
    store = store_path.read_text(encoding="utf-8")
    store = patch_text_in_memory(
        store,
        "  processed_at: string | null;\n\n  chain_position?: {\n",
        "  processed_at: string | null;\n  stream_cursor?: string | null;\n\n  chain_position?: {\n",
        "Frontend realtime stream cursor type",
    )
    store = patch_text_in_memory(
        store,
        "export interface RealtimeEntityState {\n  values: Record<string, unknown>;\n",
        "export interface RealtimeEntityState {\n  entityId: string;\n  values: Record<string, unknown>;\n",
        "RealtimeEntityState entityId",
    )
    store = patch_text_in_memory(
        store,
        "  return {\n    values: {\n      ...(current?.values ?? {}),\n      ...patch,\n    },\n\n    chain: event.chain ?? current?.chain ?? null,\n",
        "  return {\n    entityId: event.entity_id,\n    values: {\n      ...(current?.values ?? {}),\n      ...patch,\n    },\n\n    chain: event.chain ?? current?.chain ?? null,\n",
        "RealtimeEntityState entity ID assignment",
    )
    store = patch_text_in_memory(
        store,
        "        const current =\n          collections[event.entity_id];\n",
        "        const entityKey = `${event.chain ?? \"unknown\"}:${event.entity_id}`;\n        const current = collections[entityKey];\n",
        "Chain-qualified realtime entity lookup",
    )
    store = store.replace("[event.entity_id]:\n                    nextEntity,", "[entityKey]:\n                    nextEntity,")
    if store.count("[entityKey]:\n                    nextEntity,") != 3:
        raise RuntimeError("Expected all three realtime collections to use chain-qualified keys.")
    store_path.write_text(store, encoding="utf-8")

    # Discover filters records by selected chain and uses the actual address, not the qualified key.
    discover_path = root / "apps/web/app/discover/page.tsx"
    discover = discover_path.read_text(encoding="utf-8")
    import_marker = 'import { useRealtimeStore } from "@/store/realtimeStore";\n'
    if discover.count(import_marker) != 1:
        raise RuntimeError("Could not add chain selector store import to Discover.")
    discover = discover.replace(
        import_marker,
        import_marker + 'import { useChainStore } from "@/store/chainStore";\n',
        1,
    )
    component_marker = "export default function DiscoverPage() {\n"
    discover = patch_text_in_memory(
        discover,
        component_marker,
        component_marker + '  const selectedChain = useChainStore((state) => state.selectedChain);\n\n',
        "Discover selected chain state",
    )
    map_marker = "  const tokens = Object.entries(tokenRecords)\n    .map(([entityId, entity]) => {\n"
    map_new = "  const tokens = Object.entries(tokenRecords)\n    .filter(([, entity]) => (entity.chain ?? \"unknown\").toLowerCase() === selectedChain)\n    .map(([, entity]) => {\n"
    discover = patch_text_in_memory(discover, map_marker, map_new, "Discover chain filter")
    discover = patch_text_in_memory(
        discover,
        "        ) || entityId;\n",
        "        ) || entity.entityId;\n",
        "Discover actual token ID fallback",
    )
    discover_path.write_text(discover, encoding="utf-8")

    # Remove duplicate Zustand store definition from types/chain.ts.
    write_file(
        root,
        "apps/web/types/chain.ts",
        'export type { ChainId } from "@/store/chainStore";',
    )

    # Deployment files.
    write_file(root, "apps/api/Dockerfile", API_DOCKERFILE)
    write_file(root, "apps/web/Dockerfile", WEB_DOCKERFILE)
    write_file(
        root,
        "apps/web/public/brand/chains/elysium.svg",
        r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="29" fill="#101010" stroke="#D4AF37" stroke-width="2"/>
  <path d="M43 17H25L16 32L25 47H43" fill="none" stroke="#F5C84C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M26 32H42" stroke="#F5C84C" stroke-width="5" stroke-linecap="round"/>
</svg>''',
    )
    write_file(root, "docker-compose.yml", DOCKER_COMPOSE)

    # Root .env.example is the Compose env_file. Add backend Alchemy URL and browser RPC variable.
    root_env = root / ".env.example"
    if root_env.exists():
        text = root_env.read_text(encoding="utf-8")
        block = '''\n# Kinetiq Elysium mainnet (Alchemy)\nELYSIUM_CHAIN_ID=99901\nELYSIUM_NATIVE_SYMBOL=HYPE\nELYSIUM_RPC_URL=https://elysium-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY\nELYSIUM_WSS_URL=wss://elysium-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY\n\n# Browser wallet network-add URL. This value is public in the browser.\n# Use an Alchemy key restricted by allowed origins/usage.\nNEXT_PUBLIC_ELYSIUM_RPC_URL=\n'''
        if "ELYSIUM_RPC_URL=" not in text:
            text += block
            root_env.write_text(text, encoding="utf-8")

    api_env = root / "apps/api/.env.example"
    if api_env.exists():
        text = api_env.read_text(encoding="utf-8")
        block = '''\n# Kinetiq Elysium mainnet (Alchemy)\nELYSIUM_CHAIN_ID=99901\nELYSIUM_NATIVE_SYMBOL=HYPE\nELYSIUM_RPC_URL=https://elysium-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY\nELYSIUM_WSS_URL=wss://elysium-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY\n'''
        if "ELYSIUM_RPC_URL=" not in text:
            text += block
            api_env.write_text(text, encoding="utf-8")

    print("SentinelAI fix pack applied.")
    print(f"Backup folder: {backup}")
    print("Next: configure the real .env, then run the syntax/build checks in README.md.")


def patch_text_in_memory(content: str, old: str, new: str, label: str) -> str:
    count = content.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one exact match, found {count}.")
    return content.replace(old, new, 1)


if __name__ == "__main__":
    main()
