class VolumeFlowEngine:

    def calculate(
        self,
        previous_volume: float,
        current_volume: float,
        previous_timestamp: float,
        current_timestamp: float,
    ) -> dict:

        delta = current_volume - previous_volume

        elapsed = max(
            current_timestamp - previous_timestamp,
            1.0,
        )

        flow_rate = delta / elapsed

        if previous_volume > 0:
            change_percent = (
                delta / previous_volume
            ) * 100
        else:
            change_percent = 0.0

        return {
            "delta_usd": delta,
            "flow_rate": flow_rate,
            "change_percent": change_percent,
            "positive": delta > 0,
        }