class FreezeChecker:

    def check(
        self,
        freeze_authority: bool
    ):

        return {

            "freeze_enabled":
            freeze_authority,

            "risk":
            80 if freeze_authority else 0
        }