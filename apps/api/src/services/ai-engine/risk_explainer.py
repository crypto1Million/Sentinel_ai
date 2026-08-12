class RiskExplainer:

    def analyze(
        self,
        token
    ):

        risks = []

        if token["rug_risk"] > 50:

            risks.append(
                "Elevated rug risk"
            )

        if token["top10"] > 40:

            risks.append(
                "Holder concentration"
            )

        if token["dev_wallet"] > 10:

            risks.append(
                "Large dev allocation"
            )

        return risks