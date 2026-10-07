from __future__ import annotations

import asyncio
import importlib.util
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from realtime.models import RealtimeEvent
from state.models import (
    PoolState,
    TokenState,
    WalletState,
)
from state.service import StateService


API_SRC = Path(__file__).resolve().parents[1]

SERVICES_DIR = (
    API_SRC / "services"
)


@contextmanager
def legacy_service_path(
    directory: Path,
):
    """
    Temporarily expose a legacy service directory.

    Several existing SentinelAI engines use imports like:

        from risk_score import RiskScore

    instead of package-relative imports.

    This bridge lets us connect them now without silently
    rewriting their internal implementation.
    """

    path = str(directory)

    inserted = False

    if path not in sys.path:
        sys.path.insert(0, path)
        inserted = True

    try:
        yield
    finally:
        if inserted:
            try:
                sys.path.remove(path)
            except ValueError:
                pass


def load_class(
    *,
    file_path: Path,
    class_name: str,
    module_name: str,
    extra_path: Path | None = None,
):
    if not file_path.exists():
        raise FileNotFoundError(
            str(file_path)
        )

    with legacy_service_path(
        extra_path
        or file_path.parent
    ):
        spec = (
            importlib.util.spec_from_file_location(
                module_name,
                file_path,
            )
        )

        if spec is None or spec.loader is None:
            raise ImportError(
                f"Cannot load {file_path}"
            )

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(module)

        cls = getattr(
            module,
            class_name,
            None,
        )

        if cls is None:
            raise AttributeError(
                f"{class_name} not found in "
                f"{file_path}"
            )

        return cls


class IntelligenceRunner:
    """
    Executes SentinelAI intelligence engines from
    canonical state + observed event data.

    Critical rule:
        Missing data -> UNAVAILABLE
        Never fabricate values merely to satisfy
        an engine's arguments.
    """

    def __init__(
        self,
        state_service: StateService | None = None,
    ) -> None:

        self.state_service = (
            state_service
            or StateService()
        )

    # =========================================================
    # TOKEN STATE
    # =========================================================

    async def get_token_state(
        self,
        event: RealtimeEvent,
    ) -> TokenState | None:

        if event.chain is None:
            return None

        return await self.state_service.get_token(
            event.chain,
            event.entity_id,
        )

    async def get_wallet_state(
        self,
        event: RealtimeEvent,
    ) -> WalletState | None:

        if event.chain is None:
            return None

        return await self.state_service.get_wallet(
            event.chain,
            event.entity_id,
        )

    async def get_pool_state(
        self,
        event: RealtimeEvent,
    ) -> PoolState | None:

        if event.chain is None:
            return None

        return await self.state_service.get_pool(
            event.chain,
            event.entity_id,
        )

    # =========================================================
    # RUG RADAR
    # =========================================================

    async def rug_radar(
        self,
        event: RealtimeEvent,
        token: TokenState,
        features: dict[str, Any],
    ) -> dict[str, Any]:

        required = [
            "mint_authority",
            "freeze_authority",
            "bundled_percent",
            "sniper_percent",
            "insider_percent",
            "lp_burned",
        ]

        missing = [
            key
            for key in required
            if key not in features
            and not hasattr(token, key)
        ]

        if missing:
            return {
                "status": "unavailable",
                "missing_fields": missing,
            }

        token_data = {
            "mint_authority": (
                features.get(
                    "mint_authority",
                    token.mint_authority,
                )
            ),
            "freeze_authority": (
                features.get(
                    "freeze_authority",
                    token.freeze_authority,
                )
            ),
            "bundled_percent": features.get(
                "bundled_percent"
            ),
            "sniper_percent": features.get(
                "sniper_percent"
            ),
            "insider_percent": features.get(
                "insider_percent"
            ),
            "lp_burned": features.get(
                "lp_burned",
                token.lp_burned,
            ),
        }

        scanner_path = (
            SERVICES_DIR
            / "rug-radar"
            / "rug_scanner.py"
        )

        try:
            Scanner = load_class(
                file_path=scanner_path,
                class_name="RugScanner",
                module_name=(
                    "sentinel_rug_scanner_runtime"
                ),
            )

            scanner = Scanner()

            return await asyncio.to_thread(
                scanner.scan,
                token_data,
            )

        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
            }

    # =========================================================
    # MARKET INTELLIGENCE
    # =========================================================

    async def market_intelligence(
        self,
        features: dict[str, Any],
    ) -> dict[str, Any]:

        required = [
            "smart_wallets",
            "whale_inflow",
            "fresh_wallet_percent",
            "inflow",
            "outflow",
            "holder_growth",
        ]

        missing = [
            key
            for key in required
            if key not in features
        ]

        if missing:
            return {
                "status": "unavailable",
                "missing_fields": missing,
            }

        engine_path = (
            SERVICES_DIR
            / "market_intelligence"
            / "intelligence_engine.py"
        )

        try:
            Engine = load_class(
                file_path=engine_path,
                class_name="IntelligenceEngine",
                module_name=(
                    "sentinel_market_intelligence_runtime"
                ),
            )

            engine = Engine()

            return await asyncio.to_thread(
                engine.analyze,
                {
                    key: features[key]
                    for key in required
                },
            )

        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
            }

    # =========================================================
    # J7
    # =========================================================

    async def j7tracker(
        self,
        features: dict[str, Any],
    ) -> dict[str, Any]:

        required = [
            "follows",
            "deploys",
            "mentions",
            "narrative",
        ]

        missing = [
            key
            for key in required
            if key not in features
        ]

        if missing:
            return {
                "status": "unavailable",
                "missing_fields": missing,
            }

        engine_path = (
            SERVICES_DIR
            / "j7tracker-engine"
            / "intelligence.py"
        )

        try:
            Engine = load_class(
                file_path=engine_path,
                class_name="J7Intelligence",
                module_name=(
                    "sentinel_j7_runtime"
                ),
            )

            engine = Engine()

            return await asyncio.to_thread(
                engine.analyze,
                {
                    key: features[key]
                    for key in required
                },
            )

        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
            }

    # =========================================================
    # NARRATIVE
    # =========================================================

    async def narrative(
        self,
        token: TokenState,
    ) -> dict[str, Any]:

        token_name = (
            token.name
            or token.symbol
        )

        if not token_name:
            return {
                "status": "unavailable",
                "missing_fields": [
                    "name_or_symbol"
                ],
            }

        classifier_path = (
            SERVICES_DIR
            / "narrative-engine"
            / "meta_classifier.py"
        )

        try:
            Classifier = load_class(
                file_path=classifier_path,
                class_name="MetaClassifier",
                module_name=(
                    "sentinel_narrative_runtime"
                ),
            )

            classifier = Classifier()

            narrative = await asyncio.to_thread(
                classifier.classify,
                token_name,
            )

            return {
                "status": "derived",
                "narrative": narrative,
            }

        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
            }

    # =========================================================
    # WALLET DNA
    # =========================================================

    async def wallet_dna(
        self,
        event: RealtimeEvent,
    ) -> dict[str, Any]:

        """
        Feed real wallet transfer relationships into the
        existing Wallet DNA GraphBuilder.

        No synthetic wallet labels are generated.
        """

        payload = event.payload

        source_address = payload.get(
            "from_address"
        )

        target_address = payload.get(
            "to_address"
        )

        if not source_address or not target_address:
            return {
                "status": "unavailable",
                "missing_fields": [
                    "from_address",
                    "to_address",
                ],
            }

        graph_path = (
            SERVICES_DIR
            / "wallet_dna"
            / "graph"
            / "graph_builder.py"
        )

        try:
            GraphBuilder = load_class(
                file_path=graph_path,
                class_name="GraphBuilder",
                module_name=(
                    "sentinel_wallet_graph_runtime"
                ),
            )

            # One graph per process for realtime updates.
            graph = self._wallet_graph(
                GraphBuilder
            )

            source = self._ensure_wallet(
                graph,
                source_address,
            )

            target = self._ensure_wallet(
                graph,
                target_address,
            )

            amount_sol = float(
                payload.get(
                    "amount_sol",
                    0,
                )
            )

            signature = (
                event.chain_position
                .transaction_signature
                if event.chain_position
                else None
            )

            graph.add_transfer(
                source,
                target,
                amount_sol,
                tx_signature=signature,
            )

            return {
                "status": "derived",
                "source_wallet": source_address,
                "target_wallet": target_address,
                "amount_sol": amount_sol,
                "graph_summary": graph.summary(),
            }

        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
            }

    _wallet_graph_instance: Any = None

    def _wallet_graph(
        self,
        GraphBuilder,
    ):
        if (
            self._wallet_graph_instance
            is None
        ):
            self._wallet_graph_instance = (
                GraphBuilder()
            )

        return self._wallet_graph_instance

    @staticmethod
    def _ensure_wallet(
        graph,
        address: str,
    ) -> str:

        if not graph.has_wallet(address):
            graph.add_wallet(address)

        node_id = graph.get_node_id(
            address
        )

        if node_id is None:
            raise RuntimeError(
                f"Wallet graph node missing: {address}"
            )

        return node_id

    # =========================================================
    # SCORING
    # =========================================================

    async def scoring(
        self,
        features: dict[str, Any],
    ) -> dict[str, Any]:

        required = [
            "successful_launches",
            "rugs",
            "avg_ath",
            "wallet_age_days",
            "smart_money",
            "whales",
            "insiders",
            "volume",
            "buyers",
            "repeat_wallets",
            "telegram_members",
            "twitter_mentions",
            "j7_signals",
            "engagement_rate",
            "narrative_rank",
            "narrative_growth",
            "narrative_volume_growth",
            "mint_enabled",
            "freeze_enabled",
            "dev_percent",
            "bundled_wallets",
            "market_cap",
            "age_minutes",
            "score_boost",
        ]

        missing = [
            key
            for key in required
            if key not in features
            or features[key] is None
        ]

        if missing:
            return {
                "status": "unavailable",
                "missing_fields": missing,
            }

        engine_path = (
            SERVICES_DIR
            / "scoring-engine"
            / "sentinel_score.py"
        )

        try:
            Engine = load_class(
                file_path=engine_path,
                class_name="SentinelScoreEngine",
                module_name=(
                    "sentinel_scoring_runtime"
                ),
            )

            engine = Engine()

            result = await asyncio.to_thread(
                engine.calculate,
                features,
            )

            return {
                "status": "model_derived",
                "model_name": "SentinelScoreEngine",
                "model_version": "legacy-1.0",
                "result": result,
            }

        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
            }