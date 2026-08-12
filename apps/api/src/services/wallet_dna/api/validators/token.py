###############################################################################
# Imports
###############################################################################

from __future__ import annotations

###############################################################################
# Constants
###############################################################################

MIN_TOKEN_LENGTH = 32
MAX_TOKEN_LENGTH = 44

BASE58_ALPHABET = set(
    "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
)

###############################################################################
# Token Validation
###############################################################################


def validate_token(
    token: str,
) -> bool:
    """
    Validate token mint address.
    """

    if not token:
        return False

    token = normalize_token(token)

    return (
        token_length(token)
        and is_valid_mint(token)
    )


###############################################################################


def validate_mint(
    mint: str,
) -> bool:
    """
    Validate Solana mint.
    """

    return validate_token(mint)


###############################################################################


def normalize_token(
    token: str,
) -> str:
    """
    Normalize token string.
    """

    return token.strip()


###############################################################################


def token_exists(
    token: str,
) -> bool:
    """
    Placeholder token existence check.
    """

    return validate_token(token)


###############################################################################


def verify_metadata(
    metadata: dict,
) -> bool:
    """
    Basic metadata verification.
    """

    required = {
        "name",
        "symbol",
    }

    return required.issubset(metadata.keys())


###############################################################################
# Runtime
###############################################################################


def diagnostics():
    """
    Validator diagnostics.
    """

    return {
        "validator": "token",
        "mint_validation": True,
    }


###############################################################################


def summary():
    """
    Validator summary.
    """

    return {
        "min_length": MIN_TOKEN_LENGTH,
        "max_length": MAX_TOKEN_LENGTH,
    }


###############################################################################
# Utilities
###############################################################################


def token_length(
    token: str,
) -> bool:
    """
    Validate token length.
    """

    return MIN_TOKEN_LENGTH <= len(token) <= MAX_TOKEN_LENGTH


###############################################################################


def is_valid_mint(
    mint: str,
) -> bool:
    """
    Check Base58 mint encoding.
    """

    return all(
        char in BASE58_ALPHABET
        for char in mint
    )