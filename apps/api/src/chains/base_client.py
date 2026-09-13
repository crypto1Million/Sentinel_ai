from __future__ import annotations

from typing import Any

from web3 import Web3

from config.settings import get_settings


ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string",
            }
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string",
            }
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8",
            }
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256",
            }
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "account",
                "type": "address",
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "",
                "type": "uint256",
            }
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "name": "",
                "type": "address",
            }
        ],
        "type": "function",
    },
]


ZERO_ADDRESS = (
    "0x0000000000000000000000000000000000000000"
)


class BaseClient:
    def __init__(self) -> None:
        settings = get_settings()

        rpc_url = (
            settings.BASE_RPC_URL
            or "https://mainnet.base.org"
        )

        self.w3 = Web3(
            Web3.HTTPProvider(
                rpc_url,
                request_kwargs={
                    "timeout": 10,
                },
            )
        )

    def health(self) -> dict[str, Any]:
        connected = self.w3.is_connected()

        chain_id = None

        if connected:
            chain_id = self.w3.eth.chain_id

        return {
            "connected": connected,
            "chain_id": chain_id,
            "expected_chain_id": 8453,
        }

    def ensure_connected(self) -> None:
        health = self.health()

        if not health["connected"]:
            raise RuntimeError(
                "Unable to connect to Base RPC"
            )

        if health["chain_id"] != 8453:
            raise RuntimeError(
                "Base RPC returned an unexpected chain ID"
            )

    def checksum(
        self,
        address: str,
    ) -> str:
        return Web3.to_checksum_address(address)

    def token_metadata(
        self,
        token: str,
    ) -> dict[str, Any]:
        self.ensure_connected()

        address = self.checksum(token)

        if len(self.w3.eth.get_code(address)) <= 2:
            raise ValueError(
                "Address is not a deployed contract"
            )

        contract = self.w3.eth.contract(
            address=address,
            abi=ERC20_ABI,
        )

        def safe_call(
            method_name: str,
            default: Any,
        ) -> Any:
            try:
                return getattr(
                    contract.functions,
                    method_name,
                )().call()
            except Exception:
                return default

        return {
            "chain": "base",
            "address": address,
            "name": safe_call(
                "name",
                "Unknown Token",
            ),
            "symbol": safe_call(
                "symbol",
                "UNKNOWN",
            ),
            "decimals": int(
                safe_call(
                    "decimals",
                    18,
                )
            ),
            "total_supply": str(
                safe_call(
                    "totalSupply",
                    0,
                )
            ),
            "owner": safe_call(
                "owner",
                None,
            ),
            "block_number": self.w3.eth.block_number,
        }

    def token_balance(
        self,
        token: str,
        wallet: str,
    ) -> int:
        self.ensure_connected()

        contract = self.w3.eth.contract(
            address=self.checksum(token),
            abi=ERC20_ABI,
        )

        return int(
            contract.functions.balanceOf(
                self.checksum(wallet)
            ).call()
        )

    def get_code(
        self,
        address: str,
    ) -> bytes:
        self.ensure_connected()

        return self.w3.eth.get_code(
            self.checksum(address)
        )