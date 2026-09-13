from __future__ import annotations

from typing import Any

from chains.base_client import BaseClient
from config.settings import get_settings


FACTORY_ABI = [
    {
        "inputs": [
            {
                "name": "tokenA",
                "type": "address",
            },
            {
                "name": "tokenB",
                "type": "address",
            },
            {
                "name": "stable",
                "type": "bool",
            },
        ],
        "name": "getPool",
        "outputs": [
            {
                "name": "pool",
                "type": "address",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    }
]


ZERO_ADDRESS = (
    "0x0000000000000000000000000000000000000000"
)


class BaseDexDiscovery:
    def __init__(
        self,
        client: BaseClient | None = None,
    ) -> None:
        self.client = client or BaseClient()

        settings = get_settings()

        self.factory = (
            settings.AERODROME_FACTORY_ADDRESS
        )

        self.weth = (
            settings.BASE_WETH_ADDRESS
        )

        self.usdc = (
            settings.BASE_USDC_ADDRESS
        )

    def discover(
        self,
        token: str,
    ) -> list[dict[str, Any]]:
        w3 = self.client.w3

        factory = w3.eth.contract(
            address=w3.to_checksum_address(
                self.factory
            ),
            abi=FACTORY_ABI,
        )

        quotes = [
            ("WETH", self.weth),
            ("USDC", self.usdc),
        ]

        pools: list[dict[str, Any]] = []

        for quote_symbol, quote_address in quotes:
            for stable in (
                False,
                True,
            ):
                try:
                    pool = (
                        factory
                        .functions
                        .getPool(
                            w3.to_checksum_address(
                                token
                            ),
                            w3.to_checksum_address(
                                quote_address
                            ),
                            stable,
                        )
                        .call()
                    )

                    if pool.lower() == ZERO_ADDRESS.lower():
                        continue

                    pools.append(
                        {
                            "chain": "base",
                            "dex": "aerodrome",
                            "pool": pool,
                            "token": token,
                            "quote": quote_symbol,
                            "stable": stable,
                        }
                    )
                except Exception:
                    continue

        return pools