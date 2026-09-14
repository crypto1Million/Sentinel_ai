from __future__ import annotations

from chains.evm.adapter import EVMChainAdapter
from chains.models import (
    Chain,
    ChainAdapter,
)
from chains.registry import get_chain_config
from chains.solana.adapter import SolanaChainAdapter


def get_chain_adapter(
    chain: Chain,
) -> ChainAdapter:
    config = get_chain_config(chain)

    if chain == Chain.SOLANA:
        return SolanaChainAdapter(config)

    if chain in {
        Chain.BASE,
        Chain.ETHEREUM,
        Chain.BNB,
    }:
        return EVMChainAdapter(config)

    if chain == Chain.ROBINHOOD:
        raise ValueError(
            "Robinhood chain adapter is not enabled"
        )

    raise ValueError(
        f"No adapter for {chain.value}"
    )