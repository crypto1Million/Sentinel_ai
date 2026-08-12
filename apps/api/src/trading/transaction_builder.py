import uuid

class TransactionBuilder:

    def build(

        self,

        token_mint,

        side,

        amount
    ):

        return {

            "id":
            str(uuid.uuid4()),

            "mint":
            token_mint,

            "side":
            side,

            "amount":
            amount
        }