from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from events.models import (
    TokenAuthorityChangedEvent,
    TokenMetadataUpdatedEvent,
    MarketSnapshotEvent,
    LiquidityChangedEvent,
    LaunchpadAttributionEvent,
)
from realtime.envelope import EventEnvelope
from realtime.bus import get_realtime_bus
from state.models import (
    StateMetadata,
    TokenState,
)
from state.service import get_state_service


class StateProcessor:
    """
    Converts canonical events into current canonical state.

    IMPORTANT:
    This is the reducer layer.

    Providers do not directly mutate Redis state.
    Routes do not directly mutate Redis state.
    WebSockets do not directly mutate Redis state.
    """

    def __init__(self) -> None:
        self.state = get_state_service()

    # =========================================================
    # TOKEN EVENT REDUCER
    # =========================================================

    async def process_token_event(
        self,
        event: EventEnvelope,
    ) -> TokenState | None:
        chain = event.chain
        mint = event.entity_id

        current = await self.state.get_token(
            chain,
            mint,
        )

        payload: dict[str, Any] = event.payload

        # -----------------------------------------------------
        # CREATE INITIAL STATE
        # -----------------------------------------------------

        if current is None:
            current = TokenState(
                chain=chain,
                mint=mint,
                name=payload.get("name"),
                symbol=payload.get("symbol"),
                decimals=payload.get("decimals"),
                creator_address=payload.get(
                    "creator_address"
                ),
                price_usd=(
                    self._decimal(
                        payload.get("price_usd")
                    )
                ),
                market_cap_usd=(
                    self._decimal(
                        payload.get("market_cap_usd")
                    )
                ),
                fdv_usd=(
                    self._decimal(
                        payload.get("fdv_usd")
                    )
                ),
                liquidity_usd=(
                    self._decimal(
                        payload.get("liquidity_usd")
                    )
                ),
                volume_5m_usd=(
                    self._decimal(
                        payload.get("volume_5m_usd")
                    )
                ),
                volume_1h_usd=(
                    self._decimal(
                        payload.get("volume_1h_usd")
                    )
                ),
                volume_24h_usd=(
                    self._decimal(
                        payload.get("volume_24h_usd")
                    )
                ),
                holders=payload.get("holders"),
                circulating_supply=(
                    self._decimal(
                        payload.get(
                            "circulating_supply"
                        )
                    )
                ),
                launchpad_id=payload.get(
                    "launchpad_id"
                ),
                launchpad_status=payload.get(
                    "launchpad_status",
                    "unresolved",
                ),
                metadata_uri=payload.get(
                    "metadata_uri"
                ),
                image_uri=payload.get(
                    "image_uri"
                ),
                meta=StateMetadata(
                    version=1,
                    last_event_id=event.event_id,
                    observed_at=event.observed_at,
                    updated_at=datetime.now(
                        timezone.utc
                    ),
                    source=event.source.provider,
                    status=event.quality.value,
                ),
            )

            await self.state.save_token(
                current
            )

            return current

        # -----------------------------------------------------
        # SAFE INCREMENT
        # -----------------------------------------------------

        next_version = (
            current.meta.version + 1
        )

        # -----------------------------------------------------
        # APPLY ONLY OBSERVED VALUES
        # -----------------------------------------------------

        for field in (
            "name",
            "symbol",
            "decimals",
            "creator_address",
            "holders",
            "metadata_uri",
            "image_uri",
            "launchpad_id",
            "launchpad_status",
        ):
            if field in payload:
                value = payload[field]

                # Do not convert missing values to
                # fake defaults.
                if value is not None:
                    setattr(
                        current,
                        field,
                        value,
                    )

        decimal_fields = (
            "price_usd",
            "market_cap_usd",
            "fdv_usd",
            "liquidity_usd",
            "volume_5m_usd",
            "volume_1h_usd",
            "volume_24h_usd",
            "circulating_supply",
        )

        for field in decimal_fields:
            if field in payload:
                value = (
                    self._decimal(
                        payload[field]
                    )
                )

                if value is not None:
                    setattr(
                        current,
                        field,
                        value,
                    )

        # -----------------------------------------------------
        # PROVENANCE / VERSION
        # -----------------------------------------------------

        current.meta.version = (
            next_version
        )

        current.meta.last_event_id = (
            event.event_id
        )

        current.meta.observed_at = (
            event.observed_at
        )

        current.meta.updated_at = (
            datetime.now(timezone.utc)
        )

        current.meta.source = (
            event.source.provider
        )

        current.meta.status = (
            event.quality.value
        )

        await self.state.save_token(
            current
        )

        return current

    # =========================================================
    # DISPATCH
    # =========================================================

    async def process(
        self,
        event: EventEnvelope,
    ) -> None:

        if (
            event.entity_type == "token"
        ):
            await self.process_token_event(
                event
            )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _decimal(
        value: Any,
    ) -> Decimal | None:

        if value is None:
            return None

        try:
            return Decimal(str(value))
        except Exception:
            return None


async def state_worker() -> None:
    """
    Dedicated Redis consumer-group worker.
    """

    bus = get_realtime_bus()

    processor = StateProcessor()

    async for stream_id, event in bus.consume(
        group_name="sentinel-state",
        consumer_name="state-worker-1",
    ):
        try:
            # EventEnvelope is the authoritative event
            # passed through the pipeline.
            await processor.process(
                EventEnvelope.model_validate(
                    event.to_wire()
                )
            )

            await bus.ack(
                group_name="sentinel-state",
                stream_id=stream_id,
            )

        except Exception:
            # Do NOT ACK failed state mutations.
            # It remains recoverable from the stream.
            raise