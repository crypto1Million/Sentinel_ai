import asyncio

class NarrativeWorker:

    async def run(self):

        while True:

            print(
                "Updating narratives..."
            )

            await asyncio.sleep(
                30
            )