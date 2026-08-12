import httpx
from typing import Dict


class JitoIngestor:

    BASE_URL = (
        "https://mainnet.block-engine.jito.wtf"
    )

    async def get_bundle_status(
        self,
        bundle_id: str
    ) -> Dict:

        try:

            payload = {

                "jsonrpc": "2.0",

                "id": 1,

                "method":
                "getBundleStatuses",

                "params": [

                    [bundle_id]

                ]
            }

            async with httpx.AsyncClient() as client:

                response = await client.post(

                    f"{self.BASE_URL}/api/v1",

                    json=payload

                )

                response.raise_for_status()

                return response.json()

        except Exception as e:

            print(
                f"Jito Error: {e}"
            )

            return {}