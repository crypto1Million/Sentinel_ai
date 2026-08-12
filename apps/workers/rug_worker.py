import asyncio

class RugWorker:

    async def run(self):

        while True:

            print(
                "Updating rug radar..."
            )

            await asyncio.sleep(
                20
            )