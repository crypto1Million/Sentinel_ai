from mint_checker import MintChecker

from freeze_checker import FreezeChecker

from bundle_detector import BundleDetector

from sniper_detector import SniperDetector

from insider_detector import InsiderDetector

from lp_checker import LPChecker

from risk_score import RiskScore


class RugScanner:

    def __init__(self):

        self.mint = MintChecker()

        self.freeze = FreezeChecker()

        self.bundle = BundleDetector()

        self.sniper = SniperDetector()

        self.insider = InsiderDetector()

        self.lp = LPChecker()

        self.score = RiskScore()

    def scan(
        self,
        token_data
    ):

        mint = self.mint.check(
            token_data["mint_authority"]
        )

        freeze = self.freeze.check(
            token_data["freeze_authority"]
        )

        bundle = self.bundle.detect(
            token_data["bundled_percent"]
        )

        sniper = self.sniper.detect(
            token_data["sniper_percent"]
        )

        insider = self.insider.detect(
            token_data["insider_percent"]
        )

        lp = self.lp.analyze(
            token_data["lp_burned"]
        )

        rug_score = self.score.calculate(

            mint["risk"],

            freeze["risk"],

            bundle["score"],

            sniper["score"],

            insider["score"],

            lp["risk"]
        )

        return {

            "rug_risk":
            rug_score,

            "bundle":
            bundle,

            "sniper":
            sniper,

            "insider":
            insider
        }