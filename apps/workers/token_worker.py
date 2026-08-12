import asyncio

class TokenWorker:

    async def run(self):

        while True:

            print(
                "Updating tokens..."
            )

            await asyncio.sleep(
                10
            )