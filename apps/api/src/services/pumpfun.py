import httpx


class PumpFunClient:

    BASE_URL = "https://frontend-api.pump.fun"

    async def get_coin(self, mint: str):

        url = f"{self.BASE_URL}/coins/{mint}"

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            if response.status_code != 200:
                return None

            return response.json()

    async def get_featured(self):

        url = (
            f"{self.BASE_URL}/coins"
            "?offset=0&limit=50"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            return response.json()