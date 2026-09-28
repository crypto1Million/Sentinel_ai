from __future__ import annotations

from chains.models import (
    Chain,
    ChainConfig,
    ChainType,
)


CHAIN_CONFIGS: dict[Chain, ChainConfig] = {
    Chain.SOLANA: ChainConfig(
        id=Chain.SOLANA,
        name="Solana",
        chain_type=ChainType.SOLANA,
        chain_id=None,
        native_symbol="SOL",
        rpc_env="SOLANA_RPC_URL",
        explorer_url="https://solscan.io",
        enabled=True,
    ),

    Chain.BASE: ChainConfig(
        id=Chain.BASE,
        name="Base",
        chain_type=ChainType.EVM,
        chain_id=8453,
        native_symbol="ETH",
        rpc_env="BASE_RPC_URL",
        explorer_url="https://basescan.org",
        enabled=True,
    ),

    Chain.ETHEREUM: ChainConfig(
        id=Chain.ETHEREUM,
        name="Ethereum",
        chain_type=ChainType.EVM,
        chain_id=1,
        native_symbol="ETH",
        rpc_env="ETHEREUM_RPC_URL",
        explorer_url="https://etherscan.io",
        enabled=True,
    ),

    Chain.BNB: ChainConfig(
        id=Chain.BNB,
        name="BNB Chain",
        chain_type=ChainType.EVM,
        chain_id=56,
        native_symbol="BNB",
        rpc_env="BNB_RPC_URL",
        explorer_url="https://bscscan.com",
        enabled=True,
    ),

    Chain.ROBINHOOD: ChainConfig(
        id=Chain.ROBINHOOD,
        name="Robinhood Chain",
        chain_type=ChainType.EVM,
        chain_id=4663,
        native_symbol="ETH",
        rpc_env="ROBINHOOD_RPC_URL",
        explorer_url="https://robinhoodchain.blockscout.com",
        enabled=True,
    ),
}


def get_chain_config(
    chain: Chain,
) -> ChainConfig:
    config = CHAIN_CONFIGS.get(chain)

    if config is None:
        raise ValueError(
            f"Unsupported chain: {chain.value}"
        )

    if not config.enabled:
        raise ValueError(
            f"Chain is currently disabled: {chain.value}"
        )

    return config


def list_chains() -> list[ChainConfig]:
    return list(CHAIN_CONFIGS.values())