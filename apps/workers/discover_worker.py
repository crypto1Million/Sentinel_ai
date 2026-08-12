import asyncio

class DiscoverWorker:

    async def run(self):

        while True:

            print(
                "Updating discover..."
            )

            await asyncio.sleep(
                15
            )