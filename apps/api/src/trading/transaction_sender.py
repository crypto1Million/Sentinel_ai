class TransactionSender:

    async def send(
        self,
        tx
    ):

        return {

            "success":
            True,

            "signature":
            "mock_signature",

            "transaction":
            tx
        }