from __future__ import annotations

import json
from typing import TypeVar

from redis.asyncio import Redis

from config.settings import get_settings
from state.models import (
    DeveloperState,
    LaunchpadState,
    PoolState,
    TokenState,
    WalletState,
)


T = TypeVar(
    "T",
    TokenState,
    PoolState,
    WalletState,
    DeveloperState,
    LaunchpadState,
)


class RedisStateStore:
    def __init__(
        self,
        redis: Redis | None = None,
    ) -> None:
        settings = get_settings()

        self.redis = redis or Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
        )

        self.prefix = (
            settings.REDIS_STREAM_PREFIX
        )

    def _key(
        self,
        entity_type: str,
        chain: str,
        entity_id: str,
    ) -> str:
        return (
            f"{self.prefix}:state:"
            f"{entity_type}:"
            f"{chain}:"
            f"{entity_id}"
        )

    async def get(
        self,
        *,
        entity_type: str,
        chain: str,
        entity_id: str,
        model_type: type[T],
    ) -> T | None:

        key = self._key(
            entity_type,
            chain,
            entity_id,
        )

        payload = await self.redis.get(key)

        if payload is None:
            return None

        return model_type.model_validate_json(
            payload
        )

    async def save(
        self,
        *,
        entity_type: str,
        chain: str,
        entity_id: str,
        state: T,
    ) -> T:

        key = self._key(
            entity_type,
            chain,
            entity_id,
        )

        payload = state.model_dump_json(
            exclude_none=False
        )

        await self.redis.set(
            key,
            payload,
        )

        return state

    async def delete(
        self,
        *,
        entity_type: str,
        chain: str,
        entity_id: str,
    ) -> None:

        await self.redis.delete(
            self._key(
                entity_type,
                chain,
                entity_id,
            )
        )

    async def ping(self) -> bool:
        try:
            return bool(await self.redis.ping())
        except Exception:
            return False

    async def close(self) -> None:
        await self.redis.aclose()