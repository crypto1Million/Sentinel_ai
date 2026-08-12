class AnimalMeta:

    KEYWORDS = [

        "dog",

        "cat",

        "pepe",

        "frog",

        "roach",

        "roachi",

        "shiba",

        "wolf"
    ]

    def detect(
        self,
        text: str
    ):

        text = text.lower()

        for word in self.KEYWORDS:

            if word in text:

                return "ANIMAL"

        return None