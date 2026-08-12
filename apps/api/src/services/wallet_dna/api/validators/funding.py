###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from decimal import Decimal
from typing import Any

###############################################################################
# Constants
###############################################################################

MIN_SIGNATURE_LENGTH = 64
MAX_SIGNATURE_LENGTH = 128

MAX_FUNDING_DEPTH = 50

###############################################################################
# Funding Validation
###############################################################################


def validate_funding_chain(
    chain: list[dict],
) -> bool:
    """
    Validate funding chain.
    """

    if not chain:
        return False

    return all(
        validate_transaction(tx)
        for tx in chain
    )


###############################################################################


def validate_transaction(
    transaction: dict,
) -> bool:
    """
    Validate funding transaction.
    """

    required = {
        "source",
        "destination",
        "signature",
        "amount",
    }

    if not required.issubset(transaction.keys()):
        return False

    return (
        validate_signature(
            transaction["signature"]
        )
        and validate_amount(
            transaction["amount"]
        )
    )


###############################################################################


def validate_signature(
    signature: str,
) -> bool:
    """
    Validate Solana transaction signature.
    """

    signature = normalize_signature(signature)

    return (
        MIN_SIGNATURE_LENGTH
        <= len(signature)
        <= MAX_SIGNATURE_LENGTH
    )


###############################################################################


def validate_depth(
    depth: int,
) -> bool:
    """
    Validate funding depth.
    """

    return 0 <= depth <= MAX_FUNDING_DEPTH


###############################################################################


def validate_amount(
    amount: Decimal | float | int,
) -> bool:
    """
    Validate funding amount.
    """

    return Decimal(str(amount)) >= 0


###############################################################################
# Runtime
###############################################################################


def diagnostics():
    """
    Validator diagnostics.
    """

    return {
        "validator": "funding",
        "max_depth": MAX_FUNDING_DEPTH,
    }


###############################################################################


def summary():
    """
    Validator summary.
    """

    return {
        "signature_length": (
            MIN_SIGNATURE_LENGTH,
            MAX_SIGNATURE_LENGTH,
        ),
        "max_depth": MAX_FUNDING_DEPTH,
    }


###############################################################################
# Utilities
###############################################################################


def normalize_signature(
    signature: str,
) -> str:
    """
    Normalize signature.
    """

    return signature.strip()


###############################################################################


def sanitize_chain(
    chain: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove invalid transactions.
    """

    return [
        tx
        for tx in chain
        if validate_transaction(tx)
    ]