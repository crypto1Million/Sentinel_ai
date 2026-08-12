class MempoolTimingAnalyzer:

    def analyze(self, pending_tx):

        latency = pending_tx["confirmed"] - pending_tx["submitted"]

        suspicious = latency < 0.4

        return {
            "latency": latency,
            "suspicious": suspicious
        }

    def timing_score(self, pending_tx):

        latency = pending_tx["confirmed"] - pending_tx["submitted"]

        if latency < 0.20:
            return 100

        if latency < 0.50:
            return 80

        if latency < 1:
            return 60

        return 20