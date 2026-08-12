class MintChecker:

    def check(
        self,
        mint_authority: bool
    ):

        return {

            "mint_enabled":
            mint_authority,

            "risk":
            100 if mint_authority else 0
        }