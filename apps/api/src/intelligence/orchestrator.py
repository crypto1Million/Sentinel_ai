from __future__ import annotations

import logging
from typing import Any

from intelligence.feature_store import (
    IntelligenceFeatureStore,
    get_intelligence_feature_store,
)
from intelligence.runner import IntelligenceRunner
from realtime.models import RealtimeEvent
from realtime.publisher import publish_event
from state.models import TokenState
from state.service import StateService


logger = logging.getLogger(
    "sentinel.intelligence"
)


RAW_EVENTS = {
    "token.updated",
    "wallet.updated",
    "pool.updated",
    "launchpad.detected",
    "chain.observed",
}


class IntelligenceOrchestrator:
    """
    Event-driven SentinelAI intelligence layer.

    Raw/state event
        ↓
    State lookup
        ↓
    Feature merge
        ↓
    Appropriate intelligence engines
        ↓
    Derived events
        ↓
    Feature cache
        ↓
    Score recomputation when enough
    evidence exists.
    """

    def __init__(
        self,
        state_service: StateService | None = None,
        feature_store: IntelligenceFeatureStore | None = None,
    ) -> None:

        self.state_service = (
            state_service
            or StateService()
        )

        self.features = (
            feature_store
            or get_intelligence_feature_store()
        )

        self.runner = IntelligenceRunner(
            self.state_service
        )

    async def handle(
        self,
        event: RealtimeEvent,
    ) -> None:

        if event.event_type not in RAW_EVENTS:
            return

        if event.chain is None:
            return

        logger.debug(
            "Processing intelligence event %s",
            event.event_id,
        )

        if event.entity_type == "wallet":
            await self._handle_wallet(
                event
            )
            return

        if event.entity_type == "token":
            await self._handle_token(
                event
            )
            return

        if event.entity_type == "pool":
            await self._handle_pool(
                event
            )
            return

        # Launchpad/chain events may reference a token.
        token_mint = (
            event.related_entity_id
            or event.payload.get("token_mint")
        )

        if token_mint:
            token = (
                await self.state_service.get_token(
                    event.chain,
                    token_mint,
                )
            )

            if token:
                await self._handle_token(
                    event,
                    token_override=token,
                )

    # =========================================================
    # TOKEN
    # =========================================================

    async def _handle_token(
        self,
        event: RealtimeEvent,
        token_override: TokenState | None = None,
    ) -> None:

        token = token_override

        if token is None:
            token = (
                await self.state_service.get_token(
                    event.chain,
                    event.entity_id,
                )
            )

        if token is None:
            logger.debug(
                "Token state unavailable for %s",
                event.entity_id,
            )
            return

        current = await self.features.merge(
            chain=event.chain,
            token=token.mint,
            source="state",
            values=token.model_dump(
                mode="json"
            ),
            event_id=event.event_id,
        )

        # Include freshly observed event payload.
        current = await self.features.merge(
            chain=event.chain,
            token=token.mint,
            source="event",
            values=event.payload,
            event_id=event.event_id,
        )

        await self._run_token_engines(
            event=event,
            token=token,
            features=current,
        )

    # =========================================================
    # POOL
    # =========================================================

    async def _handle_pool(
        self,
        event: RealtimeEvent,
    ) -> None:

        pool = (
            await self.state_service.get_pool(
                event.chain,
                event.entity_id,
            )
        )

        token_mint = (
            event.payload.get("token_mint")
            or event.related_entity_id
        )

        if pool is None or not token_mint:
            return

        current = await self.features.merge(
            chain=event.chain,
            token=token_mint,
            source="pool",
            values=pool.model_dump(
                mode="json"
            ),
            event_id=event.event_id,
        )

        await self._run_market_engine(
            event,
            token_mint,
            current,
        )

        await self._run_score_engine(
            event,
            token_mint,
            current,
        )

    # =========================================================
    # WALLET
    # =========================================================

    async def _handle_wallet(
        self,
        event: RealtimeEvent,
    ) -> None:

        wallet = (
            await self.state_service.get_wallet(
                event.chain,
                event.entity_id,
            )
        )

        if wallet is not None:
            await self.features.merge(
                chain=event.chain,
                token=(
                    event.payload.get(
                        "token_mint"
                    )
                    or "__wallet__"
                ),
                source="wallet",
                values=wallet.model_dump(
                    mode="json"
                ),
                event_id=event.event_id,
            )

        result = await self.runner.wallet_dna(
            event
        )

        await self.features.set_status(
            chain=event.chain,
            token=(
                event.payload.get(
                    "token_mint"
                )
                or "__wallet__"
            ),
            engine="wallet_dna",
            status=result.get(
                "status",
                "unknown",
            ),
            missing_fields=result.get(
                "missing_fields",
                [],
            ),
        )

        await publish_event(
            event_type="wallet_dna.updated",
            entity_type="wallet",
            entity_id=event.entity_id,
            chain=event.chain,
            source="wallet_dna",
            source_id=event.event_id,
            status=result.get(
                "status",
                "derived",
            ),
            payload={
                "wallet": event.entity_id,
                **result,
            },
        )

        # Wallet events can also feed J7 if the upstream
        # event contains real social/J7 fields.
        token_mint = event.payload.get(
            "token_mint"
        )

        if token_mint:
            current = await self.features.merge(
                chain=event.chain,
                token=token_mint,
                source="wallet_event",
                values=event.payload,
                event_id=event.event_id,
            )

            await self._run_j7_engine(
                event,
                token_mint,
                current,
            )

            await self._run_score_engine(
                event,
                token_mint,
                current,
            )

    # =========================================================
    # ENGINE FAN-OUT
    # =========================================================

    async def _run_token_engines(
        self,
        *,
        event: RealtimeEvent,
        token: TokenState,
        features: dict[str, Any],
    ) -> None:

        await self._run_rug_engine(
            event,
            token,
            features,
        )

        await self._run_market_engine(
            event,
            token.mint,
            features,
        )

        await self._run_j7_engine(
            event,
            token.mint,
            features,
        )

        await self._run_narrative_engine(
            event,
            token,
        )

        await self._run_score_engine(
            event,
            token.mint,
            features,
        )

    # =========================================================
    # RUG
    # =========================================================

    async def _run_rug_engine(
        self,
        event: RealtimeEvent,
        token: TokenState,
        features: dict[str, Any],
    ) -> None:

        result = await self.runner.rug_radar(
            event,
            token,
            features,
        )

        status = result.get(
            "status",
            "derived",
        )

        await self.features.set_status(
            chain=event.chain,
            token=token.mint,
            engine="rug_radar",
            status=status,
            missing_fields=result.get(
                "missing_fields",
                [],
            ),
        )

        if status == "error":
            logger.exception(
                "Rug Radar failed for %s: %s",
                token.mint,
                result.get("error"),
            )

        await publish_event(
            event_type="rug.updated",
            entity_type="token",
            entity_id=token.mint,
            chain=event.chain,
            source="rug_radar",
            source_id=event.event_id,
            status=status,
            payload={
                "token": token.mint,
                **result,
            },
        )

        await self.features.merge(
            chain=event.chain,
            token=token.mint,
            source="rug_radar",
            values=result,
            event_id=event.event_id,
        )

    # =========================================================
    # MARKET INTELLIGENCE
    # =========================================================

    async def _run_market_engine(
        self,
        event: RealtimeEvent,
        token_mint: str,
        features: dict[str, Any],
    ) -> None:

        result = await self.runner.market_intelligence(
            features
        )

        status = result.get(
            "status",
            "derived",
        )

        await self.features.set_status(
            chain=event.chain,
            token=token_mint,
            engine="market_intelligence",
            status=status,
            missing_fields=result.get(
                "missing_fields",
                [],
            ),
        )

        await self.features.merge(
            chain=event.chain,
            token=token_mint,
            source="market_intelligence",
            values=result,
            event_id=event.event_id,
        )

        if status == "unavailable":
            return

        await publish_event(
            event_type="market_intelligence.updated",
            entity_type="token",
            entity_id=token_mint,
            chain=event.chain,
            source="market_intelligence",
            source_id=event.event_id,
            status=status,
            payload={
                "token": token_mint,
                **result,
            },
        )

    # =========================================================
    # J7
    # =========================================================

    async def _run_j7_engine(
        self,
        event: RealtimeEvent,
        token_mint: str,
        features: dict[str, Any],
    ) -> None:

        result = await self.runner.j7tracker(
            features
        )

        status = result.get(
            "status",
            "derived",
        )

        await self.features.set_status(
            chain=event.chain,
            token=token_mint,
            engine="j7tracker",
            status=status,
            missing_fields=result.get(
                "missing_fields",
                [],
            ),
        )

        await self.features.merge(
            chain=event.chain,
            token=token_mint,
            source="j7tracker",
            values=result,
            event_id=event.event_id,
        )

        if status == "unavailable":
            return

        await publish_event(
            event_type="j7.updated",
            entity_type="token",
            entity_id=token_mint,
            chain=event.chain,
            source="j7tracker",
            source_id=event.event_id,
            status=status,
            payload={
                "token": token_mint,
                **result,
            },
        )

    # =========================================================
    # NARRATIVE
    # =========================================================

    async def _run_narrative_engine(
        self,
        event: RealtimeEvent,
        token: TokenState,
    ) -> None:

        result = await self.runner.narrative(
            token
        )

        status = result.get(
            "status",
            "derived",
        )

        await self.features.set_status(
            chain=event.chain,
            token=token.mint,
            engine="narrative",
            status=status,
            missing_fields=result.get(
                "missing_fields",
                [],
            ),
        )

        await self.features.merge(
            chain=event.chain,
            token=token.mint,
            source="narrative",
            values=result,
            event_id=event.event_id,
        )

        if status == "unavailable":
            return

        await publish_event(
            event_type="narrative.updated",
            entity_type="token",
            entity_id=token.mint,
            chain=event.chain,
            source="narrative_engine",
            source_id=event.event_id,
            status=status,
            payload={
                "token": token.mint,
                **result,
            },
        )

    # =========================================================
    # SCORE
    # =========================================================

    async def _run_score_engine(
        self,
        event: RealtimeEvent,
        token_mint: str,
        features: dict[str, Any],
    ) -> None:

        result = await self.runner.scoring(
            features
        )

        status = result.get(
            "status",
            "model_derived",
        )

        await self.features.set_status(
            chain=event.chain,
            token=token_mint,
            engine="scoring",
            status=status,
            missing_fields=result.get(
                "missing_fields",
                [],
            ),
        )

        if status != "model_derived":
            return

        await self.features.merge(
            chain=event.chain,
            token=token_mint,
            source="scoring",
            values=result,
            event_id=event.event_id,
        )

        await publish_event(
            event_type="score.updated",
            entity_type="token",
            entity_id=token_mint,
            chain=event.chain,
            source="sentinel_score",
            source_id=event.event_id,
            status="model_derived",
            payload={
                "token": token_mint,
                "model_version": "legacy-1.0",
                **result,
            },
        )