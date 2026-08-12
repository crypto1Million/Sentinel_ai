class PoliticalMeta:

    KEYWORDS = [

        "trump",

        "maga",

        "biden",

        "president",

        "government",

        "election",

        "politics",

        "congress",

        "government"
    ]

    def detect(
        self,
        text: str
    ):

        text = text.lower()

        for word in self.KEYWORDS:

            if word in text:

                return "POLITICAL"

        return None