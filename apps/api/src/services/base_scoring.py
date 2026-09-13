from __future__ import annotations

from typing import Any


def clamp(
    value: float,
) -> float:
    return max(
        0.0,
        min(
            100.0,
            value,
        ),
    )


class BaseScoring:
    def calculate(
        self,
        rug_score: float,
        deployer_quality: float,
        wallet_quality: float,
        holder_quality: float,
        liquidity_quality: float,
        social_strength: float = 50,
        narrative_strength: float = 50,
    ) -> dict[str, Any]:
        score = (
            clamp(
                100 - rug_score
            )
            * 0.25
            + clamp(deployer_quality)
            * 0.15
            + clamp(wallet_quality)
            * 0.15
            + clamp(holder_quality)
            * 0.15
            + clamp(liquidity_quality)
            * 0.15
            + clamp(social_strength)
            * 0.10
            + clamp(narrative_strength)
            * 0.05
        )

        return {
            "chain": "base",
            "base_score": round(
                clamp(score),
                2,
            ),
            "components": {
                "contract_security": round(
                    clamp(100 - rug_score),
                    2,
                ),
                "deployer_quality": round(
                    clamp(deployer_quality),
                    2,
                ),
                "wallet_quality": round(
                    clamp(wallet_quality),
                    2,
                ),
                "holder_distribution": round(
                    clamp(holder_quality),
                    2,
                ),
                "initial_liquidity": round(
                    clamp(liquidity_quality),
                    2,
                ),
                "social_strength": round(
                    clamp(social_strength),
                    2,
                ),
                "narrative_strength": round(
                    clamp(narrative_strength),
                    2,
                ),
            },
        }