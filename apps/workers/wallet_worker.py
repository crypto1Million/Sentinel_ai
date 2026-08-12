import asyncio

class WalletWorker:

    async def run(self):

        while True:

            print(
                "Updating wallets..."
            )

            await asyncio.sleep(
                20
            )