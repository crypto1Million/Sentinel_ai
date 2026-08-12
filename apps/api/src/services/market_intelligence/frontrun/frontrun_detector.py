from .block_analyzer import BlockAnalyzer
from .jito_bundle_analyzer import JitoBundleAnalyzer
from .mempool_timing_analyzer import MempoolTimingAnalyzer
from .coordinated_wallet_detector import CoordinatedWalletDetector


class FrontRunDetector:

    def __init__(self):

        self.block = BlockAnalyzer()

        self.bundle = JitoBundleAnalyzer()

        self.timing = MempoolTimingAnalyzer()

        self.wallets = CoordinatedWalletDetector()

    def analyze(
        self,
        block_trades,
        bundle,
        pending_tx,
        wallet_trades
    ):

        block_data = self.block.analyze(block_trades)

        bundle_data = self.bundle.analyze_bundle(bundle)

        timing_data = self.timing.analyze(pending_tx)

        coordinated = self.wallets.detect(wallet_trades)

        risk = 0

        if bundle_data["possible_frontrun"]:
            risk += 35

        if timing_data["suspicious"]:
            risk += 35

        if coordinated:
            risk += 30

        return {

            "front_run_score": min(risk, 100),

            "block_analysis": block_data,

            "bundle_analysis": bundle_data,

            "timing_analysis": timing_data,

            "coordinated_wallets": coordinated,

            "is_front_run": risk >= 70

        }