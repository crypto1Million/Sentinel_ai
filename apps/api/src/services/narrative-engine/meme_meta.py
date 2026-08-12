class MemeMeta:

    KEYWORDS = [

        "meme",

        "wojak",

        "gigachad",

        "based",

        "cope",

        "rekt"

        "cat meme"

        "dog meme",

        "animal meme",

        "viral meme",

        "bird meme"
    ]

    def detect(
        self,
        text: str
    ):

        text = text.lower()

        for word in self.KEYWORDS:

            if word in text:

                return "MEME"

        return None