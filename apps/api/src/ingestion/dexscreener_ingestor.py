import httpx
from typing import Dict


class DexScreenerIngestor:

    BASE_URL = (
        "https://api.dexscreener.com/latest"
    )

    async def fetch_token(
        self,
        mint: str
    ) -> Dict:

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(

                    f"{self.BASE_URL}/dex/tokens/{mint}"

                )

                response.raise_for_status()

                return response.json()

        except Exception as e:

            print(
                f"Dex Error: {e}"
            )

            return {}