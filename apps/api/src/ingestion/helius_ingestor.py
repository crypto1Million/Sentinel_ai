import httpx
import os
from typing import Dict


class HeliusIngestor:

    def __init__(self):

        self.api_key = os.getenv(
            "HELIUS_API_KEY"
        )

        self.base_url = (
            "https://api.helius.xyz/v0"
        )

    async def get_wallet(
        self,
        wallet: str
    ) -> Dict:

        try:

            url = (

                f"{self.base_url}/addresses/"
                f"{wallet}/balances"

                f"?api-key={self.api_key}"

            )

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url
                )

                response.raise_for_status()

                return response.json()

        except Exception as e:

            print(
                f"Helius Error: {e}"
            )

            return {}