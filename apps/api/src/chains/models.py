from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class Chain(str, Enum):
    SOLANA = "solana"
    BASE = "base"
    ETHEREUM = "ethereum"
    BNB = "bnb"
    ROBINHOOD = "robinhood"


class ChainType(str, Enum):
    SOLANA = "solana"
    EVM = "evm"


@dataclass(frozen=True)
class ChainConfig:
    id: Chain
    name: str
    chain_type: ChainType
    chain_id: int | None
    native_symbol: str
    rpc_env: str
    explorer_url: str
    enabled: bool = True


class ChainAdapter(Protocol):
    config: ChainConfig

    async def quote(
        self,
        input_token: str,
        output_token: str,
        amount: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        ...

    async def execute(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        ...