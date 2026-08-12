import asyncio

from ingestion.token_ingestor import (
    TokenIngestor
)


class TokenScheduler:

    def __init__(self):

        self.ingestor = TokenIngestor()

    async def run(self):

        while True:

            try:

                print(
                    "Scanning for new tokens..."
                )

                #
                # Future:
                # PumpFun launch scanner
                # J7Tracker feed
                # Helius webhooks
                #

            except Exception as e:

                print(
                    "Scheduler Error:",
                    str(e)
                )

            await asyncio.sleep(10)