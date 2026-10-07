from __future__ import annotations

import asyncio
from typing import Any

from sqlalchemy.orm import Session

from database.session import SessionLocal
from models.state_history import StateSnapshot
from state.models import (
    DeveloperState,
    LaunchpadState,
    PoolState,
    TokenState,
    WalletState,
)


class PostgresStateStore:

    async def append_snapshot(
        self,
        *,
        entity_type: str,
        chain: str,
        entity_id: str,
        state: (
            TokenState
            | PoolState
            | WalletState
            | DeveloperState
            | LaunchpadState
        ),
    ) -> None:

        payload = state.model_dump(
            mode="json",
            exclude_none=False,
        )

        meta = state.meta

        await asyncio.to_thread(
            self._insert_snapshot,
            entity_type,
            chain,
            entity_id,
            meta.version,
            meta.status.value,
            meta.source_id,
            meta.last_event_id,
            meta.observed_at,
            meta.processed_at,
            payload,
        )

    @staticmethod
    def _insert_snapshot(
        entity_type: str,
        chain: str,
        entity_id: str,
        version: int,
        status: str,
        source_id: str | None,
        event_id: str | None,
        observed_at: Any,
        processed_at: Any,
        payload: dict[str, Any],
    ) -> None:

        db: Session = SessionLocal()

        try:
            db.add(
                StateSnapshot(
                    entity_type=entity_type,
                    chain=chain,
                    entity_id=entity_id,
                    version=version,
                    status=status,
                    source_id=source_id,
                    event_id=event_id,
                    observed_at=observed_at,
                    processed_at=processed_at,
                    payload=payload,
                )
            )

            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()