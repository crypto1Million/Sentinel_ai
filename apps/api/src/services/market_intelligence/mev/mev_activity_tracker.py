from .sandwich_detector import SandwichDetector
from .arbitrage_detector import ArbitrageDetector
from .jito_searcher_detector import JitoSearcherDetector
from .bundle_profitability import BundleProfitability
from .validator_relationship_analyzer import ValidatorRelationshipAnalyzer


class MEVActivityTracker:

    def __init__(self):

        self.sandwich = SandwichDetector()

        self.arbitrage = ArbitrageDetector()

        self.searcher = JitoSearcherDetector()

        self.bundle = BundleProfitability()

        self.validator = ValidatorRelationshipAnalyzer()

    def analyze(

        self,

        swaps,

        routes,

        bundles

    ):

        sandwiches = self.sandwich.detect(swaps)

        arbitrage = self.arbitrage.detect(routes)

        searchers = self.searcher.detect(bundles)

        profits = self.bundle.analyze(bundles)

        validators = self.validator.analyze(bundles)

        score = 0

        score += self.sandwich.score(sandwiches)

        score += self.searcher.score(searchers)

        if arbitrage:

            score += 20

        if profits:

            score += 15

        return {

            "mev_score": min(score, 100),

            "sandwiches": sandwiches,

            "arbitrage": arbitrage,

            "searchers": searchers,

            "bundle_profitability": profits,

            "validator_relationships": validators,

            "dominant_validator":

                self.validator.dominant_validator(bundles),

            "mev_detected": score >= 70

        }