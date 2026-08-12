class GraduationDetector:

    def detect(
        self,
        token
    ):

        return token.get(
            "graduated",
            False
        )