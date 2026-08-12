from ai_meta import AIMeta

from animal_meta import AnimalMeta

from gaming_meta import GamingMeta

from political_meta import PoliticalMeta

from celebrity_meta import CelebrityMeta

from meme_meta import MemeMeta


class MetaClassifier:

    def __init__(self):

        self.ai = AIMeta()

        self.animal = AnimalMeta()

        self.gaming = GamingMeta()

        self.political = PoliticalMeta()

        self.celebrity = CelebrityMeta()

        self.meme = MemeMeta()

    def classify(
        self,
        token_name: str
    ):

        checks = [

            self.ai.detect(token_name),

            self.animal.detect(token_name),

            self.gaming.detect(token_name),

            self.political.detect(token_name),

            self.celebrity.detect(token_name),

            self.meme.detect(token_name)
        ]

        for result in checks:

            if result:

                return result

        return "UNKNOWN"