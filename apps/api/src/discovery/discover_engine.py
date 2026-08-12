from conviction_engine import ConvictionEngine
from opportunity_finder import OpportunityFinder

class DiscoverEngine:

    def __init__(self):

        self.conviction = ConvictionEngine()

        self.opportunity = OpportunityFinder()

    def analyze(
        self,
        token
    ):

        conviction = self.conviction.classify(
            token["sentinel_score"]
        )

        opportunity = self.opportunity.find(
            token
        )

        return {

            "symbol":
            token["symbol"],

            "conviction":
            conviction,

            "opportunity":
            opportunity,

            "score":
            token["sentinel_score"]
        }