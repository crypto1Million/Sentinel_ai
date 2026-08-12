import asyncio

class PortfolioWorker:

    async def run(self):

        while True:

            print(
                "Updating portfolio..."
            )

            await asyncio.sleep(
                10
            )