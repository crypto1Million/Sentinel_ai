from typing import List, Dict


class WalletDistributionScore:

    def calculate(
        self,
        holder_changes: List[float]
    ) -> Dict:

        if not holder_changes:
            return {
                "score": 0
            }

        sellers = len(
            [x for x in holder_changes if x < 0]
        )

        ratio = sellers / len(holder_changes)

        score = int(ratio * 100)

        return {
            "score": score,
            "distribution_ratio": ratio
        }