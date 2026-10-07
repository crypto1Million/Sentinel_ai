from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis

from config.settings import get_settings


class IntelligenceFeatureStore:
    """
    Hot feature cache for realtime intelligence.

    StateService:
        canonical blockchain/entity state

    IntelligenceFeatureStore:
        latest derived intelligence/features used by engines

    Historical events:
        remain in Redis Streams / durable persistence
    """

    PREFIX = "sentinel:intelligence:features"

    def __init__(
        self,
        redis_client: Redis | None = None,
    ) -> None:
        settings = get_settings()

        if redis_client is not None:
            self.redis = redis_client
            self._owns_redis = False
        else:
            password = getattr(
                settings,
                "REDIS_PASSWORD",
                "",
            )

            if password:
                url = (
                    f"redis://:{password}@"
                    f"{settings.REDIS_HOST}:"
                    f"{settings.REDIS_PORT}/"
                    f"{settings.REDIS_DB}"
                )
            else:
                url = (
                    f"redis://"
                    f"{settings.REDIS_HOST}:"
                    f"{settings.REDIS_PORT}/"
                    f"{settings.REDIS_DB}"
                )

            self.redis = Redis.from_url(
                url,
                decode_responses=True,
            )

            self._owns_redis = True

    def _key(
        self,
        chain: str,
        token: str,
    ) -> str:
        return (
            f"{self.PREFIX}:"
            f"{chain}:"
            f"{token}"
        )

    async def get(
        self,
        chain: str,
        token: str,
    ) -> dict[str, Any]:
        raw = await self.redis.get(
            self._key(chain, token)
        )

        if raw is None:
            return {}

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    async def merge(
        self,
        *,
        chain: str,
        token: str,
        source: str,
        values: dict[str, Any],
        event_id: str,
    ) -> dict[str, Any]:

        current = await self.get(
            chain,
            token,
        )

        sources = current.get(
            "_sources",
            {},
        )

        source_record = sources.get(
            source,
            {},
        )

        source_record.update(
            {
                "event_id": event_id,
                "values": values,
            }
        )

        sources[source] = source_record

        # Flat merged feature map.
        for key, value in values.items():
            current[key] = value

        current["_sources"] = sources

        await self.redis.set(
            self._key(chain, token),
            json.dumps(
                current,
                default=str,
                separators=(",", ":"),
            ),
        )

        return current

    async def set_status(
        self,
        *,
        chain: str,
        token: str,
        engine: str,
        status: str,
        missing_fields: list[str] | None = None,
    ) -> None:

        current = await self.get(
            chain,
            token,
        )

        statuses = current.get(
            "_engine_status",
            {},
        )

        statuses[engine] = {
            "status": status,
            "missing_fields": (
                missing_fields or []
            ),
        }

        current["_engine_status"] = statuses

        await self.redis.set(
            self._key(chain, token),
            json.dumps(
                current,
                default=str,
                separators=(",", ":"),
            ),
        )

    async def close(self) -> None:
        if self._owns_redis:
            await self.redis.aclose()


_store: IntelligenceFeatureStore | None = None


def get_intelligence_feature_store() -> IntelligenceFeatureStore:
    global _store

    if _store is None:
        _store = IntelligenceFeatureStore()

    return _store