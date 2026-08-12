class CelebrityMeta:

    KEYWORDS = [

        "elon",

        "musk",

        "tate",

        "mrbeast",

        "ronaldo",

        "messi",

        "trump",

        "drake"
    ]

    def detect(
        self,
        text: str
    ):

        text = text.lower()

        for word in self.KEYWORDS:

            if word in text:

                return "CELEBRITY"

        return None