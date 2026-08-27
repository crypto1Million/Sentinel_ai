import os
from dotenv import load_dotenv

load_dotenv()

from .models import Chain, ChainConfig, ChainType


CHAINS: dict[Chain, ChainConfig] = {

    Chain.SOLANA: ChainConfig(
        id=Chain.SOLANA,
        name="Solana",
        chain_type=ChainType.SOLANA,
        chain_id=None,
        native_symbol="SOL",
        rpc_env="SOLANA_RPC_URL",
        explorer_url="https://solscan.io",
    ),

    Chain.ETHEREUM: ChainConfig(
        id=Chain.ETHEREUM,
        name="Ethereum",
        chain_type=ChainType.EVM,
        chain_id=1,
        native_symbol="ETH",
        rpc_env="ETHEREUM_RPC_URL",
        explorer_url="https://etherscan.io",
    ),

    Chain.BASE: ChainConfig(
        id=Chain.BASE,
        name="Base",
        chain_type=ChainType.EVM,
        chain_id=8453,
        native_symbol="ETH",
        rpc_env="BASE_RPC_URL",
        explorer_url="https://basescan.org",
    ),

    Chain.BNB: ChainConfig(
        id=Chain.BNB,
        name="BNB Smart Chain",
        chain_type=ChainType.EVM,
        chain_id=56,
        native_symbol="BNB",
        rpc_env="BNB_RPC_URL",
        explorer_url="https://bscscan.com",
    ),

    Chain.ROBINHOOD: ChainConfig(
        id=Chain.ROBINHOOD,
        name="Robinhood Chain",
        chain_type=ChainType.EVM,
        chain_id=4663,
        native_symbol="ETH",
        rpc_env="ROBINHOOD_RPC_URL",
        explorer_url="https://robinhoodchain.blockscout.com",
    ),
}


def get_chain(chain: Chain) -> ChainConfig:
    try:
        return CHAINS[chain]
    except KeyError:
        raise ValueError(f"Unsupported chain: {chain}")


def get_rpc_url(chain: Chain) -> str:
    config = get_chain(chain)

    rpc_url = os.getenv(config.rpc_env)

    if not rpc_url:
        raise RuntimeError(
            f"Missing RPC environment variable: {config.rpc_env}"
        )

    return rpc_url