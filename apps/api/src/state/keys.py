from __future__ import annotations

import re

from state.models import ChainId


def _safe(value: str) -> str:
    """
    Restrict IDs to safe Redis-key components.
    """

    value = value.strip().lower()

    return re.sub(
        r"[^a-zA-Z0-9_.:-]",
        "_",
        value,
    )


def token_key(
    chain: ChainId,
    mint: str,
) -> str:
    return (
        f"sentinel:state:"
        f"token:"
        f"{_safe(chain.value)}:"
        f"{_safe(mint)}"
    )


def pool_key(
    chain: ChainId,
    pool_address: str,
) -> str:
    return (
        f"sentinel:state:"
        f"pool:"
        f"{_safe(chain.value)}:"
        f"{_safe(pool_address)}"
    )


def wallet_key(
    chain: ChainId,
    wallet_address: str,
) -> str:
    return (
        f"sentinel:state:"
        f"wallet:"
        f"{_safe(chain.value)}:"
        f"{_safe(wallet_address)}"
    )


def developer_key(
    chain: ChainId,
    developer_address: str,
) -> str:
    return (
        f"sentinel:state:"
        f"developer:"
        f"{_safe(chain.value)}:"
        f"{_safe(developer_address)}"
    )


def launchpad_key(
    chain: ChainId,
    launchpad_id: str,
) -> str:
    return (
        f"sentinel:state:"
        f"launchpad:"
        f"{_safe(chain.value)}:"
        f"{_safe(launchpad_id)}"
    )