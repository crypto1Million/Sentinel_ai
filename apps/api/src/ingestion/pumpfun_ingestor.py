import httpx
from typing import List, Dict


class PumpFunIngestor:

    BASE_URL = "https://frontend-api.pump.fun"

    async def fetch_new_tokens(self) -> List[Dict]:

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    f"{self.BASE_URL}/coins"
                )

                response.raise_for_status()

                return response.json()

        except Exception as e:

            print(
                f"PumpFun Error: {e}"
            )

            return []

    async def normalize_token(
        self,
        token: Dict
    ) -> Dict:

        return {

            "address":
            token.get("mint"),

            "name":
            token.get("name"),

            "symbol":
            token.get("symbol"),

            "market_cap":
            token.get("usd_market_cap", 0),

            "source":
            "pumpfun"
        }