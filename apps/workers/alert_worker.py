import asyncio

class AlertWorker:

    async def run(self):

        while True:

            print(
                "Scanning alerts..."
            )

            await asyncio.sleep(
                5
            )