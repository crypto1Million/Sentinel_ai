class JitoBundleAnalyzer:

    def analyze_bundle(self, bundle):

        return {
            "bundle_id": bundle.get("bundle_id"),
            "transactions": len(bundle.get("transactions", [])),
            "priority_fee": bundle.get("priority_fee"),
            "possible_frontrun": bundle.get("priority_fee", 0) > 500000
        }

    def bundle_score(self, bundle):

        score = 0

        if bundle.get("priority_fee", 0) > 500000:
            score += 40

        if len(bundle.get("transactions", [])) > 3:
            score += 30

        if bundle.get("sandwich"):
            score += 30

        return min(score, 100)