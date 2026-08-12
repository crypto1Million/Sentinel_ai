class JitoSearcherDetector:

    def detect(self, bundles):

        searchers = []

        for bundle in bundles:

            if bundle.get("searcher"):

                searchers.append({

                    "searcher": bundle["searcher"],

                    "priority_fee": bundle["priority_fee"],

                    "bundle_id": bundle["bundle_id"]

                })

        return searchers

    def score(self, searchers):

        return min(len(searchers) * 15, 100)