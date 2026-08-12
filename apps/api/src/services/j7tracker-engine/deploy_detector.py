class DeployDetector:

    def detect(
        self,
        deploys: int
    ):

        return min(
            100,
            deploys * 10
        )