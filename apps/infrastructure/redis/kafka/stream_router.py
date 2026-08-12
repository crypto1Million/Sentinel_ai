class StreamRouter:

    def route(

        self,

        event
    ):

        if event["type"] == "token":

            return "token_updates"

        if event["type"] == "score":

            return "score_updates"

        return "general"