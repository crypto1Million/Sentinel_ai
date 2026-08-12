from dev_quality import DevQualityScorer
from wallet_quality import WalletQualityScorer
from volume_quality import VolumeQualityScorer
from social_strength import SocialStrengthScorer
from narrative_momentum import NarrativeMomentumScorer
from rug_risk import RugRiskScorer
from opportunity_score import OpportunityScoreScorer


class SentinelScoreEngine:

    def __init__(self):

        self.dev = DevQualityScorer()

        self.wallet = WalletQualityScorer()

        self.volume = VolumeQualityScorer()

        self.social = SocialStrengthScorer()

        self.narrative = NarrativeMomentumScorer()

        self.rug = RugRiskScorer()

        self.opportunity = OpportunityScoreScorer()

    def calculate(self, data):

        dev_score = self.dev.calculate(
            data["successful_launches"],
            data["rugs"],
            data["avg_ath"],
            data["wallet_age_days"]
        )

        wallet_score = self.wallet.calculate(
            data["smart_money"],
            data["whales"],
            data["insiders"]
        )

        volume_score = self.volume.calculate(
            data["volume"],
            data["buyers"],
            data["repeat_wallets"]
        )

        social_score = self.social.calculate(
            data["telegram_members"],
            data["twitter_mentions"],
            data["j7_signals"],
            data["engagement_rate"]
        )

        narrative_score = self.narrative.calculate(
            data["narrative_rank"],
            data["narrative_growth"],
            data["narrative_volume_growth"]
        )

        rug_score = self.rug.calculate(
            data["mint_enabled"],
            data["freeze_enabled"],
            data["dev_percent"],
            data["bundled_wallets"]
        )

        opportunity_score = self.opportunity.calculate(
            data["market_cap"],
            data["age_minutes"],
            data["score_boost"]
        )

        sentinel_score = (

            dev_score * 0.20 +

            wallet_score * 0.20 +

            volume_score * 0.15 +

            social_score * 0.10 +

            narrative_score * 0.15 +

            rug_score * 0.10 +

            opportunity_score * 0.10

        )

        if sentinel_score >= 90:
            grade = "S"
            recommendation = "STRONG BUY"

        elif sentinel_score >= 80:
            grade = "A"
            recommendation = "BUY"

        elif sentinel_score >= 70:
            grade = "B"
            recommendation = "WATCH"

        elif sentinel_score >= 60:
            grade = "C"
            recommendation = "SPECULATIVE"

        else:
            grade = "D"
            recommendation = "AVOID"

        return {

            "sentinel_score":
            round(sentinel_score, 2),

            "grade":
            grade,

            "recommendation":
            recommendation,

            "dev_quality":
            round(dev_score, 2),

            "wallet_quality":
            round(wallet_score, 2),

            "volume_quality":
            round(volume_score, 2),

            "social_strength":
            round(social_score, 2),

            "narrative_momentum":
            round(narrative_score, 2),

            "rug_risk":
            round(rug_score, 2),

            "opportunity_score":
            round(opportunity_score, 2)
        }