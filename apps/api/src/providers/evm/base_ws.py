from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from collections.abc import AsyncIterator, Sequence
from datetime import datetime, timezone
from typing import Any

from websockets.asyncio.client import ClientConnection
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed

from realtime.bus import get_realtime_bus
from realtime.models import RealtimeEvent


logger = logging.getLogger(__name__)


class EVMWebSocketError(RuntimeError):
    """Raised when an EVM websocket stream cannot be established."""


class EVMWebSocketAdapter:
    """
    Shared persistent EVM websocket adapter.

    Responsibilities:
    - Connect to the configured WSS endpoint.
    - Subscribe to newHeads.
    - Subscribe to filtered logs when addresses/topics are supplied.
    - Automatically reconnect with exponential backoff.
    - Convert provider-specific JSON-RPC notifications into
      SentinelAI RealtimeEvent objects.
    - Publish those events to the central realtime bus.

    Important:
    This class does NOT decide that a log is a token launch,
    pool creation, whale action, or launchpad event.

    It only observes and transports chain evidence.

    Higher layers perform protocol-specific interpretation.
    """

    def __init__(
        self,
        *,
        chain: str,
        chain_id: int,
        wss_url: str,
        provider_name: str = "evm_wss",
        log_addresses: Sequence[str] | None = None,
        log_topics: Sequence[str | None] | None = None,
        reconnect_delay_seconds: float = 2.0,
        max_reconnect_delay_seconds: float = 30.0,
        heartbeat_seconds: float = 20.0,
    ) -> None:
        self.chain = chain
        self.chain_id = chain_id
        self.wss_url = wss_url.strip()
        self.provider_name = provider_name

        self.log_addresses = tuple(
            self._normalize_address(address)
            for address in (log_addresses or [])
        )

        self.log_topics = tuple(
            topic.lower() if isinstance(topic, str) else None
            for topic in (log_topics or [])
        )

        self.reconnect_delay_seconds = (
            reconnect_delay_seconds
        )

        self.max_reconnect_delay_seconds = (
            max_reconnect_delay_seconds
        )

        self.heartbeat_seconds = (
            heartbeat_seconds
        )

        self._request_id = 0
        self._running = False
        self._subscription_ids: set[str] = set()

        self.bus = get_realtime_bus()

    # =========================================================
    # PUBLIC API
    # =========================================================

    async def run(self) -> None:
        """
        Run forever until stop() is called.

        This is the process-level producer for this chain.
        """
        if self._running:
            logger.warning(
                "%s stream is already running",
                self.chain,
            )
            return

        if not self.wss_url:
            raise EVMWebSocketError(
                f"No WSS URL configured for {self.chain}"
            )

        self._running = True

        delay = self.reconnect_delay_seconds

        try:
            while self._running:
                try:
                    await self._run_connection()

                    # A clean return while still running means the
                    # provider ended the connection. Reconnect.
                    if self._running:
                        logger.warning(
                            "%s websocket ended unexpectedly",
                            self.chain,
                        )

                except asyncio.CancelledError:
                    raise

                except Exception:
                    logger.exception(
                        "%s websocket connection failed",
                        self.chain,
                    )

                if not self._running:
                    break

                await self._publish_status(
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

            await self._publish_status(
                status="stopped",
                error=None,
            )

    async def stop(self) -> None:
        """
        Request graceful termination.

        The active websocket is closed by the connection context.
        """
        self._running = False

    # =========================================================
    # CONNECTION
    # =========================================================

    async def _run_connection(self) -> None:
        """
        Establish one websocket session and process it until
        the connection closes.
        """

        logger.info(
            "Connecting %s websocket: %s",
            self.chain,
            self.provider_name,
        )

        async with connect(
            self.wss_url,
            open_timeout=15,
            close_timeout=10,
            ping_interval=self.heartbeat_seconds,
            ping_timeout=self.heartbeat_seconds,
            max_size=None,
        ) as websocket:

            await self._publish_status(
                status="connected",
                error=None,
            )

            self._subscription_ids.clear()

            await self._subscribe(
                websocket,
                "newHeads",
            )

            if self.log_addresses:
                await self._subscribe_logs(
                    websocket,
                )

            logger.info(
                "%s websocket subscriptions active",
                self.chain,
            )

            await self._receive_loop(
                websocket,
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
                    "%s websocket connection closed",
                    self.chain,
                )
                return

            if raw_message is None:
                return

            if isinstance(raw_message, bytes):
                raw_message = raw_message.decode(
                    "utf-8",
                    errors="replace",
                )

            if not raw_message:
                continue

            try:
                message = json.loads(raw_message)
            except json.JSONDecodeError:
                logger.warning(
                    "%s provider sent invalid JSON",
                    self.chain,
                )
                continue

            await self._handle_message(
                message,
            )

    # =========================================================
    # SUBSCRIPTIONS
    # =========================================================

    async def _subscribe(
        self,
        websocket: ClientConnection,
        subscription_type: str,
    ) -> str:
        request_id = self._next_request_id()

        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "eth_subscribe",
            "params": [subscription_type],
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

            message = json.loads(raw_message)

            if message.get("id") == request_id:
                error = message.get("error")

                if error:
                    raise EVMWebSocketError(
                        f"{self.chain} subscription "
                        f"{subscription_type} failed: "
                        f"{error}"
                    )

                subscription_id = message.get(
                    "result"
                )

                if not isinstance(
                    subscription_id,
                    str,
                ):
                    raise EVMWebSocketError(
                        f"{self.chain} subscription "
                        f"{subscription_type} returned "
                        "an invalid subscription ID"
                    )

                self._subscription_ids.add(
                    subscription_id
                )

                logger.info(
                    "%s subscribed to %s",
                    self.chain,
                    subscription_type,
                )

                return subscription_id

            # A provider may deliver a notification while
            # we wait for an acknowledgement. Do not silently
            # discard it.
            await self._handle_message(
                message,
            )

    async def _subscribe_logs(
        self,
        websocket: ClientConnection,
    ) -> str:
        request_id = self._next_request_id()

        filter_object: dict[str, Any] = {
            "address": list(
                self.log_addresses
            )
        }

        if self.log_topics:
            filter_object["topics"] = list(
                self.log_topics
            )

        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "eth_subscribe",
            "params": [
                "logs",
                filter_object,
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

            message = json.loads(raw_message)

            if message.get("id") == request_id:
                error = message.get("error")

                if error:
                    raise EVMWebSocketError(
                        f"{self.chain} log subscription failed: "
                        f"{error}"
                    )

                subscription_id = message.get(
                    "result"
                )

                if not isinstance(
                    subscription_id,
                    str,
                ):
                    raise EVMWebSocketError(
                        f"{self.chain} log subscription returned "
                        "an invalid subscription ID"
                    )

                self._subscription_ids.add(
                    subscription_id
                )

                logger.info(
                    "%s filtered log subscription active",
                    self.chain,
                )

                return subscription_id

            await self._handle_message(
                message,
            )

    # =========================================================
    # MESSAGE HANDLING
    # =========================================================

    async def _handle_message(
        self,
        message: dict[str, Any],
    ) -> None:
        method = message.get("method")

        if method != "eth_subscription":
            return

        params = message.get("params")

        if not isinstance(params, dict):
            return

        subscription_id = params.get(
            "subscription"
        )

        result = params.get(
            "result"
        )

        if not isinstance(result, dict):
            return

        if subscription_id not in self._subscription_ids:
            # Do not reject the message as false data.
            # Keep the raw provider observation visible.
            logger.debug(
                "%s received notification for unknown "
                "subscription %s",
                self.chain,
                subscription_id,
            )

        if self._looks_like_log(result):
            event = self._log_to_event(
                result=result,
                subscription_id=subscription_id,
            )
        else:
            event = self._head_to_event(
                result=result,
                subscription_id=subscription_id,
            )

        await self.bus.publish(
            event
        )

    # =========================================================
    # CANONICAL EVENT CONVERSION
    # =========================================================

    def _head_to_event(
        self,
        *,
        result: dict[str, Any],
        subscription_id: str | None,
    ) -> RealtimeEvent:
        block_number = self._hex_int(
            result.get("number")
        )

        timestamp = self._hex_int(
            result.get("timestamp")
        )

        block_hash = result.get(
            "hash"
        )

        event_identity = "|".join(
            [
                self.chain,
                "newHeads",
                str(block_hash or ""),
                str(block_number or ""),
            ]
        )

        event_id = self._stable_event_id(
            event_identity
        )

        observed_at = (
            self._timestamp_from_unix(
                timestamp
            )
            if timestamp is not None
            else datetime.now(
                timezone.utc
            )
        )

        return RealtimeEvent(
            event_id=event_id,
            event_type="system.updated",
            entity_type="chain_block",
            entity_id=(
                block_hash
                or f"{self.chain}:{block_number}"
            ),
            chain=self.chain,
            source=self.provider_name,
            source_id=subscription_id,
            observed_at=observed_at,
            status="observed",
            payload={
                "kind": "chain.head",
                "chain_id": self.chain_id,
                "block_number": block_number,
                "block_hash": block_hash,
                "parent_hash": result.get(
                    "parentHash"
                ),
                "state_root": result.get(
                    "stateRoot"
                ),
                "transactions_root": result.get(
                    "transactionsRoot"
                ),
                "receipts_root": result.get(
                    "receiptsRoot"
                ),
                "miner": result.get(
                    "miner"
                ),
                "gas_limit": self._hex_int(
                    result.get("gasLimit")
                ),
                "gas_used": self._hex_int(
                    result.get("gasUsed")
                ),
                "timestamp": timestamp,
                "provider_payload": result,
            },
        )

    def _log_to_event(
        self,
        *,
        result: dict[str, Any],
        subscription_id: str | None,
    ) -> RealtimeEvent:
        transaction_hash = result.get(
            "transactionHash"
        )

        block_hash = result.get(
            "blockHash"
        )

        log_index = self._hex_int(
            result.get("logIndex")
        )

        block_number = self._hex_int(
            result.get("blockNumber")
        )

        transaction_index = self._hex_int(
            result.get(
                "transactionIndex"
            )
        )

        address = self._normalize_address(
            str(
                result.get(
                    "address",
                    "",
                )
            )
        )

        topics = [
            topic.lower()
            if isinstance(topic, str)
            else topic
            for topic in (
                result.get("topics")
                or []
            )
        ]

        removed = bool(
            result.get(
                "removed",
                False,
            )
        )

        event_identity = "|".join(
            [
                self.chain,
                "log",
                str(transaction_hash or ""),
                str(log_index),
                str(block_hash or ""),
                str(address),
                json.dumps(
                    topics,
                    sort_keys=True,
                ),
            ]
        )

        event_id = self._stable_event_id(
            event_identity
        )

        return RealtimeEvent(
            event_id=event_id,
            event_type="system.updated",
            entity_type="chain_log",
            entity_id=(
                f"{transaction_hash or block_hash or address}:"
                f"{log_index}"
            ),
            chain=self.chain,
            source=self.provider_name,
            source_id=subscription_id,
            observed_at=datetime.now(
                timezone.utc
            ),
            status="observed",
            payload={
                "kind": "chain.log",
                "chain_id": self.chain_id,
                "address": address,
                "topics": topics,
                "data": result.get(
                    "data"
                ),
                "block_number": block_number,
                "block_hash": block_hash,
                "transaction_hash": transaction_hash,
                "transaction_index": transaction_index,
                "log_index": log_index,
                "removed": removed,
                "provider_payload": result,
            },
        )

    # =========================================================
    # STATUS
    # =========================================================

    async def _publish_status(
        self,
        *,
        status: str,
        error: str | None,
    ) -> None:
        event = RealtimeEvent(
            event_type="system.updated",
            entity_type="provider",
            entity_id=(
                f"{self.provider_name}:{self.chain}"
            ),
            chain=self.chain,
            source=self.provider_name,
            source_id=self.chain,
            payload={
                "kind": "provider.status",
                "status": status,
                "error": error,
                "chain_id": self.chain_id,
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
                "Failed to publish %s provider status",
                self.chain,
            )

    # =========================================================
    # HELPERS
    # =========================================================

    def _next_request_id(self) -> int:
        self._request_id += 1
        return self._request_id

    @staticmethod
    def _normalize_address(
        address: str,
    ) -> str:
        return address.strip().lower()

    @staticmethod
    def _hex_int(
        value: Any,
    ) -> int | None:
        if value is None:
            return None

        if isinstance(value, int):
            return value

        if not isinstance(value, str):
            return None

        try:
            return int(
                value,
                16,
            )
        except ValueError:
            return None

    @staticmethod
    def _timestamp_from_unix(
        value: int | None,
    ) -> datetime:
        if value is None:
            return datetime.now(
                timezone.utc
            )

        try:
            return datetime.fromtimestamp(
                value,
                tz=timezone.utc,
            )
        except (
            OverflowError,
            OSError,
            ValueError,
        ):
            return datetime.now(
                timezone.utc
            )

    @staticmethod
    def _stable_event_id(
        value: str,
    ) -> str:
        return (
            hashlib.sha256(
                value.encode(
                    "utf-8"
                )
            ).hexdigest()
        )

    @staticmethod
    def _looks_like_log(
        result: dict[str, Any],
    ) -> bool:
        return (
            "transactionHash" in result
            and "topics" in result
            and "address" in result
        )

class BaseChainWebSocketAdapter(
    EVMWebSocketAdapter
):
    """
    Base Mainnet realtime chain observer.
    """

    def __init__(
        self,
        *,
        log_addresses: Sequence[str] | None = None,
        log_topics: Sequence[str | None] | None = None,
    ) -> None:
        settings = get_settings()

        wss_url = (
            settings.BASE_WSS_URL
            or self._build_alchemy_url(
                settings.ALCHEMY_API_KEY
            )
        )

        super().__init__(
            chain="base",
            chain_id=settings.BASE_CHAIN_ID,
            wss_url=wss_url,
            provider_name="alchemy",
            log_addresses=log_addresses,
            log_topics=log_topics,
            reconnect_delay_seconds=(
                settings.REALTIME_RECONNECT_DELAY_SECONDS
            ),
            max_reconnect_delay_seconds=(
                settings.REALTIME_MAX_RECONNECT_DELAY_SECONDS
            ),
            heartbeat_seconds=(
                settings.REALTIME_HEARTBEAT_SECONDS
            ),
        )

    @staticmethod
    def _build_alchemy_url(
        api_key: str,
    ) -> str:
        if not api_key.strip():
            return ""

        return (
            "wss://base-mainnet.g.alchemy.com/v2/"
            f"{api_key.strip()}"
        )        