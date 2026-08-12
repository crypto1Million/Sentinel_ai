from smart_money_tracker import SmartMoneyTracker
from whale_tracker import WhaleTracker
from fresh_wallet_tracker import FreshWalletTracker
from money_flow_score import MoneyFlowScore
from market_pulse import MarketPulse


class IntelligenceEngine:

    def __init__(self):

        self.smart = (
            SmartMoneyTracker()
        )

        self.whale = (
            WhaleTracker()
        )

        self.fresh = (
            FreshWalletTracker()
        )

        self.money_flow = (
            MoneyFlowScore()
        )

        self.pulse = (
            MarketPulse()
        )

    def analyze(
        self,
        token
    ):

        smart = self.smart.analyze(
            token["smart_wallets"]
        )

        whale = self.whale.analyze(
            token["whale_inflow"]
        )

        fresh = self.fresh.analyze(
            token["fresh_wallet_percent"]
        )

        money_score = (
            self.money_flow.calculate(

                smart["score"],

                token["inflow"],

                token["outflow"],

                whale["strength"]
            )
        )

        pulse = (
            self.pulse.generate(

                money_score,

                token["holder_growth"]
            )
        )

        return {

            "money_flow_score":
            money_score,

            "market_pulse":
            pulse,

            "smart_money":
            smart,

            "whale_activity":
            whale,

            "fresh_wallets":
            fresh
        }