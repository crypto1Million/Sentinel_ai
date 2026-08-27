from enum import Enum
from dataclasses import dataclass


class ChainType(str, Enum):
    SOLANA = "solana"
    EVM = "evm"


class Chain(str, Enum):
    SOLANA = "solana"
    ETHEREUM = "ethereum"
    BASE = "base"
    BNB = "bnb"
    ROBINHOOD = "robinhood"


@dataclass(frozen=True)
class ChainConfig:
    id: Chain
    name: str
    chain_type: ChainType
    chain_id: int | None
    native_symbol: str
    rpc_env: str
    explorer_url: str