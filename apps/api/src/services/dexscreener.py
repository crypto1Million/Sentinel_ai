import httpx


class DexScreenerClient:

    BASE_URL = "https://api.dexscreener.com/latest/dex"

    async def get_token(self, token_address: str):

        url = f"{self.BASE_URL}/tokens/{token_address}"

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            response.raise_for_status()

            return response.json()

    async def search(self, query: str):

        url = (
            f"https://api.dexscreener.com/latest/dex/search"
            f"?q={query}"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            response.raise_for_status()

            return response.json()