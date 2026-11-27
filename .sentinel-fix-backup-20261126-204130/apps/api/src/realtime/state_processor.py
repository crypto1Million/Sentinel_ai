from __future__ import annotations

from datetime import datetime, timezone
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
    """Reduce canonical RealtimeEvent objects into state."""

    TOKEN_FIELDS = {
        "name", "symbol", "decimals", "price_usd",
        "market_cap_usd", "fdv_usd", "total_supply",
        "circulating_supply", "holders", "liquidity_usd",
        "volume_5m_usd", "volume_1h_usd", "volume_24h_usd",
        "buy_volume_5m_usd", "sell_volume_5m_usd",
        "transaction_count_5m", "launchpad_id",
        "launchpad_name", "launchpad_rail",
        "launchpad_attribution_status", "primary_pool_id",
        "pool_ids", "metadata_uri", "logo_uri",
        "creator_address", "mint_authority",
        "freeze_authority",
    }

    WALLET_FIELDS = {
        "native_balance", "token_count",
        "transaction_count", "total_volume_usd",
        "realized_pnl_usd", "unrealized_pnl_usd",
        "win_rate", "average_hold_seconds",
        "classification", "smart_money", "sniper",
        "insider", "fresh_wallet", "first_seen_at",
        "last_activity_at", "preferred_launchpads",
        "preferred_tokens",
    }

    POOL_FIELDS = {
        "base_reserve", "quote_reserve", "price_usd",
        "liquidity_usd", "volume_5m_usd",
        "volume_1h_usd", "volume_24h_usd",
        "buy_volume_5m_usd", "sell_volume_5m_usd",
        "fee_bps", "lp_supply", "created_at",
        "last_swap_at", "last_liquidity_change_at",
    }

    def __init__(
        self,
        state_service: StateService | None = None,
    ) -> None:
        self.state = state_service or StateService()

    @staticmethod
    def _meta(
        event: RealtimeEvent,
        version: int,
    ) -> StateMeta:
        return StateMeta(
            version=version,
            status=STATUS_MAP.get(
                event.status,
                StateStatus.UNAVAILABLE,
            ),
            source_id=event.source_id or event.source,
            observed_at=event.observed_at,
            processed_at=datetime.now(timezone.utc),
            last_event_id=event.event_id,
            parser=event.parser_name,
            parser_version=event.parser_version,
        )

    @staticmethod
    def _clean_payload(
        payload: dict[str, Any],
        allowed: set[str],
    ) -> dict[str, Any]:
        return {
            key: value
            for key, value in payload.items()
            if key in allowed and value is not None
        }

    async def _process_token(
        self,
        event: RealtimeEvent,
    ) -> None:
        mint = event.entity_id
        payload = dict(event.payload)

        # Normalize common provider aliases.
        if (
            "image_uri" in payload
            and "logo_uri" not in payload
        ):
            payload["logo_uri"] = payload["image_uri"]

        if (
            "launchpad_status" in payload
            and "launchpad_attribution_status" not in payload
        ):
            payload["launchpad_attribution_status"] = (
                str(payload["launchpad_status"]).upper()
            )

        if (
            "market_cap" in payload
            and "market_cap_usd" not in payload
        ):
            payload["market_cap_usd"] = payload["market_cap"]

        patch = self._clean_payload(
            payload,
            self.TOKEN_FIELDS,
        )

        chain = event.chain or "unknown"

        current = await self.state.get_token(
            chain,
            mint,
        )

        version = (
            current.meta.version + 1
            if current else 1
        )

        if current:
            data = current.model_dump()
            data.update(patch)
            data["meta"] = self._meta(event, version)

            updated = TokenState.model_validate(data)
        else:
            updated = TokenState(
                chain=chain,
                mint=mint,
                **patch,
                meta=self._meta(event, version),
            )

        await self.state.save_token(updated)

    async def _process_wallet(
        self,
        event: RealtimeEvent,
    ) -> None:
        address = str(
            event.payload.get("wallet_address")
            or event.payload.get("address")
            or event.entity_id
        )

        patch = self._clean_payload(
            event.payload,
            self.WALLET_FIELDS,
        )

        chain = event.chain or "unknown"

        current = await self.state.get_wallet(
            chain,
            address,
        )

        version = (
            current.meta.version + 1
            if current else 1
        )

        if current:
            data = current.model_dump()
            data.update(patch)
            data["meta"] = self._meta(event, version)

            updated = WalletState.model_validate(data)
        else:
            updated = WalletState(
                chain=chain,
                address=address,
                **patch,
                meta=self._meta(event, version),
            )

        await self.state.save_wallet(updated)

    async def _process_pool(
        self,
        event: RealtimeEvent,
    ) -> None:
        payload = event.payload

        pool_id = str(
            payload.get("pool_address")
            or payload.get("pool_id")
            or event.entity_id
        )

        chain = event.chain or "unknown"

        current = await self.state.get_pool(
            chain,
            pool_id,
        )

        # PoolState requires a DEX and two token addresses.
        dex_id = (
            payload.get("dex_id")
            or (current.dex_id if current else None)
        )

        base_token = (
            payload.get("base_token")
            or payload.get("token0")
            or (current.base_token if current else None)
        )

        quote_token = (
            payload.get("quote_token")
            or payload.get("token1")
            or (current.quote_token if current else None)
        )

        # Never fabricate missing pool identifiers.
        if not dex_id or not base_token or not quote_token:
            return

        patch = self._clean_payload(
            payload,
            self.POOL_FIELDS,
        )

        version = (
            current.meta.version + 1
            if current else 1
        )

        if current:
            data = current.model_dump()
            data.update(patch)
            data["meta"] = self._meta(event, version)

            updated = PoolState.model_validate(data)
        else:
            updated = PoolState(
                chain=chain,
                pool_id=pool_id,
                dex_id=str(dex_id),
                base_token=str(base_token),
                quote_token=str(quote_token),
                **patch,
                meta=self._meta(event, version),
            )

        await self.state.save_pool(updated)

    async def process(
        self,
        event: RealtimeEvent,
    ) -> None:
        if not event.chain:
            return

        if (
            event.event_type == "token.updated"
            and event.entity_type == "token"
        ):
            await self._process_token(event)

        elif (
            event.event_type == "wallet.updated"
            and event.entity_type == "wallet"
        ):
            await self._process_wallet(event)

        elif (
            event.event_type == "pool.updated"
            and event.entity_type == "pool"
        ):
            await self._process_pool(event)