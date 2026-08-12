from .wallet_profit_history import WalletProfitHistory
from .cost_basis_calculator import CostBasisCalculator
from .realized_pnl_tracker import RealizedPnLTracker
from .holder_churn_analyzer import HolderChurnAnalyzer


class ExitLiquidityDetector:

    def __init__(self):

        self.wallet_history = WalletProfitHistory()

        self.cost_basis = CostBasisCalculator()

        self.pnl_tracker = RealizedPnLTracker()

        self.churn = HolderChurnAnalyzer()

    def analyze(

        self,

        wallet,

        buys,

        sells,

        previous_holders,

        current_holders,

        current_price

    ):

        cost = self.cost_basis.calculate(buys)

        realized = []

        total_realized = 0

        for sell in sells:

            pnl = self.pnl_tracker.calculate(

                sell["price"],

                cost,

                sell["amount"]

            )

            total_realized += pnl["realized_pnl"]

            realized.append(pnl)

            self.wallet_history.add_trade(

                wallet,

                sell["token"],

                pnl["realized_pnl"],

                sell["timestamp"]

            )

        unrealized = self.cost_basis.unrealized_pnl(

            current_price,

            cost,

            sum(

                b["amount"] for b in buys

            ) - sum(

                s["amount"] for s in sells

            )

        )

        churn = self.churn.analyze(

            previous_holders,

            current_holders

        )

        exit_score = 0

        if churn["churn_rate"] > 20:
            exit_score += 30

        if total_realized > 50000:
            exit_score += 35

        if unrealized < 0:
            exit_score += 15

        if self.wallet_history.win_rate(wallet) > 80:
            exit_score += 20

        return {

            "exit_liquidity_score": min(exit_score, 100),

            "cost_basis": cost,

            "realized_pnl": total_realized,

            "unrealized_pnl": unrealized,

            "wallet_win_rate":

                self.wallet_history.win_rate(wallet),

            "holder_churn": churn,

            "wallet_profit_history":

                self.wallet_history.get_wallet_history(wallet),

            "is_exit_liquidity":

                exit_score >= 70

        }