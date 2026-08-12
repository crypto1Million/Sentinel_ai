class WalletInsiderDetector:

    def detect(
        self,
        early_entries: int,
        launches_participated: int,
        bundled_wallet_links: int
    ):

        score = 0

        score += early_entries * 3

        score += launches_participated * 2

        score += bundled_wallet_links * 15

        if score >= 70:

            return {
                "is_insider": True,
                "confidence": score
            }

        return {
            "is_insider": False,
            "confidence": score
        }