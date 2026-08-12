class J7Parser:

    def parse(
        self,
        event
    ):

        return {

            "type":
            event.get("type"),

            "user":
            event.get("user"),

            "token":
            event.get("token"),

            "timestamp":
            event.get("timestamp")
        }