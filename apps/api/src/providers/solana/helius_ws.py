from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Any

from websockets.asyncio.client import ClientConnection
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed

from config.settings import get_settings
from realtime.bus import get_realtime_bus
from realtime.models import RealtimeEvent


logger = logging.getLogger(__name__)


class HeliusWebSocketError(
    RuntimeError
):
    """Raised when Helius realtime streaming fails."""


class HeliusWebSocketAdapter:
    """
    SentinelAI Solana realtime observer backed by
    Helius Enhanced WebSockets.

    This adapter observes transactions interacting with
    explicitly supplied Solana programs/accounts.

    It does not infer launchpad brands or trading semantics.
    """

    HELIUS_MAINNET_WSS = (
        "wss://atlas-mainnet.helius-rpc.com"
    )

    def __init__(
        self,
        *,
        account_include: Sequence[str],
        commitment: str = "confirmed",
        reconnect_delay_seconds: float | None = None,
        max_reconnect_delay_seconds: float | None = None,
        heartbeat_seconds: float | None = None,
    ) -> None:
        settings = get_settings()

        self.wss_url = (
            settings.HELIUS_WSS_URL
            or self._build_wss_url(
                settings.HELIUS_API_KEY
            )
        )

        self.account_include = tuple(
            dict.fromkeys(
                account.strip()
                for account in account_include
                if account and account.strip()
            )
        )

        if not self.account_include:
            raise HeliusWebSocketError(
                "At least one account/program is required "
                "for Helius transactionSubscribe"
            )

        self.commitment = commitment

        self.reconnect_delay_seconds = (
            reconnect_delay_seconds
            if reconnect_delay_seconds is not None
            else settings.REALTIME_RECONNECT_DELAY_SECONDS
        )

        self.max_reconnect_delay_seconds = (
            max_reconnect_delay_seconds
            if max_reconnect_delay_seconds is not None
            else settings.REALTIME_MAX_RECONNECT_DELAY_SECONDS
        )

        self.heartbeat_seconds = (
            heartbeat_seconds
            if heartbeat_seconds is not None
            else float(
                settings.REALTIME_HEARTBEAT_SECONDS
            )
        )

        self.bus = get_realtime_bus()

        self._running = False
        self._request_id = 0
        self._subscription_id: int | str | None = None

    # =========================================================
    # PUBLIC API
    # =========================================================

    async def run(self) -> None:
        """
        Maintain the Helius stream until stop() is called.
        """

        if self._running:
            logger.warning(
                "Helius Solana stream is already running"
            )
            return

        if not self.wss_url:
            raise HeliusWebSocketError(
                "HELIUS_WSS_URL or HELIUS_API_KEY is required"
            )

        self._running = True

        delay = self.reconnect_delay_seconds

        try:
            while self._running:
                try:
                    await self._run_connection()

                except asyncio.CancelledError:
                    raise

                except Exception:
                    logger.exception(
                        "Helius Solana stream failed"
                    )

                if not self._running:
                    break

                await self._publish_provider_status(
                    status="reconnecting",
                    error=None,
                )

                await asyncio.sleep(delay)

                delay = min(
                    delay * 2,
                    self.max_reconnect_delay_seconds,
                )

        finally:
            self._running = False

            await self._publish_provider_status(
                status="stopped",
                error=None,
            )

    async def stop(self) -> None:
        self._running = False

    # =========================================================
    # CONNECTION
    # =========================================================

    async def _run_connection(self) -> None:
        logger.info(
            "Connecting Helius Solana websocket"
        )

        async with connect(
            self.wss_url,
            open_timeout=15,
            close_timeout=10,
            ping_interval=self.heartbeat_seconds,
            ping_timeout=self.heartbeat_seconds,
            max_size=None,
        ) as websocket:

            await self._publish_provider_status(
                status="connected",
                error=None,
            )

            await self._subscribe(
                websocket
            )

            logger.info(
                "Helius transactionSubscribe active "
                "for %d accounts/programs",
                len(self.account_include),
            )

            await self._receive_loop(
                websocket
            )

    async def _receive_loop(
        self,
        websocket: ClientConnection,
    ) -> None:
        while self._running:
            try:
                raw_message = await websocket.recv()

            except ConnectionClosed:
                logger.warning(
                    "Helius websocket connection closed"
                )
                return

            if raw_message is None:
                return

            if isinstance(raw_message, bytes):
                raw_message = raw_message.decode(
                    "utf-8",
                    errors="replace",
                )

            try:
                message = json.loads(
                    raw_message
                )
            except json.JSONDecodeError:
                logger.warning(
                    "Helius returned invalid JSON"
                )
                continue

            await self._handle_message(
                message
            )

    # =========================================================
    # SUBSCRIPTION
    # =========================================================

    async def _subscribe(
        self,
        websocket: ClientConnection,
    ) -> None:
        request_id = self._next_request_id()

        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "transactionSubscribe",
            "params": [
                {
                    "failed": False,
                    "accountInclude": list(
                        self.account_include
                    ),
                },
                {
                    "commitment": self.commitment,
                    "encoding": "jsonParsed",
                    "transactionDetails": "full",
                    "maxSupportedTransactionVersion": 0,
                    "showRewards": True,
                },
            ],
        }

        await websocket.send(
            json.dumps(request)
        )

        while True:
            raw_message = await websocket.recv()

            if isinstance(raw_message, bytes):
                raw_message = raw_message.decode(
                    "utf-8",
                    errors="replace",
                )

            message = json.loads(
                raw_message
            )

            if message.get("id") == request_id:
                error = message.get("error")

                if error:
                    raise HeliusWebSocketError(
                        f"transactionSubscribe failed: {error}"
                    )

                self._subscription_id = (
                    message.get("result")
                )

                if self._subscription_id is None:
                    raise HeliusWebSocketError(
                        "Helius returned no subscription ID"
                    )

                logger.info(
                    "Helius subscription established: %s",
                    self._subscription_id,
                )

                return

            # Preserve notifications that may arrive
            # while waiting for subscription acknowledgement.
            await self._handle_message(
                message
            )

    # =========================================================
    # MESSAGE HANDLING
    # =========================================================

    async def _handle_message(
        self,
        message: dict[str, Any],
    ) -> None:
        if message.get(
            "method"
        ) != "transactionNotification":
            return

        params = message.get(
            "params"
        )

        if not isinstance(
            params,
            dict,
        ):
            return

        result = params.get(
            "result"
        )

        if not isinstance(
            result,
            dict,
        ):
            return

        event = self._transaction_to_event(
            result
        )

        await self.bus.publish(
            event
        )

    # =========================================================
    # CANONICAL EVENT
    # =========================================================

    def _transaction_to_event(
        self,
        result: dict[str, Any],
    ) -> RealtimeEvent:
        slot = result.get(
            "slot"
        )

        signature = result.get(
            "signature"
        )

        if not signature:
            signature = (
                self._extract_signature(
                    result
                )
            )

        if not signature:
            signature = (
                f"slot:{slot}"
            )

        event_id = self._stable_event_id(
            "|".join(
                [
                    "solana",
                    "helius",
                    str(slot),
                    str(signature),
                ]
            )
        )

        return RealtimeEvent(
            event_id=event_id,
            event_type="system.updated",
            entity_type="chain_transaction",
            entity_id=signature,
            chain="solana",
            source="helius",
            source_id=str(
                self._subscription_id
            )
            if self._subscription_id is not None
            else None,
            observed_at=datetime.now(
                timezone.utc
            ),
            status="observed",
            payload={
                "kind": "chain.transaction",
                "slot": slot,
                "signature": signature,
                "commitment": self.commitment,
                "account_include": list(
                    self.account_include
                ),
                "transaction": result,
            },
        )

    # =========================================================
    # STATUS
    # =========================================================

    async def _publish_provider_status(
        self,
        *,
        status: str,
        error: str | None,
    ) -> None:
        event = RealtimeEvent(
            event_type="system.updated",
            entity_type="provider",
            entity_id="helius:solana",
            chain="solana",
            source="helius",
            source_id=(
                str(self._subscription_id)
                if self._subscription_id is not None
                else None
            ),
            payload={
                "kind": "provider.status",
                "status": status,
                "error": error,
                "commitment": self.commitment,
                "account_include_count": len(
                    self.account_include
                ),
                "observed_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            },
            status="observed",
        )

        try:
            await self.bus.publish(
                event
            )
        except Exception:
            logger.exception(
                "Failed to publish Helius provider status"
            )

    # =========================================================
    # HELPERS
    # =========================================================

    @classmethod
    def _build_wss_url(
        cls,
        api_key: str,
    ) -> str:
        if not api_key.strip():
            return ""

        return (
            f"{cls.HELIUS_MAINNET_WSS}"
            "?api-key="
            f"{api_key.strip()}"
        )

    def _next_request_id(self) -> int:
        self._request_id += 1
        return self._request_id

    @staticmethod
    def _stable_event_id(
        value: str,
    ) -> str:
        return hashlib.sha256(
            value.encode(
                "utf-8"
            )
        ).hexdigest()

    @staticmethod
    def _extract_signature(
        result: dict[str, Any],
    ) -> str | None:
        """
        Best-effort extraction from the documented result shape.

        We do NOT fabricate a signature.
        """

        direct = result.get(
            "signature"
        )

        if isinstance(
            direct,
            str,
        ) and direct:
            return direct

        transaction = result.get(
            "transaction"
        )

        if not isinstance(
            transaction,
            dict,
        ):
            return None

        transaction_obj = transaction.get(
            "transaction"
        )

        if not isinstance(
            transaction_obj,
            dict,
        ):
            return None

        signatures = transaction_obj.get(
            "signatures"
        )

        if not isinstance(
            signatures,
            list,
        ):
            return None

        for signature in signatures:
            if isinstance(
                signature,
                str,
            ) and signature:
                return signature

        return None