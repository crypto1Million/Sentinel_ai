from typing import Dict, Any

class SentinelScoreService:

    def calculate(
        self,
        dev_quality: float,
        wallet_quality: float,
        volume_quality: float,
        social_strength: float,
        narrative_momentum: float,
        rug_safety: float,
        smart_money: float,
        liquidity_flow: float,
    ):

        metrics = {
            "dev_quality": dev_quality,
            "wallet_quality": wallet_quality,
            "volume_quality": volume_quality,
            "social_strength": social_strength,
            "narrative_momentum": narrative_momentum,
            "rug_safety": rug_safety,
            "smart_money": smart_money,
            "liquidity_flow": liquidity_flow,
        }

        score = 0

        for metric, weight in self.weights.items():
            score += (
                metrics.get(metric, 0)
                * weight
            )

        return round(
            min(score, 100),
            2,
        )


class SentinelScoreService:
    """
    Sentinel AI dynamic token scoring engine.

    The score starts with an initial evaluation and can be
    recalculated when important market signals change.
    """

    def __init__(self):
        self.weights = {
            "dev_quality": 0.15,
            "wallet_quality": 0.15,
            "volume_quality": 0.15,
            "social_strength": 0.10,
            "narrative_momentum": 0.10,
            "rug_safety": 0.15,
            "smart_money": 0.10,
            "liquidity_flow": 0.10,
        }

    def calculate_initial_score(
        self,
        metrics: Dict[str, float],
    ) -> Dict[str, Any]:

        score = 0

        for metric, weight in self.weights.items():
            value = metrics.get(metric, 0)
            score += value * weight

        score = round(min(max(score, 0), 100), 2)

        return {
            "score": score,
            "type": "initial",
            "reason": "Initial Sentinel Score calculation",
        }

    def recalculate_score(
        self,
        current_score: float,
        smart_money_flow: float = 0,
        liquidity_flow: float = 0,
        volume_flow: float = 0,
    ) -> Dict[str, Any]:

        adjustments = {
            "smart_money": 0,
            "liquidity": 0,
            "volume": 0,
        }

        # SMART MONEY FLOW
        if smart_money_flow >= 80:
            adjustments["smart_money"] = 15

        elif smart_money_flow >= 60:
            adjustments["smart_money"] = 10

        elif smart_money_flow >= 40:
            adjustments["smart_money"] = 5

        # LIQUIDITY FLOW
        if liquidity_flow >= 80:
            adjustments["liquidity"] = 12

        elif liquidity_flow >= 60:
            adjustments["liquidity"] = 8

        elif liquidity_flow >= 40:
            adjustments["liquidity"] = 4

        # VOLUME FLOW
        if volume_flow >= 80:
            adjustments["volume"] = 12

        elif volume_flow >= 60:
            adjustments["volume"] = 8

        elif volume_flow >= 40:
            adjustments["volume"] = 4

        total_adjustment = sum(
            adjustments.values()
        )

        new_score = current_score + total_adjustment

        new_score = round(
            min(max(new_score, 0), 100),
            2,
        )

        signals = []

        if adjustments["smart_money"] > 0:
            signals.append(
                "Smart money inflow detected"
            )

        if adjustments["liquidity"] > 0:
            signals.append(
                "Liquidity expansion detected"
            )

        if adjustments["volume"] > 0:
            signals.append(
                "Volume acceleration detected"
            )

        return {
            "previous_score": current_score,
            "score": new_score,
            "adjustments": adjustments,
            "signals": signals,
            "market_momentum_detected": (
                total_adjustment > 0
            ),
        }