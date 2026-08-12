import httpx


class RaydiumClient:

    BASE_URL = "https://api-v3.raydium.io"


    async def get_pool(self, pool_id: str):

        url = (
            f"{self.BASE_URL}"
            f"/pools/info/ids"
            f"?ids={pool_id}"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            return response.json()


    async def get_token_pools(
        self,
        mint_address: str
    ):

        url = (
            f"{self.BASE_URL}"
            f"/pools/info/mint"
            f"?mint1={mint_address}"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            return response.json()