import asyncio

class ScoreWorker:

    async def run(self):

        while True:

            print(
                "Updating scores..."
            )

            await asyncio.sleep(
                15
            )