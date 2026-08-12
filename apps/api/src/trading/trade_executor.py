from transaction_builder import TransactionBuilder
from transaction_sender import TransactionSender

class TradeExecutor:

    def __init__(self):

        self.builder = TransactionBuilder()

        self.sender = TransactionSender()

    async def execute(

        self,

        mint,

        side,

        amount
    ):

        tx = self.builder.build(

            mint,

            side,

            amount
        )

        result = await self.sender.send(
            tx
        )

        return result