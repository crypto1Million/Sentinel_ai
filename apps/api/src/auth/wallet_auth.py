"""
apps/api/src/auth/wallet_auth.py

Wallet Authentication
Supports:

- Phantom
- Backpack
- Solflare
- Any Solana Wallet

Uses Ed25519 signature verification.
"""

from __future__ import annotations

import base64
import secrets
from typing import Any

from fastapi import HTTPException, status
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


# ============================================================
# Constants
# ============================================================

NONCE_LENGTH = 32


# ============================================================
# Nonce
# ============================================================

def generate_nonce() -> str:
    """
    Generates a random nonce for wallet login.
    """
    return secrets.token_urlsafe(NONCE_LENGTH)


# ============================================================
# Login Message
# ============================================================

def create_login_message(
    wallet_address: str,
    nonce: str,
) -> str:
    """
    Standard SIWS (Sign In With Solana) message.
    """

    return f"""
Sentinel AI Login

Wallet:
{wallet_address}

Nonce:
{nonce}

Sign this message to authenticate.

No blockchain transaction will occur.
"""


# ============================================================
# Signature Verification
# ============================================================

def verify_wallet_signature(
    wallet_address: str,
    message: str,
    signature: str,
) -> bool:
    """
    Verify Solana wallet signature.

    wallet_address -> base58 public key
    signature -> base64 signature
    """

    try:

        import base58

        public_key = base58.b58decode(
            wallet_address
        )

        verify_key = VerifyKey(public_key)

        verify_key.verify(
            message.encode(),
            base64.b64decode(signature),
        )

        return True

    except BadSignatureError:
        return False

    except Exception:
        return False


# ============================================================
# Authenticate Wallet
# ============================================================

def authenticate_wallet(
    wallet_address: str,
    message: str,
    signature: str,
) -> dict[str, Any]:

    verified = verify_wallet_signature(
        wallet_address,
        message,
        signature,
    )

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid wallet signature.",
        )

    return {
        "provider": "wallet",
        "wallet": wallet_address,
        "verified": True,
    }


# ============================================================
# Phantom
# ============================================================

def authenticate_phantom(
    wallet_address: str,
    message: str,
    signature: str,
):
    result = authenticate_wallet(
        wallet_address,
        message,
        signature,
    )

    result["wallet_provider"] = "phantom"

    return result


# ============================================================
# Backpack
# ============================================================

def authenticate_backpack(
    wallet_address: str,
    message: str,
    signature: str,
):
    result = authenticate_wallet(
        wallet_address,
        message,
        signature,
    )

    result["wallet_provider"] = "backpack"

    return result


# ============================================================
# Solflare
# ============================================================

def authenticate_solflare(
    wallet_address: str,
    message: str,
    signature: str,
):
    result = authenticate_wallet(
        wallet_address,
        message,
        signature,
    )

    result["wallet_provider"] = "solflare"

    return result


# ============================================================
# Wallet Metadata
# ============================================================

def wallet_profile(
    wallet_address: str,
) -> dict[str, Any]:
    """
    Placeholder for future Wallet DNA integration.
    """

    return {
        "wallet": wallet_address,

        "wallet_age_days": None,

        "wallet_score": None,

        "wallet_dna": None,

        "first_seen": None,

        "last_seen": None,

        "labels": [],

        "tags": [],
    }


# ============================================================
# Combined Login
# ============================================================

def wallet_login(
    provider: str,
    wallet_address: str,
    message: str,
    signature: str,
):

    provider = provider.lower()

    if provider == "phantom":
        return authenticate_phantom(
            wallet_address,
            message,
            signature,
        )

    if provider == "backpack":
        return authenticate_backpack(
            wallet_address,
            message,
            signature,
        )

    if provider == "solflare":
        return authenticate_solflare(
            wallet_address,
            message,
            signature,
        )

    return authenticate_wallet(
        wallet_address,
        message,
        signature,
    )