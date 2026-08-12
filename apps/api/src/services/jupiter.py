import httpx


class JupiterClient:

    BASE_URL = "https://quote-api.jup.ag/v6"


    async def quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int
    ):

        url = (
            f"{self.BASE_URL}/quote"
            f"?inputMint={input_mint}"
            f"&outputMint={output_mint}"
            f"&amount={amount}"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            return response.json()