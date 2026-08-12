import httpx

class HeliusClient:

    def __init__(
        self,
        api_key
    ):

        self.api_key = api_key

    async def get_asset(
        self,
        mint
    ):

        url = (
            f"https://mainnet.helius-rpc.com"
            f"/?api-key={self.api_key}"
        )

        payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "getAsset",
            "params": {
                "id": mint
            }
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                url,
                json=payload
            )

            return response.json()