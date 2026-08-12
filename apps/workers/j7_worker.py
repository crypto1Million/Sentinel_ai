import asyncio

class J7Worker:

    async def run(self):

        while True:

            print(
                "Checking J7 activity..."
            )

            await asyncio.sleep(
                5
            )