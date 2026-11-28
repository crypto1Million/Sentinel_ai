class SmartMoneyTracker:
    """Small deterministic tiering helper; it does not infer wallet identity."""

    def analyze(self, smart_wallets: int) -> dict[str, int | str]:
        if isinstance(smart_wallets, bool) or not isinstance(smart_wallets, int) or smart_wallets < 0:
            raise ValueError("smart_wallets must be a non-negative integer")
        if smart_wallets >= 20:
            return {"grade": "A", "score": 95}
        if smart_wallets >= 10:
            return {"grade": "B", "score": 75}
        return {"grade": "C", "score": 50}