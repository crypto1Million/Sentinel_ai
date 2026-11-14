from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any


class WhaleWalletRankings:
    """
    Rank wallets using existing Sentinel wallet snapshot metrics.

    Inputs are compatible with the fields in WalletSnapshot:
        - whale_score
        - total_value_usd
        - realized_pnl
        - unrealized_pnl
        - win_rate
        - conviction_score
        - smart_money_score

    The output score is a relative ranking heuristic, not a
    prediction of future wallet performance.
    """

    WEIGHTS = {
        "whale_score": 0.50,
        "total_value_usd": 0.20,
        "net_pnl": 0.15,
        "win_rate": 0.10,
        "conviction_score": 0.05,
    }

    def _number(self, value: Any) -> float | None:
        """Convert a value into a valid finite number."""

        if value is None or isinstance(value, bool):
            return None

        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            return None

        if not math.isfinite(number):
            return None

        return number

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(100.0, value))

    def _percentile_scores(
        self,
        values: dict[int, float | None],
    ) -> dict[int, float]:
        """
        Calculate cohort-relative percentile scores.

        Equal values receive equal scores. A single available
        observation receives a neutral score of 50.
        """

        valid = [
            (index, value)
            for index, value in values.items()
            if value is not None
        ]

        if not valid:
            return {}

        if len(valid) == 1:
            return {valid[0][0]: 50.0}

        valid.sort(key=lambda item: item[1])

        scores: dict[int, float] = {}
        total = len(valid)

        start = 0

        while start < total:
            end = start + 1
            current_value = valid[start][1]

            while (
                end < total
                and valid[end][1] == current_value
            ):
                end += 1

            average_position = (
                start + end - 1
            ) / 2

            percentile = (
                average_position / (total - 1)
            ) * 100

            for position in range(start, end):
                index = valid[position][0]
                scores[index] = round(percentile, 2)

            start = end

        return scores

    def _prepare_wallet(
        self,
        wallet: Mapping[str, Any],
    ) -> dict[str, float | None]:

        whale_score = self._number(
            wallet.get("whale_score")
        )

        total_value = self._number(
            wallet.get("total_value_usd")
        )

        realized_pnl = self._number(
            wallet.get("realized_pnl")
        )

        unrealized_pnl = self._number(
            wallet.get("unrealized_pnl")
        )

        win_rate = self._number(
            wallet.get("win_rate")
        )

        conviction = self._number(
            wallet.get("conviction_score")
        )

        # Fall back to the existing smart money metric.
        if conviction is None:
            conviction = self._number(
                wallet.get("smart_money_score")
            )

        net_pnl = None

        if (
            realized_pnl is not None
            or unrealized_pnl is not None
        ):
            net_pnl = (
                (realized_pnl or 0.0)
                + (unrealized_pnl or 0.0)
            )

        if win_rate is not None:
            # Support both 0.0-1.0 and 0-100 formats.
            if 0 <= win_rate <= 1:
                win_rate *= 100

            win_rate = self._clamp(win_rate)

        return {
            "whale_score": (
                self._clamp(whale_score)
                if whale_score is not None
                else None
            ),
            "total_value_usd": total_value,
            "net_pnl": net_pnl,
            "win_rate": win_rate,
            "conviction_score": (
                self._clamp(conviction)
                if conviction is not None
                else None
            ),
        }

    def rank(
        self,
        wallets: Sequence[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Rank wallets from highest to lowest whale rank score.

        Original wallet dictionaries are not modified.
        """

        prepared = [
            self._prepare_wallet(wallet)
            for wallet in wallets
        ]

        # Relative comparisons for capital and PnL.
        capital_scores = self._percentile_scores({
            i: item["total_value_usd"]
            for i, item in enumerate(prepared)
        })

        pnl_scores = self._percentile_scores({
            i: item["net_pnl"]
            for i, item in enumerate(prepared)
        })

        ranked: list[dict[str, Any]] = []

        for index, wallet in enumerate(wallets):

            metrics = prepared[index]

            components = {
                "whale_score": metrics["whale_score"],
                "total_value_usd": capital_scores.get(index),
                "net_pnl": pnl_scores.get(index),
                "win_rate": metrics["win_rate"],
                "conviction_score": metrics["conviction_score"],
            }

            weighted_total = 0.0
            available_weight = 0.0

            for metric, weight in self.WEIGHTS.items():

                value = components[metric]

                if value is None:
                    continue

                weighted_total += value * weight
                available_weight += weight

            if available_weight > 0:
                score = weighted_total / available_weight
            else:
                score = 0.0

            if score >= 80:
                tier = "ELITE"
            elif score >= 65:
                tier = "HIGH"
            elif score >= 45:
                tier = "WATCH"
            elif available_weight == 0:
                tier = "UNRANKED"
            else:
                tier = "LOW"

            ranked.append({
                **dict(wallet),
                "whale_rank_score": round(score, 2),
                "whale_rank_coverage": round(
                    available_weight * 100, 2
                ),
                "whale_tier": tier,
            })

        ranked.sort(
            key=lambda item: item["whale_rank_score"],
            reverse=True,
        )

        for position, wallet in enumerate(ranked, start=1):
            wallet["whale_rank"] = position

        return ranked

    def top_wallets(
        self,
        wallets: Sequence[Mapping[str, Any]],
        limit: int = 25,
    ) -> list[dict[str, Any]]:
        """Return the highest-ranked wallets."""

        if limit < 0:
            raise ValueError("limit cannot be negative")

        return self.rank(wallets)[:limit]