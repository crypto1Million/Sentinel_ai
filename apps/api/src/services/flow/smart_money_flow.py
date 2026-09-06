class SmartMoneyFlowEngine:

    def calculate(
        self,
        previous_smart_money_usd: float,
        current_smart_money_usd: float,
        previous_timestamp: float,
        current_timestamp: float,
    ) -> dict:

        delta = current_smart_money_usd - previous_smart_money_usd

        elapsed = max(
            current_timestamp - previous_timestamp,
            1.0,
        )

        flow_rate = delta / elapsed

        return {
            "delta_usd": delta,
            "flow_rate": flow_rate,
            "positive": delta > 0,
        }