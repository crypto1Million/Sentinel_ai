from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Mapping


MODEL_NAME = "SentinelScoreEngine"
MODEL_VERSION = "2.0.0"

# Preserve the six original pillars and their weights.
PILLAR_WEIGHTS: dict[str, float] = {
    "developer_history": 20.0,
    "developer_wallet": 20.0,
    "narrative": 20.0,
    "initial_money_flow": 20.0,
    "funding_provenance": 10.0,
    "developer_social": 10.0,
}

FLOW_WINDOW_WEIGHTS: dict[str, float] = {
    "1m": 0.10,
    "5m": 0.25,
    "15m": 0.35,
    "1h": 0.30,
}

GROUP_MAX_AGE_SECONDS = {
    "developer_history": 7 * 24 * 60 * 60,
    "developer_wallet": 24 * 60 * 60,
    "narrative": 10 * 60,
    "funding_provenance": 7 * 24 * 60 * 60,
    "developer_social": 6 * 60 * 60,
}

FLOW_MAX_AGE_SECONDS = {
    "1m": 90,
    "5m": 180,
    "15m": 600,
    "1h": 1800,
}

# Initial category priors, not empirically calibrated probabilities.
NARRATIVE_CATEGORY_SCORES = {
    "major_x_tweet": 76.0,
    "viral_animal": 72.0,
    "meme_template": 72.0,
    "cultural_trend": 70.0,
    "ai_innovation": 76.0,
    "product_concept": 70.0,
    "terminal_meta": 62.0,
    "world_event": 70.0,
    "unknown": 50.0,
}


class SentinelScoreEngine:
    """Evidence-aware SentinelScore potential and independent Rug Risk."""

    MIN_POTENTIAL_COVERAGE = 60.0
    MIN_RUG_COVERAGE = 50.0

    def calculate(
        self,
        features: Mapping[str, Any] | None,
        *,
        now: datetime | None = None,
    ) -> dict[str, Any]:

        data = dict(features or {})
        now = now or datetime.now(timezone.utc)

        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)

        pillars = {
            "developer_history": self._developer_history(
                self._group(data, "dev_history", "developer_history"),
                now,
            ),
            "developer_wallet": self._developer_wallet(
                self._group(data, "dev_wallet", "developer_wallet"),
                now,
            ),
            "narrative": self._narrative(
                self._group(data, "narrative"),
                now,
            ),
            "initial_money_flow": self._initial_money_flow(
                self._group(data, "initial_flow", "initial_money_flow"),
                now,
            ),
            "funding_provenance": self._funding(
                self._group(data, "funding", "funding_provenance"),
                now,
            ),
            "developer_social": self._developer_social(
                self._group(data, "dev_social", "developer_social"),
                now,
            ),
        }

        potential, coverage, confidence = self._combine_pillars(pillars)
        rug = self._rug_risk(data, now)

        potential_status = (
            "scored" if potential is not None else "insufficient_data"
        )

        return {
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION,

            "potential_score": self._round(potential),
            "potential_status": potential_status,
            "potential_grade": (
                self._grade(potential)
                if potential is not None
                else None
            ),

            "rug_risk_score": self._round(rug["score"]),
            "rug_risk_status": rug["status"],
            "rug_risk_coverage_pct": self._round(
                rug["coverage_pct"]
            ),
            "rug_risk_confidence_pct": self._round(
                rug["confidence_pct"]
            ),

            "data_coverage_pct": self._round(coverage),
            "confidence_pct": self._round(confidence),

            "pillars": pillars,
            "risk_flags": rug["risk_flags"],
            "risk_components": rug["components"],
            "rug_hard_veto": rug["hard_veto"],

            "interpretation": (
                "Potential is a relative evidence score, not a profit "
                "probability or buy recommendation. Rug Risk is assessed "
                "independently."
            ),
            "scored_at": now.isoformat(),
        }

    # ==============================================================
    # 1. DEVELOPER HISTORY
    # ==============================================================

    def _developer_history(
        self,
        group: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:

        total = self._number(
            group.get("total_launches"),
            minimum=0,
        )
        clean = self._number(
            group.get("successful_migrations"),
            minimum=0,
        )
        rugs = self._number(
            group.get("rugged_tokens"),
            minimum=0,
        )

        verified = group.get("outcomes_verified")

        score = None
        coverage = 0.0
        sample_quality = 0.0
        notes: list[str] = []

        if (
            total is not None
            and clean is not None
            and rugs is not None
        ):
            outcomes = clean + rugs

            if (
                outcomes > 0
                and clean <= total
                and rugs <= total
                and outcomes <= total
            ):
                # Beta(2,2) prior prevents tiny samples from producing
                # extreme scores. The prior starts at neutral 50.
                score = (
                    100.0
                    * (clean + 2.0)
                    / (outcomes + 4.0)
                )

                coverage = 1.0
                sample_quality = min(
                    1.0,
                    math.sqrt(outcomes / 10.0),
                )

                if verified is not True:
                    notes.append(
                        "Outcome verification was not explicitly confirmed"
                    )

            elif outcomes == 0:
                notes.append(
                    "No matured outcomes yet; launch count alone "
                    "is not a success signal"
                )

            else:
                notes.append(
                    "Inconsistent developer outcome counts; verify source data"
                )

        quality = self._group_quality(
            group,
            now,
            GROUP_MAX_AGE_SECONDS["developer_history"],
        )

        if verified is True:
            quality = min(1.0, quality * 1.08)

        return self._pillar(
            score,
            coverage,
            quality * sample_quality,
            notes,
            details={
                "total_launches": total,
                "successful_migrations": clean,
                "rugged_tokens": rugs,
                "matured_outcomes": (
                    clean + rugs
                    if clean is not None and rugs is not None
                    else None
                ),
            },
        )

    # ==============================================================
    # 2. DEVELOPER WALLET INTELLIGENCE
    # ==============================================================

    def _developer_wallet(
        self,
        group: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:

        analyzed = self._number(
            group.get("linked_wallets_analyzed"),
            minimum=0,
        )
        clean = self._number(
            group.get("clean_migrations"),
            minimum=0,
        )
        rugs = self._number(
            group.get("linked_rugged_tokens"),
            minimum=0,
        )

        is_new = group.get("new_funded_wallet")

        score = None
        coverage = 0.0
        sample_quality = 0.0
        notes: list[str] = []

        if (
            analyzed is not None
            and clean is not None
            and rugs is not None
        ):
            outcomes = clean + rugs

            if analyzed > 0 and outcomes > 0:
                score = (
                    100.0
                    * (clean + 2.0)
                    / (outcomes + 4.0)
                )

                coverage = 1.0
                sample_quality = min(
                    1.0,
                    math.sqrt(outcomes / 8.0),
                )

            elif analyzed == 0 or outcomes == 0:
                notes.append(
                    "Wallet has no verified linked-token outcome history"
                )

        # New funded wallet is not automatically suspicious.
        # It remains unproven until its linked history is established.
        if is_new is True and coverage == 0:
            notes.append(
                "Newly funded wallet is unproven, not automatically malicious"
            )

        quality = self._group_quality(
            group,
            now,
            GROUP_MAX_AGE_SECONDS["developer_wallet"],
        )

        if is_new is True and coverage == 0:
            quality *= 0.8

        return self._pillar(
            score,
            coverage,
            quality * sample_quality,
            notes,
            details={
                "linked_wallets_analyzed": analyzed,
                "clean_migrations": clean,
                "linked_rugged_tokens": rugs,
                "new_funded_wallet": (
                    is_new if isinstance(is_new, bool) else None
                ),
            },
        )

    # ==============================================================
    # 3. NARRATIVE INTELLIGENCE
    # ==============================================================

    def _narrative(
        self,
        group: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:

        category = self._normalize_category(
            group.get("category")
        )

        metrics = [
            (
                NARRATIVE_CATEGORY_SCORES.get(category)
                if category else None,
                10.0,
            ),
            (
                self._growth_score(
                    group.get("mention_growth_1h_pct")
                ),
                20.0,
            ),
            (
                self._growth_score(
                    group.get("mention_growth_24h_pct")
                ),
                10.0,
            ),
            (
                self._count_score(
                    group.get("unique_accounts_1h"),
                    100,
                ),
                20.0,
            ),
            (
                self._growth_score(
                    group.get("volume_growth_1h_pct")
                ),
                20.0,
            ),
            (
                self._inverse_pct(
                    group.get("saturation_pct")
                ),
                10.0,
            ),
            (
                self._pct(
                    group.get("source_credibility_pct")
                ),
                10.0,
            ),
        ]

        score, coverage = self._weighted(metrics)

        quality = self._group_quality(
            group,
            now,
            GROUP_MAX_AGE_SECONDS["narrative"],
        )

        notes = []

        if category is None:
            notes.append(
                "Narrative category is missing or unrecognized"
            )

        if coverage < 1:
            notes.append(
                "Narrative momentum is only partially observed"
            )

        return self._pillar(
            score if coverage >= 0.4 else None,
            coverage,
            quality,
            notes,
            details={"category": category},
        )

    # ==============================================================
    # 4. INITIAL MONEY FLOW
    # ==============================================================

    def _initial_money_flow(
        self,
        group: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:

        windows = group.get("windows")

        if not isinstance(windows, Mapping):
            windows = {}

        scored_windows = []
        window_coverage = 0.0
        notes: list[str] = []

        for timeframe, tf_weight in FLOW_WINDOW_WEIGHTS.items():
            window = windows.get(timeframe)

            if not isinstance(window, Mapping):
                continue

            result = self._score_flow_window(
                dict(window),
                now,
                timeframe,
                group,
            )

            if result["score"] is None:
                continue

            effective_weight = tf_weight * result["coverage"]

            scored_windows.append(
                (
                    result["score"],
                    effective_weight,
                    result["confidence"],
                    timeframe,
                )
            )

            window_coverage += effective_weight
            notes.extend(result["risk_notes"])

        denominator = sum(
            item[1] for item in scored_windows
        )

        score = (
            sum(item[0] * item[1] for item in scored_windows)
            / denominator
            if denominator > 0
            else None
        )

        confidence = (
            sum(item[2] * item[1] for item in scored_windows)
            / denominator
            if denominator > 0
            else 0.0
        )

        if len(scored_windows) < 2:
            notes.append(
                "Fewer than two flow windows are available; "
                "short-term flow is less reliable"
            )
            confidence *= 0.75

        return self._pillar(
            score if window_coverage >= 0.35 else None,
            min(1.0, window_coverage),
            confidence,
            notes,
            details={
                "available_windows": [
                    item[3] for item in scored_windows
                ],
                "window_weights": FLOW_WINDOW_WEIGHTS,
            },
        )

    def _score_flow_window(
        self,
        window: dict[str, Any],
        now: datetime,
        timeframe: str,
        parent: dict[str, Any],
    ) -> dict[str, Any]:

        buy = self._number(
            window.get("buy_volume_usd"),
            minimum=0,
        )
        sell = self._number(
            window.get("sell_volume_usd"),
            minimum=0,
        )
        liquidity = self._number(
            window.get("liquidity_usd"),
            minimum=0,
        )
        buyers = self._number(
            window.get("unique_buyers"),
            minimum=0,
        )
        sellers = self._number(
            window.get("unique_sellers"),
            minimum=0,
        )
        smart_net = self._number(
            window.get("smart_money_net_flow_usd"),
            allow_negative=True,
        )
        concentration = self._number(
            window.get("top_buyer_concentration_pct"),
            minimum=0,
            maximum=100,
        )
        dev_sell = self._number(
            window.get("developer_sell_pct"),
            minimum=0,
            maximum=100,
        )

        buy_pressure = None
        normalized_net = None
        buyer_breadth = None
        smart_flow = None

        if buy is not None and sell is not None:
            total = buy + sell

            buy_pressure = (
                50.0
                if total == 0
                else 100.0 * buy / total
            )

            if liquidity is not None and liquidity > 0:
                normalized_net = (
                    50.0
                    + 50.0
                    * math.tanh(
                        ((buy - sell) / liquidity) * 4.0
                    )
                )

        if buyers is not None and sellers is not None:
            total_wallets = buyers + sellers

            buyer_breadth = (
                35.0
                if total_wallets == 0
                else 100.0 * buyers / total_wallets
            )

        if smart_net is not None and liquidity is not None and liquidity > 0:
            smart_flow = (
                50.0
                + 50.0
                * math.tanh(
                    (smart_net / liquidity) * 4.0
                )
            )

        score, coverage = self._weighted([
            (buy_pressure, 25.0),
            (normalized_net, 20.0),
            (buyer_breadth, 15.0),
            (smart_flow, 15.0),
            (self._inverse_pct(concentration), 10.0),
            (self._inverse_pct(dev_sell), 15.0),
        ])

        confidence = self._mapping_quality(
            window if window.get("_meta") else parent,
            now,
            FLOW_MAX_AGE_SECONDS[timeframe],
        )

        risk_notes: list[str] = []

        if dev_sell is not None and dev_sell >= 15.0:
            risk_notes.append(
                f"Developer sold {dev_sell:.1f}% in the {timeframe} window"
            )

        if concentration is not None and concentration >= 50.0:
            risk_notes.append(
                f"Top-buyer concentration is {concentration:.1f}% "
                f"in the {timeframe} window"
            )

        return {
            "score": score if coverage >= 0.4 else None,
            "coverage": coverage,
            "confidence": confidence,
            "risk_notes": risk_notes,
        }

    # ==============================================================
    # 5. FUNDING PROVENANCE
    # ==============================================================

    def _funding(
        self,
        group: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:

        source_type = group.get("source_type")
        verified = group.get("verified")
        hops = self._number(
            group.get("funding_hops"),
            minimum=0,
        )

        normalized = (
            str(source_type).strip().lower()
            if source_type is not None
            else ""
        )

        source_scores = {
            "known_clean_deployer": 90.0,
            "verified_clean_source": 90.0,
            "exchange": 58.0,
            "cex": 58.0,
            "fresh_wallet": 50.0,
            "new_wallet": 50.0,
            "unknown": 48.0,
            "unverified": 45.0,
            "linked_insider_wallet": 15.0,
            "linked_rug_wallet": 0.0,
        }

        source_score = source_scores.get(normalized)

        hop_score = None
        if hops is not None:
            hop_score = max(
                40.0,
                100.0 - max(0.0, hops - 2.0) * 12.0,
            )

        score, coverage = self._weighted([
            (source_score, 80.0),
            (hop_score, 20.0),
        ])

        quality = self._group_quality(
            group,
            now,
            GROUP_MAX_AGE_SECONDS["funding_provenance"],
        )

        if verified is False:
            quality *= 0.55
        elif verified is not True:
            quality *= 0.75

        notes = []

        if normalized in {"exchange", "cex"}:
            notes.append(
                "Exchange funding is neutral until wallet links are evaluated"
            )

        if normalized in {"fresh_wallet", "new_wallet"}:
            notes.append(
                "Fresh funding wallet is unproven; age alone is not a rug signal"
            )

        if verified is not True:
            notes.append(
                "Funding provenance is not fully verified"
            )

        return self._pillar(
            score if coverage >= 0.5 else None,
            coverage,
            quality,
            notes,
            details={
                "source_type": normalized or None,
                "verified": (
                    verified if isinstance(verified, bool) else None
                ),
            },
        )

    # ==============================================================
    # 6. DEVELOPER SOCIAL
    # ==============================================================

    def _developer_social(
        self,
        group: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:

        followers = self._number(
            group.get("followers"),
            minimum=0,
        )
        engagement = self._number(
            group.get("engagement_rate_pct"),
            minimum=0,
        )
        age_days = self._number(
            group.get("account_age_days"),
            minimum=0,
        )
        growth = self._number(
            group.get("follower_growth_7d_pct"),
            allow_negative=True,
        )

        verified_link = group.get(
            "official_token_link_verified"
        )

        suspicious = self._number(
            group.get("suspicious_followers_pct"),
            minimum=0,
            maximum=100,
        )

        engagement_score = None

        if engagement is not None:
            engagement_score = min(
                100.0,
                engagement / 5.0 * 100.0,
            )

        metrics = [
            (self._count_score(followers, 100_000), 15.0),
            (engagement_score, 25.0),
            (self._count_score(age_days, 365), 15.0),
            (self._growth_score(growth), 15.0),
            (
                (
                    100.0 if verified_link else 35.0
                )
                if isinstance(verified_link, bool)
                else None,
                15.0,
            ),
            (self._inverse_pct(suspicious), 15.0),
        ]

        score, coverage = self._weighted(metrics)

        quality = self._group_quality(
            group,
            now,
            GROUP_MAX_AGE_SECONDS["developer_social"],
        )

        notes = []

        if followers is not None and engagement is None:
            notes.append(
                "Follower count alone is insufficient to establish social strength"
            )

        if verified_link is False:
            notes.append(
                "Official token-to-account link was not verified"
            )

        return self._pillar(
            score if coverage >= 0.4 else None,
            coverage,
            quality,
            notes,
        )

    # ==============================================================
    # INDEPENDENT RUG RISK
    # ==============================================================

    def _rug_risk(
        self,
        features: dict[str, Any],
        now: datetime,
    ) -> dict[str, Any]:

        components = []
        risk_flags: list[dict[str, str]] = []

        # Developer-linked wallet history.
        dev_wallet = self._group(
            features,
            "dev_wallet",
            "developer_wallet",
        )

        clean = self._number(
            dev_wallet.get("clean_migrations"),
            minimum=0,
        )
        rugged = self._number(
            dev_wallet.get("linked_rugged_tokens"),
            minimum=0,
        )

        if (
            clean is not None
            and rugged is not None
            and clean + rugged > 0
        ):
            wallet_rug_rate = (
                100.0
                * (rugged + 1.0)
                / (clean + rugged + 2.0)
            )

            quality = self._group_quality(
                dev_wallet,
                now,
                GROUP_MAX_AGE_SECONDS["developer_wallet"],
            )

            components.append((
                wallet_rug_rate,
                20.0,
                quality,
                "linked_wallet_history",
            ))

            if rugged > 0:
                risk_flags.append(
                    self._flag(
                        "linked_rug_history",
                        "high" if rugged >= 2 else "medium",
                        f"{int(rugged)} linked rugged token outcome(s) recorded",
                    )
                )

        # Funding-wallet links.
        funding = self._group(
            features,
            "funding",
            "funding_provenance",
        )

        if funding.get("linked_rug_wallet") is True:
            components.append((
                100.0,
                15.0,
                self._group_quality(
                    funding,
                    now,
                    GROUP_MAX_AGE_SECONDS["funding_provenance"],
                ),
                "funding_link",
            ))

            risk_flags.append(
                self._flag(
                    "rug_linked_funding_wallet",
                    "high",
                    "Funding source is linked to a rug-associated wallet",
                )
            )

        elif funding.get("linked_insider_wallet") is True:
            components.append((
                80.0,
                15.0,
                self._group_quality(
                    funding,
                    now,
                    GROUP_MAX_AGE_SECONDS["funding_provenance"],
                ),
                "funding_link",
            ))

            risk_flags.append(
                self._flag(
                    "insider_linked_funding_wallet",
                    "high",
                    "Funding source is linked to an insider wallet",
                )
            )

        # Developer selling and buyer concentration.
        flow = self._group(
            features,
            "initial_flow",
            "initial_money_flow",
        )

        windows = flow.get("windows")
        if not isinstance(windows, Mapping):
            windows = {}

        dev_values = []
        concentration_values = []
        flow_quality = []

        for timeframe in ("5m", "15m", "1h"):
            window = windows.get(timeframe)

            if not isinstance(window, Mapping):
                continue

            dev_pct = self._number(
                window.get("developer_sell_pct"),
                minimum=0,
                maximum=100,
            )

            concentration = self._number(
                window.get("top_buyer_concentration_pct"),
                minimum=0,
                maximum=100,
            )

            quality = self._mapping_quality(
                window if isinstance(window.get("_meta"), Mapping) else flow,
                now,
                FLOW_MAX_AGE_SECONDS[timeframe],
            )

            if dev_pct is not None:
                dev_values.append(dev_pct)
                flow_quality.append(quality)

                if dev_pct >= 15.0:
                    risk_flags.append(
                        self._flag(
                            "developer_selling",
                            "high" if dev_pct >= 30 else "medium",
                            f"Developer sell share reached {dev_pct:.1f}% in {timeframe}",
                        )
                    )

            if concentration is not None:
                concentration_values.append(concentration)
                flow_quality.append(quality)

                if concentration >= 50.0:
                    risk_flags.append(
                        self._flag(
                            "buyer_concentration",
                            "high",
                            f"Top-buyer concentration reached {concentration:.1f}% in {timeframe}",
                        )
                    )

        if dev_values:
            quality = (
                sum(flow_quality) / len(flow_quality)
                if flow_quality else 0.5
            )

            components.append((
                max(dev_values),
                15.0,
                quality,
                "developer_sells",
            ))

        if concentration_values:
            quality = (
                sum(flow_quality) / len(flow_quality)
                if flow_quality else 0.5
            )

            components.append((
                max(concentration_values),
                10.0,
                quality,
                "buyer_concentration",
            ))

        # Contract / LP checks are deliberately separate from potential.
        contract = features.get("contract_risk")

        if not isinstance(contract, Mapping):
            contract = features.get("rug_radar")

        if not isinstance(contract, Mapping):
            contract = {}

        honeypot = contract.get("honeypot_confirmed")
        mint_active = contract.get("mint_authority_active")
        freeze_active = contract.get("freeze_authority_active")
        lp_locked = contract.get("lp_locked")
        lp_burned = contract.get("lp_burned")
        owner_renounced = contract.get("owner_renounced")

        contract_metrics = [
            (
                100.0 if honeypot is True
                else 0.0 if honeypot is False
                else None,
                45.0,
            ),
            (
                75.0 if mint_active is True
                else 0.0 if mint_active is False
                else None,
                15.0,
            ),
            (
                75.0 if freeze_active is True
                else 0.0 if freeze_active is False
                else None,
                15.0,
            ),
            (
                65.0 if lp_locked is False and lp_burned is False
                else 0.0 if lp_locked is True or lp_burned is True
                else None,
                15.0,
            ),
            (
                60.0 if owner_renounced is False
                else 0.0 if owner_renounced is True
                else None,
                10.0,
            ),
        ]

        contract_score, contract_coverage = self._weighted(
            contract_metrics
        )

        if contract_score is not None and contract_coverage >= 0.4:
            quality = self._group_quality(
                contract,
                now,
                24 * 60 * 60,
            )

            components.append((
                contract_score,
                40.0 * contract_coverage,
                quality,
                "contract_safety",
            ))

        if honeypot is True:
            risk_flags.append(
                self._flag(
                    "confirmed_honeypot",
                    "critical",
                    "A honeypot check is explicitly confirmed",
                )
            )

        if mint_active is True:
            risk_flags.append(
                self._flag(
                    "mint_authority_active",
                    "high",
                    "Mint authority is active",
                )
            )

        if freeze_active is True:
            risk_flags.append(
                self._flag(
                    "freeze_authority_active",
                    "high",
                    "Freeze authority is active",
                )
            )

        if lp_locked is False and lp_burned is False:
            risk_flags.append(
                self._flag(
                    "liquidity_not_locked_or_burned",
                    "high",
                    "Liquidity is neither confirmed locked nor burned",
                )
            )

        if owner_renounced is False:
            risk_flags.append(
                self._flag(
                    "owner_not_renounced",
                    "medium",
                    "Token owner privileges are not confirmed renounced",
                )
            )

        # Keep the highest severity for each repeated flag.
        unique_flags: dict[str, dict[str, str]] = {}

        for flag in risk_flags:
            existing = unique_flags.get(flag["code"])

            if (
                existing is None
                or self._severity_rank(flag["severity"])
                > self._severity_rank(existing["severity"])
            ):
                unique_flags[flag["code"]] = flag

        total_weight = sum(
            item[1] for item in components
        )

        # A confirmed honeypot is an immediate safety veto even if
        # other risk inputs have not arrived.
        if honeypot is True:
            contract_quality = self._group_quality(
                contract,
                now,
                24 * 60 * 60,
            )

            return {
                "score": 100.0,
                "status": "hard_veto",
                "coverage_pct": max(
                    45.0,
                    min(100.0, total_weight),
                ),
                "confidence_pct": contract_quality * 100.0,
                "components": [
                    {
                        "name": name,
                        "risk_score": self._round(value),
                        "weight": weight,
                    }
                    for value, weight, _quality, name in components
                ],
                "risk_flags": list(unique_flags.values()),
                "hard_veto": True,
            }

        if total_weight == 0:
            return {
                "score": None,
                "status": "insufficient_data",
                "coverage_pct": 0.0,
                "confidence_pct": 0.0,
                "components": [],
                "risk_flags": list(unique_flags.values()),
                "hard_veto": False,
            }

        score = (
            sum(item[0] * item[1] for item in components)
            / total_weight
        )

        coverage = min(100.0, total_weight)

        confidence = (
            sum(item[2] * item[1] for item in components)
            / total_weight
            * 100.0
        )

        status = (
            "scored"
            if coverage >= self.MIN_RUG_COVERAGE
            else "insufficient_data"
        )

        if status != "scored":
            score = None

        return {
            "score": score,
            "status": status,
            "coverage_pct": coverage,
            "confidence_pct": confidence,
            "components": [
                {
                    "name": name,
                    "risk_score": self._round(value),
                    "weight": weight,
                }
                for value, weight, _quality, name in components
            ],
            "risk_flags": list(unique_flags.values()),
            "hard_veto": False,
        }

    # ==============================================================
    # COMPOSITION AND VALIDATION HELPERS
    # ==============================================================

    def _combine_pillars(
        self,
        pillars: dict[str, dict[str, Any]],
    ) -> tuple[float | None, float, float]:

        weighted_coverage = 0.0
        effective_weight = 0.0
        weighted_score = 0.0
        weighted_confidence = 0.0

        for name, weight in PILLAR_WEIGHTS.items():
            item = pillars[name]
            pillar_coverage = item["coverage_pct"] / 100.0

            if item["score"] is None or pillar_coverage <= 0:
                continue

            weighted_coverage += weight * pillar_coverage

            used_weight = weight * pillar_coverage
            effective_weight += used_weight

            weighted_score += item["score"] * used_weight
            weighted_confidence += (
                item["confidence_pct"] * used_weight
            )

            item["model_weight_pct"] = weight
            item["effective_weight_pct"] = used_weight

        coverage_pct = weighted_coverage

        confidence_pct = (
            weighted_confidence / effective_weight
            if effective_weight
            else 0.0
        )

        if (
            coverage_pct < self.MIN_POTENTIAL_COVERAGE
            or effective_weight == 0
        ):
            return None, coverage_pct, confidence_pct

        return (
            weighted_score / effective_weight,
            coverage_pct,
            confidence_pct,
        )

    @staticmethod
    def _pillar(
        score: float | None,
        coverage: float,
        confidence: float,
        notes: list[str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        return {
            "score": SentinelScoreEngine._round(score),
            "coverage_pct": SentinelScoreEngine._round(
                max(0.0, min(100.0, coverage * 100.0))
            ),
            "confidence_pct": SentinelScoreEngine._round(
                max(0.0, min(100.0, confidence * 100.0))
            ),
            "notes": notes or [],
            "details": details or {},
        }

    @staticmethod
    def _weighted(
        metrics: list[tuple[float | None, float]],
    ) -> tuple[float | None, float]:

        expected = sum(
            weight for _score, weight in metrics
        )

        available = [
            (score, weight)
            for score, weight in metrics
            if score is not None
        ]

        present = sum(
            weight for _score, weight in available
        )

        if expected <= 0 or present <= 0:
            return None, 0.0

        score = (
            sum(float(value) * weight for value, weight in available)
            / present
        )

        return (
            max(0.0, min(100.0, score)),
            present / expected,
        )

    @staticmethod
    def _group(
        features: Mapping[str, Any],
        *names: str,
    ) -> dict[str, Any]:

        for name in names:
            value = features.get(name)

            if isinstance(value, Mapping):
                return dict(value)

        return {}

    @staticmethod
    def _number(
        value: Any,
        *,
        minimum: float | None = None,
        maximum: float | None = None,
        allow_negative: bool = False,
    ) -> float | None:

        if isinstance(value, bool) or value is None:
            return None

        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return None

        if not math.isfinite(parsed):
            return None

        if not allow_negative and parsed < 0:
            return None

        if minimum is not None and parsed < minimum:
            return None

        if maximum is not None and parsed > maximum:
            return None

        return parsed

    @staticmethod
    def _pct(value: Any) -> float | None:
        return SentinelScoreEngine._number(
            value,
            minimum=0,
            maximum=100,
        )

    @staticmethod
    def _inverse_pct(value: Any) -> float | None:
        parsed = SentinelScoreEngine._pct(value)

        return (
            None
            if parsed is None
            else 100.0 - parsed
        )

    @staticmethod
    def _growth_score(value: Any) -> float | None:
        parsed = SentinelScoreEngine._number(
            value,
            allow_negative=True,
        )

        if parsed is None:
            return None

        return 50.0 + 50.0 * math.tanh(parsed / 100.0)

    @staticmethod
    def _count_score(
        value: Any,
        saturation_at: float,
    ) -> float | None:

        parsed = SentinelScoreEngine._number(
            value,
            minimum=0,
        )

        if parsed is None:
            return None

        denominator = math.log1p(
            max(1.0, saturation_at)
        )

        return min(
            100.0,
            100.0 * math.log1p(parsed) / denominator,
        )

    @staticmethod
    def _normalize_category(value: Any) -> str | None:
        if not isinstance(value, str):
            return None

        key = (
            value.strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        aliases = {
            "major_x_account_meme": "major_x_tweet",
            "big_x_tweet": "major_x_tweet",
            "viral_animal_meme": "viral_animal",
            "new_meme_template": "meme_template",
            "social_cultural_trend": "cultural_trend",
            "ai_or_physical_innovation": "ai_innovation",
            "unique_product": "product_concept",
            "trading_terminal": "terminal_meta",
            "current_meta": "terminal_meta",
            "world_event_science": "world_event",
        }

        key = aliases.get(key, key)

        return (
            key
            if key in NARRATIVE_CATEGORY_SCORES
            else None
        )

    @staticmethod
    def _parse_datetime(value: Any) -> datetime | None:
        if isinstance(value, datetime):
            parsed = value

        elif isinstance(value, str):
            try:
                parsed = datetime.fromisoformat(
                    value.replace("Z", "+00:00")
                )
            except ValueError:
                return None

        else:
            return None

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)

    @classmethod
    def _freshness(
        cls,
        meta: Mapping[str, Any],
        now: datetime,
        max_age_seconds: float,
    ) -> float:

        stamp = cls._parse_datetime(
            meta.get("observed_at")
            or meta.get("updated_at")
        )

        if stamp is None:
            return 0.55

        age = max(
            0.0,
            (now - stamp).total_seconds(),
        )

        if age <= max_age_seconds:
            return 1.0

        return max(
            0.15,
            max_age_seconds / age,
        )

    @staticmethod
    def _quality_value(value: Any) -> float:
        if isinstance(value, bool):
            return 0.5

        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return 0.7

        if not math.isfinite(parsed):
            return 0.5

        if parsed > 1.0:
            parsed /= 100.0

        return max(
            0.1,
            min(1.0, parsed),
        )

    @classmethod
    def _group_quality(
        cls,
        group: Mapping[str, Any],
        now: datetime,
        max_age_seconds: float,
    ) -> float:

        return cls._mapping_quality(
            group,
            now,
            max_age_seconds,
        )

    @classmethod
    def _mapping_quality(
        cls,
        group: Mapping[str, Any],
        now: datetime,
        max_age_seconds: float,
    ) -> float:
        """Use the least-fresh field so partial updates cannot refresh siblings."""

        meta = (
            group.get("_meta")
            if isinstance(group.get("_meta"), Mapping)
            else {}
        )

        freshness_values = [
            cls._freshness(
                meta,
                now,
                max_age_seconds,
            )
        ]

        quality_values = [
            cls._quality_value(
                meta.get("source_quality")
            )
        ]

        field_meta = group.get("_field_meta")

        if isinstance(field_meta, Mapping):
            for item in field_meta.values():
                if not isinstance(item, Mapping):
                    continue

                freshness_values.append(
                    cls._freshness(
                        item,
                        now,
                        max_age_seconds,
                    )
                )

                quality_values.append(
                    cls._quality_value(
                        item.get("source_quality")
                    )
                )

        return (
            min(freshness_values)
            * min(quality_values)
        )

    @staticmethod
    def _grade(score: float) -> str:
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        if score >= 55:
            return "C"
        if score >= 40:
            return "D"
        return "E"

    @staticmethod
    def _flag(
        code: str,
        severity: str,
        message: str,
    ) -> dict[str, str]:

        return {
            "code": code,
            "severity": severity,
            "message": message,
        }

    @staticmethod
    def _severity_rank(value: str) -> int:
        return {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }.get(value, 0)

    @staticmethod
    def _round(value: float | None) -> float | None:
        if value is None:
            return None

        if not math.isfinite(float(value)):
            return None

        return round(float(value), 2)