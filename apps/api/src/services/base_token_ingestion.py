from __future__ import annotations

import asyncio
import logging
from typing import Any

from ingestion.pumpfun_ingestor import PumpFunIngestor
from realtime.publisher import publish_event


logger = logging.getLogger(
    "sentinel.ingestion.solana"
)


class TokenIngestionEngine:
    """Pump.fun token discovery publisher."""

    def __init__(self) -> None:
        self.pumpfun = PumpFunIngestor()
        self._seen: set[str] = set()

    async def run_once(self) -> int:
        raw_tokens = await self.pumpfun.fetch_new_tokens()

        if not isinstance(raw_tokens, list):
            logger.warning(
                "Pump.fun response was not a list."
            )
            return 0

        published = 0

        for raw in raw_tokens:
            if not isinstance(raw, dict):
                continue

            normalized = (
                await self.pumpfun.normalize_token(raw)
            )

            address = normalized.get("address")

            if (
                not isinstance(address, str)
                or not address.strip()
            ):
                continue

            address = address.strip()

            if address in self._seen:
                continue

            payload: dict[str, Any] = {
                "token_mint": address,
                "mint": address,
                "name": normalized.get("name"),
                "symbol": normalized.get("symbol"),
                "market_cap_usd": normalized.get(
                    "market_cap"
                ),
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

        if len(self._seen) > 50_000:
            self._seen = set(
                list(self._seen)[-25_000:]
            )

        logger.info(
            "Pump.fun scan complete raw=%d published=%d",
            len(raw_tokens),
            published,
        )

        return published

    async def run_forever(
        self,
        interval_seconds: float = 15.0,
    ) -> None:

        while True:
            try:
                await self.run_once()

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "Pump.fun ingestion scan failed"
                )

            await asyncio.sleep(interval_seconds)