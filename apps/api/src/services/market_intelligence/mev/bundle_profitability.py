class BundleProfitability:

    def analyze(self, bundles):

        report = []

        for bundle in bundles:

            pnl = (

                bundle["output"]

                - bundle["input"]

                - bundle["fees"]

            )

            report.append({

                "bundle": bundle["bundle_id"],

                "profit": pnl

            })

        return report

    def average_profit(self, bundles):

        report = self.analyze(bundles)

        if not report:
            return 0

        return sum(

            x["profit"]

            for x in report

        ) / len(report)