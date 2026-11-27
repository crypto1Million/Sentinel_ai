from __future__ import annotations

import asyncio
import logging

from chains.evm.client import EVMClient
from chains.models import Chain
from chains.registry import get_chain_config
from config.settings import get_settings

from realtime.bus import get_realtime_bus
from realtime.models import ChainPosition
from realtime.publisher import publish_event


logger = logging.getLogger(
    "sentinel.ingestion.elysium"
)


class ElysiumDeploymentScanner:
    """Kinetiq Elysium top-level contract deployment scanner."""

    def __init__(self) -> None:
        self.settings = get_settings()

        self.client = EVMClient(
            get_chain_config(Chain.ELYSIUM)
        )

        self.bus = get_realtime_bus()

        self.cursor_key = (
            "sentinel:ingestion:elysium:last_block"
        )

    async def _rpc(self, function, *args):
        return await asyncio.to_thread(
            function,
            *args,
        )

    async def _publish_deployment(
        self,
        block,
        tx,
    ) -> bool:

        tx_hash = tx["hash"].hex()

        receipt = await self._rpc(
            self.client.w3.eth.get_transaction_receipt,
            tx_hash,
        )

        contract_address = receipt.get(
            "contractAddress"
        )

        if not contract_address:
            return False

        try:
            metadata = await self._rpc(
                self.client.token_metadata,
                contract_address,
            )

        except Exception:
            # Most deployments are not ERC-20 tokens.
            return False

        if (
            metadata.get("symbol") == "UNKNOWN"
            and metadata.get("name") == "Unknown Token"
        ):
            return False

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

        return True

    async def scan_once(self) -> int:
        self.client.ensure_connected()

        head = int(
            await self._rpc(
                lambda: self.client.w3.eth.block_number
            )
        )

        saved = await self.bus.redis.get(
            self.cursor_key
        )

        if saved is None:
            # Initialize at current head, avoiding an
            # unrequested historical backfill.
            await self.bus.redis.set(
                self.cursor_key,
                str(head),
            )

            logger.info(
                "Elysium scanner initialized at block %d",
                head,
            )

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
                    was_published = (
                        await self._publish_deployment(
                            block,
                            tx,
                        )
                    )

                    if was_published:
                        published += 1

                except Exception:
                    logger.exception(
                        "Failed to inspect Elysium deployment tx=%s",
                        tx.get("hash"),
                    )

            await self.bus.redis.set(
                self.cursor_key,
                str(next_block),
            )

            next_block += 1

        if published:
            logger.info(
                "Elysium scanner published %d token deployments",
                published,
            )

        return published

    async def run_forever(
        self,
        interval_seconds: float = 2.0,
    ) -> None:

        if not self.settings.ELYSIUM_RPC_URL:
            logger.warning(
                "ELYSIUM_RPC_URL is empty; scanner disabled."
            )
            return

        while True:
            try:
                await self.scan_once()

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "Elysium block scanner failed"
                )

            await asyncio.sleep(interval_seconds)