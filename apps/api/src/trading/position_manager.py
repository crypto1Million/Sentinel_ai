class PositionManager:

    def create_position(

        self,

        mint,

        entry,

        size
    ):

        return {

            "mint":
            mint,

            "entry":
            entry,

            "size":
            size,

            "status":
            "open"
        }

    def close_position(
        self,
        position
    ):

        position["status"] = "closed"

        return position