from __future__ import annotations

from typing import Any, Callable

from web3 import Web3

from app.chains.evm import EVMChainClient
from app.chains.models import Chain, ChainType
from app.chains.registry import get_chain


ClientFactory = Callable[[Chain], EVMChainClient]


class TokenService:
    """
    Token metadata service for registered EVM chains.

    Uses the existing Sentinel EVMChainClient and chain registry.

    Supported EVM networks:
        - Ethereum
        - Base
        - BNB
        - Robinhood

    Solana requires a separate Solana token client.
    """

    def __init__(
        self,
        client_factory: ClientFactory | None = None,
    ) -> None:

        self.client_factory = (
            client_factory or EVMChainClient
        )

    @staticmethod
    def _resolve_chain(
        chain: Chain | str,
    ) -> Chain:

        if isinstance(chain, Chain):
            return chain

        try:
            return Chain(
                str(chain).strip().lower()
            )

        except ValueError as exc:
            raise ValueError(
                f"Unsupported chain: {chain}"
            ) from exc

    def get_token_metadata(
        self,
        chain: Chain | str,
        address: str,
    ) -> dict[str, Any]:
        """
        Retrieve token metadata from the selected EVM chain.

        Returns:
            chain
            chain_name
            address
            name
            symbol
            decimals
            total_supply_raw
            explorer_url
        """

        selected_chain = self._resolve_chain(chain)

        config = get_chain(selected_chain)

        if config.chain_type != ChainType.EVM:
            raise NotImplementedError(
                "Solana token metadata requires a "
                "dedicated Solana client."
            )

        if not Web3.is_address(address):
            raise ValueError(
                "Invalid EVM token contract address."
            )

        checksum_address = Web3.to_checksum_address(
            address
        )

        client = self.client_factory(selected_chain)

        metadata = client.get_token_metadata(
            checksum_address
        )

        return {
            "chain": selected_chain.value,
            "chain_name": config.name,
            "address": metadata["address"],
            "name": metadata["name"],
            "symbol": metadata["symbol"],
            "decimals": metadata["decimals"],
            "total_supply_raw": metadata["total_supply"],
            "explorer_url": (
                f"{config.explorer_url.rstrip('/')}"
                f"/token/{checksum_address}"
            ),
        }