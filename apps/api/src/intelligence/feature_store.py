from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping

from redis.asyncio import Redis

from config.settings import get_settings


SCORING_GROUPS = {
    "dev_history",
    "developer_history",
    "dev_wallet",
    "developer_wallet",
    "narrative",
    "initial_flow",
    "initial_money_flow",
    "funding",
    "funding_provenance",
    "dev_social",
    "developer_social",
    "contract_risk",
    "rug_radar",
}


def _iso(value: datetime | str | None) -> str:
    if isinstance(value, datetime):
        parsed = value

    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except ValueError:
            parsed = datetime.now(timezone.utc)

    else:
        parsed = datetime.now(timezone.utc)

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc).isoformat()


def _deep_merge_with_meta(
    current: Mapping[str, Any] | None,
    incoming: Mapping[str, Any],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    """Merge nested scoring features without losing existing fields."""

    merged = dict(current or {})

    previous_field_meta = merged.get("_field_meta")

    field_meta = (
        dict(previous_field_meta)
        if isinstance(previous_field_meta, Mapping)
        else {}
    )

    for key, value in incoming.items():

        if key in {"_meta", "_field_meta"}:
            continue

        if isinstance(value, Mapping):
            previous = merged.get(key)

            previous_mapping = (
                previous
                if isinstance(previous, Mapping)
                else {}
            )

            merged[key] = _deep_merge_with_meta(
                previous_mapping,
                value,
                metadata,
            )

        else:
            merged[key] = value

            # Only this field receives the new timestamp.
            # Other fields retain their original timestamps.
            field_meta[key] = dict(metadata)

    previous_meta = merged.get("_meta")

    previous_meta = (
        dict(previous_meta)
        if isinstance(previous_meta, Mapping)
        else {}
    )

    merged["_meta"] = {
        **previous_meta,
        **metadata,
    }

    merged["_field_meta"] = field_meta

    return merged


class IntelligenceFeatureStore:
    """Redis cache for canonical state and derived intelligence features."""

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
            value = json.loads(raw)

            return (
                value
                if isinstance(value, dict)
                else {}
            )

        except (json.JSONDecodeError, TypeError):
            return {}

    async def merge(
        self,
        *,
        chain: str,
        token: str,
        source: str,
        values: dict[str, Any],
        event_id: str,
        observed_at: datetime | str | None = None,
        source_quality: float = 0.7,
    ) -> dict[str, Any]:

        current = await self.get(
            chain,
            token,
        )

        now = datetime.now(timezone.utc).isoformat()

        try:
            quality = float(source_quality)

        except (TypeError, ValueError):
            quality = 0.7

        if quality > 1.0:
            quality /= 100.0

        quality = max(
            0.1,
            min(1.0, quality),
        )

        metadata = {
            "source": source,
            "event_id": event_id,
            "observed_at": _iso(observed_at),
            "updated_at": now,
            "source_quality": quality,
        }

        sources = current.get("_sources")

        sources = (
            dict(sources)
            if isinstance(sources, Mapping)
            else {}
        )

        sources[source] = {
            "event_id": event_id,
            "observed_at": metadata["observed_at"],
            "updated_at": now,
            "fields": sorted(values.keys()),
        }

        for key, value in values.items():

            if (
                key in SCORING_GROUPS
                and isinstance(value, Mapping)
            ):
                previous = current.get(key)

                previous = (
                    previous
                    if isinstance(previous, Mapping)
                    else {}
                )

                current[key] = _deep_merge_with_meta(
                    previous,
                    value,
                    metadata,
                )

            else:
                # Keep the old flat feature map behaviour for
                # existing engines and non-scoring features.
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

        statuses = current.get("_engine_status")

        statuses = (
            dict(statuses)
            if isinstance(statuses, Mapping)
            else {}
        )

        statuses[engine] = {
            "status": status,
            "missing_fields": missing_fields or [],
            "updated_at": datetime.now(
                timezone.utc
            ).isoformat(),
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