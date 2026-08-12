class GamingMeta:

    KEYWORDS = [

        "game",

        "gaming",

        "play",

        "quest",

        "arena",

        "rpg",

        "esports",

        "play to earn"
    ]

    def detect(
        self,
        text: str
    ):

        text = text.lower()

        for word in self.KEYWORDS:

            if word in text:

                return "GAMING"

        return None