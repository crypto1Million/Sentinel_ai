class MigrationDetector:

    def detect(
        self,
        token
    ):

        return token.get(
            "migrated",
            False
        )