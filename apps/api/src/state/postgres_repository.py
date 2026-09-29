from __future__ import annotations

from sqlalchemy import (
    select,
)
from sqlalchemy.orm import Session

from database.canonical_state import (
    CanonicalStateRevision,
)


class PostgresStateRepository:
    """
    Durable state-revision repository.

    This repository is append-only by design.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:

        self.session = session

    def append(
        self,
        state,
    ) -> CanonicalStateRevision:

        meta = state.meta

        revision = CanonicalStateRevision(
            entity_type=state.__class__.__name__,
            entity_id=meta.entity_id,
            chain=meta.chain.value,
            version=meta.version,
            state_status=meta.status.value,
            observed_at=meta.observed_at,
            updated_at=meta.updated_at,
            event_id=meta.last_event_id,
            source=meta.source,
            source_type=meta.source_type,
            payload=state.model_dump(
                mode="json"
            ),
        )

        self.session.add(revision)
        self.session.commit()
        self.session.refresh(revision)

        return revision

    def latest(
        self,
        *,
        entity_type: str,
        entity_id: str,
        chain: str,
    ) -> CanonicalStateRevision | None:

        statement = (
            select(CanonicalStateRevision)
            .where(
                CanonicalStateRevision.entity_type
                == entity_type,
                CanonicalStateRevision.entity_id
                == entity_id,
                CanonicalStateRevision.chain
                == chain,
            )
            .order_by(
                CanonicalStateRevision.version.desc()
            )
            .limit(1)
        )

        return self.session.execute(
            statement
        ).scalar_one_or_none()

    def history(
        self,
        *,
        entity_type: str,
        entity_id: str,
        chain: str,
        limit: int = 100,
    ) -> list[CanonicalStateRevision]:

        statement = (
            select(CanonicalStateRevision)
            .where(
                CanonicalStateRevision.entity_type
                == entity_type,
                CanonicalStateRevision.entity_id
                == entity_id,
                CanonicalStateRevision.chain
                == chain,
            )
            .order_by(
                CanonicalStateRevision.version.desc()
            )
            .limit(limit)
        )

        return list(
            self.session.execute(
                statement
            ).scalars()
        )