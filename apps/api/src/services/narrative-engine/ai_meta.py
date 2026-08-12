class AIMeta:

    KEYWORDS = [

        "ai",

        "agent",

        "gpt",

        "llm",

        "virtual",

        "neural",

        "sentient"
    ]

    def detect(
        self,
        text: str
    ):

        text = text.lower()

        for word in self.KEYWORDS:

            if word in text:

                return "AI"

        return None