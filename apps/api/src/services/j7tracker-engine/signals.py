class SignalEngine:

    def generate_signal(

        self,

        event_type: str
    ):

        mapping = {

            "follow": 10,

            "deploy": 20,

            "mention": 5,

            "buy": 15
        }

        return mapping.get(
            event_type,
            0
        )