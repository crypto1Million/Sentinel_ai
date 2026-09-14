from __future__ import annotations

from typing import Any

from web3 import Web3

from config.settings import get_settings
from chains.models import ChainConfig


ERC20_ABI: list[dict[str, Any]] = [
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
        "stateMutability": "view",
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
        "stateMutability": "view",
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
        "stateMutability": "view",
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
        "stateMutability": "view",
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
        "stateMutability": "view",
        "type": "function",
    },
]


class EVMClient:
    def __init__(
        self,
        config: ChainConfig,
    ) -> None:
        self.config = config

        settings = get_settings()

        rpc_url = getattr(
            settings,
            config.rpc_env,
            None,
        )

        if not rpc_url:
            raise RuntimeError(
                f"{config.rpc_env} is not configured"
            )

        self.w3 = Web3(
            Web3.HTTPProvider(
                rpc_url,
                request_kwargs={
                    "timeout": 15
                },
            )
        )

    def ensure_connected(self) -> None:
        if not self.w3.is_connected():
            raise RuntimeError(
                f"{self.config.name} RPC is unavailable"
            )

        if (
            self.config.chain_id is not None
            and self.w3.eth.chain_id
            != self.config.chain_id
        ):
            raise RuntimeError(
                f"{self.config.name} RPC returned "
                f"chain ID {self.w3.eth.chain_id}; "
                f"expected {self.config.chain_id}"
            )

    async def health(self) -> dict[str, Any]:
        connected = self.w3.is_connected()

        chain_id = (
            self.w3.eth.chain_id
            if connected
            else None
        )

        block_number = (
            self.w3.eth.block_number
            if connected
            else None
        )

        return {
            "chain": self.config.id.value,
            "connected": connected,
            "chain_id": chain_id,
            "expected_chain_id": self.config.chain_id,
            "block_number": block_number,
        }

    def checksum(
        self,
        address: str,
    ) -> str:
        return Web3.to_checksum_address(
            address
        )

    def native_balance(
        self,
        wallet: str,
    ) -> int:
        self.ensure_connected()

        return self.w3.eth.get_balance(
            self.checksum(wallet)
        )

    def token_metadata(
        self,
        token: str,
    ) -> dict[str, Any]:
        self.ensure_connected()

        address = self.checksum(token)

        code = self.w3.eth.get_code(address)

        if len(code) <= 2:
            raise ValueError(
                "Address is not a deployed contract"
            )

        contract = self.w3.eth.contract(
            address=address,
            abi=ERC20_ABI,
        )

        def safe_call(
            name: str,
            default: Any,
        ) -> Any:
            try:
                return getattr(
                    contract.functions,
                    name,
                )().call()
            except Exception:
                return default

        return {
            "chain": self.config.id.value,
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
            "block_number": (
                self.w3.eth.block_number
            ),
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