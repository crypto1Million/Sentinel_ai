###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Iterable

###############################################################################
# Constants
###############################################################################

BASE58_ALPHABET = set(
    "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
)

MIN_WALLET_LENGTH = 32
MAX_WALLET_LENGTH = 44

###############################################################################
# Wallet Validation
###############################################################################


def validate_wallet(
    wallet: str,
) -> bool:
    """
    Validate Solana wallet address.
    """

    if not wallet:
        return False

    wallet = normalize_wallet(wallet)

    return (
        wallet_length(wallet)
        and is_base58(wallet)
    )


###############################################################################


def validate_wallet_list(
    wallets: Iterable[str],
) -> list[str]:
    """
    Validate multiple wallets.
    """

    return [
        normalize_wallet(wallet)
        for wallet in wallets
        if validate_wallet(wallet)
    ]


###############################################################################


def normalize_wallet(
    wallet: str,
) -> str:
    """
    Normalize wallet string.
    """

    return wallet.strip()


###############################################################################


def wallet_exists(
    wallet: str,
) -> bool:
    """
    Placeholder existence check.
    """

    return validate_wallet(wallet)


###############################################################################


def wallet_checksum(
    wallet: str,
) -> bool:
    """
    Placeholder checksum verification.

    Solana Base58 addresses do not expose a
    separate checksum like Ethereum.
    """

    return validate_wallet(wallet)


###############################################################################
# Batch Validation
###############################################################################


def validate_batch(
    wallets: Iterable[str],
) -> list[str]:
    """
    Validate wallet batch.
    """

    return remove_duplicates(
        validate_wallet_list(wallets)
    )


###############################################################################


def remove_duplicates(
    wallets: Iterable[str],
) -> list[str]:
    """
    Remove duplicate wallets.
    """

    return list(dict.fromkeys(wallets))


###############################################################################
# Runtime
###############################################################################


def diagnostics():
    """
    Validator diagnostics.
    """

    return {
        "validator": "wallet",
        "base58": True,
    }


###############################################################################


def summary():
    """
    Validator summary.
    """

    return {
        "min_length": MIN_WALLET_LENGTH,
        "max_length": MAX_WALLET_LENGTH,
    }


###############################################################################
# Utilities
###############################################################################


def is_base58(
    value: str,
) -> bool:
    """
    Check Base58 encoding.
    """

    return all(
        char in BASE58_ALPHABET
        for char in value
    )


###############################################################################


def wallet_length(
    wallet: str,
) -> bool:
    """
    Validate wallet length.
    """

    return MIN_WALLET_LENGTH <= len(wallet) <= MAX_WALLET_LENGTH