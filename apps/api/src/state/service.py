from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis

from config.settings import get_settings
from state.models import (
    DeveloperState,
    LaunchpadState,
    PoolState,
    TokenState,
    WalletState,
)


class StateService:
    """
    Current-state storage for SentinelAI.

    Redis contains the latest canonical state.
    Historical events remain in the event stream/database.
    """

    def __init__(
        self,
        redis_client: Redis | None = None,
    ) -> None:
        settings = get_settings()

        self.redis = (
            redis_client
            if redis_client is not None
            else Redis.from_url(
                (
                    f"redis://"
                    f"{settings.REDIS_HOST}:"
                    f"{settings.REDIS_PORT}/"
                    f"{settings.REDIS_DB}"
                ),
                decode_responses=True,
            )
        )

        self.prefix = "sentinel:state"

    # =========================================================
    # TOKEN
    # =========================================================

    def _token_key(
        self,
        chain: str,
        mint: str,
    ) -> str:
        return (
            f"{self.prefix}:token:"
            f"{chain}:{mint}"
        )

    async def get_token(
        self,
        chain: str,
        mint: str,
    ) -> TokenState | None:
        raw = await self.redis.get(
            self._token_key(chain, mint)
        )

        if raw is None:
            return None

        return TokenState.model_validate_json(
            raw
        )

    async def save_token(
        self,
        state: TokenState,
    ) -> None:
        await self.redis.set(
            self._token_key(
                state.chain,
                state.mint,
            ),
            json.dumps(
                state.model_dump(
                    mode="json"
                ),
                separators=(",", ":"),
            ),
        )

    # =========================================================
    # POOL
    # =========================================================

    def _pool_key(
        self,
        chain: str,
        address: str,
    ) -> str:
        return (
            f"{self.prefix}:pool:"
            f"{chain}:{address}"
        )

    async def get_pool(
        self,
        chain: str,
        address: str,
    ) -> PoolState | None:
        raw = await self.redis.get(
            self._pool_key(chain, address)
        )

        if raw is None:
            return None

        return PoolState.model_validate_json(
            raw
        )

    async def save_pool(
        self,
        state: PoolState,
    ) -> None:
        await self.redis.set(
            self._pool_key(
                state.chain,
                state.address,
            ),
            json.dumps(
                state.model_dump(mode="json"),
                separators=(",", ":"),
            ),
        )

    # =========================================================
    # WALLET
    # =========================================================

    def _wallet_key(
        self,
        chain: str,
        address: str,
    ) -> str:
        return (
            f"{self.prefix}:wallet:"
            f"{chain}:{address}"
        )

    async def get_wallet(
        self,
        chain: str,
        address: str,
    ) -> WalletState | None:
        raw = await self.redis.get(
            self._wallet_key(
                chain,
                address,
            )
        )

        if raw is None:
            return None

        return WalletState.model_validate_json(
            raw
        )

    async def save_wallet(
        self,
        state: WalletState,
    ) -> None:
        await self.redis.set(
            self._wallet_key(
                state.chain,
                state.address,
            ),
            json.dumps(
                state.model_dump(mode="json"),
                separators=(",", ":"),
            ),
        )

    # =========================================================
    # DEVELOPER
    # =========================================================

    def _developer_key(
        self,
        chain: str,
        address: str,
    ) -> str:
        return (
            f"{self.prefix}:developer:"
            f"{chain}:{address}"
        )

    async def get_developer(
        self,
        chain: str,
        address: str,
    ) -> DeveloperState | None:
        raw = await self.redis.get(
            self._developer_key(
                chain,
                address,
            )
        )

        if raw is None:
            return None

        return DeveloperState.model_validate_json(
            raw
        )

    async def save_developer(
        self,
        state: DeveloperState,
    ) -> None:
        await self.redis.set(
            self._developer_key(
                state.chain,
                state.address,
            ),
            json.dumps(
                state.model_dump(mode="json"),
                separators=(",", ":"),
            ),
        )

    # =========================================================
    # LAUNCHPAD
    # =========================================================

    def _launchpad_key(
        self,
        chain: str,
        mint: str,
    ) -> str:
        return (
            f"{self.prefix}:launchpad:"
            f"{chain}:{mint}"
        )

    async def get_launchpad(
        self,
        chain: str,
        mint: str,
    ) -> LaunchpadState | None:
        raw = await self.redis.get(
            self._launchpad_key(
                chain,
                mint,
            )
        )

        if raw is None:
            return None

        return LaunchpadState.model_validate_json(
            raw
        )

    async def save_launchpad(
        self,
        state: LaunchpadState,
    ) -> None:
        await self.redis.set(
            self._launchpad_key(
                state.chain,
                state.token_mint,
            ),
            json.dumps(
                state.model_dump(mode="json"),
                separators=(",", ":"),
            ),
        )

    async def close(self) -> None:
        await self.redis.aclose()


_state_service: StateService | None = None


def get_state_service() -> StateService:
    global _state_service

    if _state_service is None:
        _state_service = StateService()

    return _state_service