from collections import defaultdict


class ValidatorRelationshipAnalyzer:

    def analyze(self, bundles):

        validators = defaultdict(int)

        for bundle in bundles:

            validators[

                bundle["validator"]

            ] += 1

        return validators

    def dominant_validator(self, bundles):

        validators = self.analyze(bundles)

        if not validators:

            return None

        return max(

            validators,

            key=validators.get

        )