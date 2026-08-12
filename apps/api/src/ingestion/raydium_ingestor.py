import httpx
from typing import Dict, List


class RaydiumIngestor:

    BASE_URL = "https://api-v3.raydium.io"

    async def fetch_pairs(
        self
    ) -> List[Dict]:

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    f"{self.BASE_URL}/pools/info/list"
                )

                response.raise_for_status()

                data = response.json()

                return data.get(
                    "data",
                    []
                )

        except Exception as e:

            print(
                f"Raydium Error: {e}"
            )

            return []