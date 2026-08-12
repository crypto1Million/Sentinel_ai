from verdict_engine import VerdictEngine
from conviction_engine import ConvictionEngine
from confidence_engine import ConfidenceEngine
from explanation_engine import ExplanationEngine
from risk_explainer import RiskExplainer
from opportunity_explainer import OpportunityExplainer
from recommendation_engine import RecommendationEngine


class AIAnalyzer:

    def __init__(self):

        self.verdict = VerdictEngine()

        self.conviction = ConvictionEngine()

        self.confidence = ConfidenceEngine()

        self.explanation = ExplanationEngine()

        self.risks = RiskExplainer()

        self.opportunities = (
            OpportunityExplainer()
        )

        self.recommendation = (
            RecommendationEngine()
        )

    def analyze(
        self,
        token
    ):

        verdict = self.verdict.generate(

            token["sentinel_score"],

            token["rug_risk"]
        )

        conviction = (
            self.conviction.classify(
                token["sentinel_score"]
            )
        )

        confidence = (
            self.confidence.calculate(

                token["sentinel_score"],

                token["wallet_quality"],

                token["narrative_momentum"]
            )
        )

        reasons = (
            self.explanation.generate(
                token
            )
        )

        risks = (
            self.risks.analyze(
                token
            )
        )

        opportunities = (
            self.opportunities.analyze(
                token
            )
        )

        recommendation = (
            self.recommendation.generate(

                verdict,

                confidence
            )
        )

        return {

            "verdict":
            verdict,

            "conviction":
            conviction,

            "confidence":
            confidence,

            "reasons":
            reasons,

            "risks":
            risks,

            "opportunities":
            opportunities,

            "recommendation":
            recommendation
        }