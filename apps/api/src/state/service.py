from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Callable, TypeVar

from state.models import (
    DeveloperState,
    LaunchpadState,
    PoolState,
    StateMeta,
    StateStatus,
    TokenState,
    WalletState,
)
from state.postgres_store import PostgresStateStore
from state.redis_store import RedisStateStore


T = TypeVar("T")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StateService:
    """
    Canonical SentinelAI state service.

    Redis:
        current state

    PostgreSQL:
        append-only state history
    """

    def __init__(
        self,
        redis_store: RedisStateStore | None = None,
        postgres_store: PostgresStateStore | None = None,
    ) -> None:

        self.redis = (
            redis_store
            or RedisStateStore()
        )

        self.postgres = (
            postgres_store
            or PostgresStateStore()
        )

    # =========================================================
    # TOKEN
    # =========================================================

    async def get_token(
        self,
        chain: str,
        mint: str,
    ) -> TokenState | None:

        return await self.redis.get(
            entity_type="token",
            chain=chain,
            entity_id=mint,
            model_type=TokenState,
        )

    async def save_token(
        self,
        state: TokenState,
    ) -> TokenState:

        state = self._touch(
            state
        )

        saved = await self.redis.save(
            entity_type="token",
            chain=state.chain,
            entity_id=state.mint,
            state=state,
        )

        await self.postgres.append_snapshot(
            entity_type="token",
            chain=state.chain,
            entity_id=state.mint,
            state=saved,
        )

        return saved

    async def update_token(
        self,
        *,
        chain: str,
        mint: str,
        updater: Callable[
            [TokenState],
            None,
        ],
        event_id: str | None = None,
        source_id: str | None = None,
        observed_at: datetime | None = None,
        status: StateStatus | None = None,
    ) -> TokenState:

        current = await self.get_token(
            chain,
            mint,
        )

        if current is None:
            current = TokenState(
                chain=chain,
                mint=mint,
                meta=StateMeta(
                    status=(
                        status
                        or StateStatus.UNAVAILABLE
                    ),
                    source_id=source_id,
                    observed_at=observed_at,
                    last_event_id=event_id,
                ),
            )
        else:
            updater(current)

            current.meta.version += 1

            if event_id is not None:
                current.meta.last_event_id = (
                    event_id
                )

            if source_id is not None:
                current.meta.source_id = (
                    source_id
                )

            if observed_at is not None:
                current.meta.observed_at = (
                    observed_at
                )

            if status is not None:
                current.meta.status = status

        updater(current)

        current.meta.version = max(
            current.meta.version,
            1,
        )

        return await self.save_token(
            current
        )

    # =========================================================
    # POOL
    # =========================================================

    async def get_pool(
        self,
        chain: str,
        pool_id: str,
    ) -> PoolState | None:

        return await self.redis.get(
            entity_type="pool",
            chain=chain,
            entity_id=pool_id,
            model_type=PoolState,
        )

    async def save_pool(
        self,
        state: PoolState,
    ) -> PoolState:

        state = self._touch(
            state
        )

        saved = await self.redis.save(
            entity_type="pool",
            chain=state.chain,
            entity_id=state.pool_id,
            state=state,
        )

        await self.postgres.append_snapshot(
            entity_type="pool",
            chain=state.chain,
            entity_id=state.pool_id,
            state=saved,
        )

        return saved

    # =========================================================
    # WALLET
    # =========================================================

    async def get_wallet(
        self,
        chain: str,
        address: str,
    ) -> WalletState | None:

        return await self.redis.get(
            entity_type="wallet",
            chain=chain,
            entity_id=address.lower(),
            model_type=WalletState,
        )

    async def save_wallet(
        self,
        state: WalletState,
    ) -> WalletState:

        state = self._touch(
            state
        )

        saved = await self.redis.save(
            entity_type="wallet",
            chain=state.chain,
            entity_id=state.address.lower(),
            state=state,
        )

        await self.postgres.append_snapshot(
            entity_type="wallet",
            chain=state.chain,
            entity_id=state.address.lower(),
            state=saved,
        )

        return saved

    # =========================================================
    # DEVELOPER
    # =========================================================

    async def get_developer(
        self,
        chain: str,
        address: str,
    ) -> DeveloperState | None:

        return await self.redis.get(
            entity_type="developer",
            chain=chain,
            entity_id=address.lower(),
            model_type=DeveloperState,
        )

    async def save_developer(
        self,
        state: DeveloperState,
    ) -> DeveloperState:

        state = self._touch(
            state
        )

        saved = await self.redis.save(
            entity_type="developer",
            chain=state.chain,
            entity_id=state.address.lower(),
            state=state,
        )

        await self.postgres.append_snapshot(
            entity_type="developer",
            chain=state.chain,
            entity_id=state.address.lower(),
            state=saved,
        )

        return saved

    # =========================================================
    # LAUNCHPAD
    # =========================================================

    async def get_launchpad(
        self,
        chain: str,
        launchpad_id: str,
    ) -> LaunchpadState | None:

        return await self.redis.get(
            entity_type="launchpad",
            chain=chain,
            entity_id=launchpad_id,
            model_type=LaunchpadState,
        )

    async def save_launchpad(
        self,
        state: LaunchpadState,
    ) -> LaunchpadState:

        state = self._touch(
            state
        )

        saved = await self.redis.save(
            entity_type="launchpad",
            chain=state.chain,
            entity_id=state.launchpad_id,
            state=state,
        )

        await self.postgres.append_snapshot(
            entity_type="launchpad",
            chain=state.chain,
            entity_id=state.launchpad_id,
            state=saved,
        )

        return saved

    # =========================================================
    # INTERNAL
    # =========================================================

    @staticmethod
    def _touch(
        state: T,
    ) -> T:

        state.meta.processed_at = utc_now()

        if state.meta.observed_at:
            delta = (
                state.meta.processed_at
                - state.meta.observed_at
            )

            state.meta.age_ms = max(
                0,
                int(
                    delta.total_seconds()
                    * 1000
                ),
            )

        return state

    async def close(self) -> None:
        await self.redis.close()