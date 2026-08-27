from decimal import Decimal
from web3 import Web3

from .models import Chain, ChainType
from .registry import get_chain, get_rpc_url


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
]


class EVMChainClient:

    def __init__(self, chain: Chain):
        config = get_chain(chain)

        if config.chain_type != ChainType.EVM:
            raise ValueError(
                f"{chain} is not an EVM chain"
            )

        self.chain = chain
        self.config = config

        self.w3 = Web3(
            Web3.HTTPProvider(
                get_rpc_url(chain),
                request_kwargs={
                    "timeout": 20
                },
            )
        )

        if not self.w3.is_connected():
            raise RuntimeError(
                f"Could not connect to {config.name}"
            )

        actual_chain_id = self.w3.eth.chain_id

        if actual_chain_id != config.chain_id:
            raise RuntimeError(
                f"Chain ID mismatch for {config.name}: "
                f"expected {config.chain_id}, "
                f"got {actual_chain_id}"
            )

    def latest_block(self) -> int:
        return self.w3.eth.block_number

    def get_native_balance(self, address: str) -> Decimal:
        address = Web3.to_checksum_address(address)

        balance = self.w3.eth.get_balance(address)

        return Decimal(
            self.w3.from_wei(balance, "ether")
        )

    def get_token_metadata(self, token_address: str) -> dict:
        token_address = Web3.to_checksum_address(
            token_address
        )

        contract = self.w3.eth.contract(
            address=token_address,
            abi=ERC20_ABI,
        )

        return {
            "address": token_address,
            "name": contract.functions.name().call(),
            "symbol": contract.functions.symbol().call(),
            "decimals": contract.functions.decimals().call(),
            "total_supply": str(
                contract.functions.totalSupply().call()
            ),
        }

    def get_transaction(self, tx_hash: str):
        return self.w3.eth.get_transaction(tx_hash)

    def get_transaction_receipt(self, tx_hash: str):
        return self.w3.eth.get_transaction_receipt(
            tx_hash
        )

    def get_block(self, block_number: int):
        return self.w3.eth.get_block(
            block_number,
            full_transactions=True,
        )