###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from passlib.context import CryptContext

from fastapi import HTTPException, status

from pydantic import BaseModel

###############################################################################
# Internal Configuration
###############################################################################

from wallet_dna.api.config import APIConfig

###############################################################################
# Constants
###############################################################################

JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_EXPIRE_DAYS = 30

API_KEY_LENGTH = 64

NONCE_LENGTH = 32

CSRF_TOKEN_LENGTH = 32

PASSWORD_SCHEME = "bcrypt"

###############################################################################
# Configuration
###############################################################################

config = APIConfig()

JWT_SECRET_KEY = config.JWT_SECRET_KEY

JWT_REFRESH_SECRET = config.JWT_REFRESH_SECRET

pwd_context = CryptContext(

    schemes=[PASSWORD_SCHEME],

    deprecated="auto",

)

UTC = timezone.utc

###############################################################################
# Password Utilities
###############################################################################

def generate_salt(
    length: int = 32,
) -> str:
    """
    Generate a cryptographically secure salt.
    """

    return secrets.token_hex(length)


###############################################################################


def hash_password(
    password: str,
) -> str:
    """
    Hash a plaintext password.
    """

    return pwd_context.hash(password)


###############################################################################


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against
    its stored hash.
    """

    try:

        return pwd_context.verify(

            plain_password,

            hashed_password,

        )

    except Exception:

        return False

###############################################################################
# JWT Utilities
###############################################################################

def create_access_token(
    subject: str,
    claims: dict[str, Any] | None = None,
) -> str:
    """
    Create JWT access token.
    """

    payload = {

        "sub": subject,

        "type": "access",

        "iat": datetime.now(UTC),

        "exp": datetime.now(UTC)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),

    }

    if claims:

        payload.update(claims)

    return jwt.encode(

        payload,

        JWT_SECRET_KEY,

        algorithm=JWT_ALGORITHM,

    )


###############################################################################


def create_refresh_token(
    subject: str,
) -> str:
    """
    Create JWT refresh token.
    """

    payload = {

        "sub": subject,

        "type": "refresh",

        "iat": datetime.now(UTC),

        "exp": datetime.now(UTC)
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),

    }

    return jwt.encode(

        payload,

        JWT_REFRESH_SECRET,

        algorithm=JWT_ALGORITHM,

    )


###############################################################################


def decode_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode JWT without validation wrapper.
    """

    return jwt.decode(

        token,

        JWT_SECRET_KEY,

        algorithms=[JWT_ALGORITHM],

    )


###############################################################################


def verify_token(
    token: str,
) -> dict[str, Any]:
    """
    Verify JWT token.
    """

    try:

        return decode_token(token)

    except jwt.ExpiredSignatureError:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Token expired.",

        )

    except jwt.InvalidTokenError:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token.",

        )


###############################################################################


def token_expired(
    payload: dict[str, Any],
) -> bool:
    """
    Check token expiration.
    """

    exp = payload.get("exp")

    if exp is None:

        return True

    if isinstance(exp, datetime):

        return exp < datetime.now(UTC)

    return datetime.fromtimestamp(

        exp,

        tz=UTC,

    ) < datetime.now(UTC)


###############################################################################


def revoke_token(
    token: str,
) -> bool:
    """
    Revoke JWT token.

    Actual revocation should be handled
    through Redis/database blacklist.
    """

    # TODO:
    # redis.set(f"revoked:{token}", True)

    return True

###############################################################################
# API Key Utilities
###############################################################################

def generate_api_key() -> str:
    """
    Generate a cryptographically secure API key.
    """

    return secrets.token_urlsafe(API_KEY_LENGTH)


###############################################################################


def hash_api_key(
    api_key: str,
) -> str:
    """
    Hash an API key before storage.
    """

    return hashlib.sha256(

        api_key.encode("utf-8")

    ).hexdigest()


###############################################################################


def verify_api_key(
    api_key: str,
    stored_hash: str,
) -> bool:
    """
    Verify an API key against its stored hash.
    """

    calculated_hash = hash_api_key(api_key)

    return secrets.compare_digest(

        calculated_hash,

        stored_hash,

    )


###############################################################################


def revoke_api_key(
    api_key_hash: str,
) -> bool:
    """
    Revoke an API key.

    Production implementation should
    mark the key as revoked in the DB.
    """

    # Example:
    # db.update(api_key_hash, revoked=True)

    return True


###############################################################################


def rotate_api_key(
    old_api_key_hash: str,
) -> tuple[str, str]:
    """
    Rotate an API key.

    Returns
    -------
    tuple
        (new_api_key, new_api_key_hash)
    """

    revoke_api_key(

        old_api_key_hash,

    )

    new_key = generate_api_key()

    new_hash = hash_api_key(

        new_key,

    )

    return (

        new_key,

        new_hash,

    )

###############################################################################
# Wallet Authentication
###############################################################################

def verify_wallet_signature(
    wallet_address: str,
    message: str,
    signature: str,
) -> bool:
    """
    Verify a wallet signature.

    NOTE:
    Replace this placeholder with actual
    Ed25519 verification using solders,
    pynacl, or another Solana library.
    """

    try:
        # TODO:
        # Verify detached Ed25519 signature
        # against the provided wallet address.
        return True

    except Exception:
        return False


###############################################################################


def verify_phantom(
    wallet_address: str,
    message: str,
    signature: str,
) -> bool:
    """
    Verify Phantom wallet signature.
    """

    return verify_wallet_signature(
        wallet_address,
        message,
        signature,
    )


###############################################################################


def verify_backpack(
    wallet_address: str,
    message: str,
    signature: str,
) -> bool:
    """
    Verify Backpack wallet signature.
    """

    return verify_wallet_signature(
        wallet_address,
        message,
        signature,
    )


###############################################################################


def verify_solflare(
    wallet_address: str,
    message: str,
    signature: str,
) -> bool:
    """
    Verify Solflare wallet signature.
    """

    return verify_wallet_signature(
        wallet_address,
        message,
        signature,
    )


###############################################################################


def verify_private_key(
    private_key: str,
) -> bool:
    """
    Validate private-key format.

    This only validates formatting.
    It must never persist the key.
    """

    try:

        return len(private_key) > 0

    except Exception:

        return False


###############################################################################


def create_wallet_session(
    wallet_address: str,
) -> dict:
    """
    Create wallet session.

    Returns an access token and metadata.
    """

    access_token = create_access_token(
        subject=wallet_address,
        claims={
            "wallet": wallet_address,
        },
    )

    refresh_token = create_refresh_token(
        subject=wallet_address,
    )

    return {

        "wallet": wallet_address,

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,

    }

###############################################################################
# OAuth Authentication
###############################################################################

from urllib.parse import urlencode


###############################################################################


def google_oauth() -> str:
    """
    Generate Google OAuth authorization URL.
    """

    params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    return (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urlencode(params)
    )


###############################################################################


def discord_oauth() -> str:
    """
    Generate Discord OAuth authorization URL.
    """

    params = {
        "client_id": config.DISCORD_CLIENT_ID,
        "redirect_uri": config.DISCORD_REDIRECT_URI,
        "response_type": "code",
        "scope": "identify email",
    }

    return (
        "https://discord.com/api/oauth2/authorize?"
        + urlencode(params)
    )


###############################################################################


def github_oauth() -> str:
    """
    Generate GitHub OAuth authorization URL.
    """

    params = {
        "client_id": config.GITHUB_CLIENT_ID,
        "redirect_uri": config.GITHUB_REDIRECT_URI,
        "scope": "read:user user:email",
    }

    return (
        "https://github.com/login/oauth/authorize?"
        + urlencode(params)
    )


###############################################################################


async def callback(
    provider: str,
    code: str,
) -> dict:
    """
    OAuth callback handler.
    """

    token = await exchange_token(
        provider=provider,
        code=code,
    )

    return {

        "provider": provider,

        "token": token,

        "status": "authenticated",

    }


###############################################################################


async def exchange_token(
    provider: str,
    code: str,
) -> dict:
    """
    Exchange authorization code
    for an access token.

    NOTE:
    Replace placeholder with HTTP request
    to provider token endpoint.
    """

    # TODO:
    # httpx.post(...)
    # validate response
    # fetch user profile

    return {

        "access_token": "provider_access_token",

        "provider": provider,

        "code": code,

    }

###############################################################################
# Permissions
###############################################################################

from fastapi import Depends, Header

###############################################################################


def require_user(
    token: str = Depends(get_current_user),
) -> dict:
    """
    Require authenticated user.
    """

    if not token:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Authentication required.",

        )

    return token


###############################################################################


def require_admin(
    user: dict = Depends(require_user),
) -> dict:
    """
    Require administrator.
    """

    if not user.get("is_admin", False):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Administrator access required.",

        )

    return user


###############################################################################


def require_wallet(
    user: dict = Depends(require_user),
) -> str:
    """
    Require connected wallet.
    """

    wallet = user.get("wallet")

    if wallet is None:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Wallet authentication required.",

        )

    return wallet


###############################################################################


def require_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> str:
    """
    Require valid API key.
    """

    # TODO:
    # Lookup API key hash from database
    # Verify key
    # Check revoked status

    if not x_api_key:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Missing API key.",

        )

    return x_api_key


###############################################################################


def check_permission(
    user: dict,
    permission: str,
) -> bool:
    """
    Check user permission.
    """

    permissions = user.get(

        "permissions",

        [],

    )

    if permission in permissions:

        return True

    if user.get(

        "is_admin",

        False,

    ):

        return True

    raise HTTPException(

        status_code=status.HTTP_403_FORBIDDEN,

        detail=f"Missing permission: {permission}",

    )

###############################################################################
# Session Management
###############################################################################

_ACTIVE_SESSIONS: dict[str, dict[str, Any]] = {}


###############################################################################


def create_session(
    user_id: str,
    wallet: str | None = None,
) -> dict:
    """
    Create a new authenticated session.
    """

    session_id = secrets.token_hex(32)

    access_token = create_access_token(
        subject=user_id,
        claims={"wallet": wallet},
    )

    refresh_token = create_refresh_token(
        subject=user_id,
    )

    session = {
        "session_id": session_id,
        "user_id": user_id,
        "wallet": wallet,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "created_at": datetime.now(UTC),
        "last_seen": datetime.now(UTC),
    }

    _ACTIVE_SESSIONS[session_id] = session

    return session


###############################################################################


def destroy_session(
    session_id: str,
) -> bool:
    """
    Destroy an existing session.
    """

    return _ACTIVE_SESSIONS.pop(session_id, None) is not None


###############################################################################


def refresh_session(
    session_id: str,
) -> dict:
    """
    Refresh access token.
    """

    session = _ACTIVE_SESSIONS.get(session_id)

    if session is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )

    session["access_token"] = create_access_token(
        subject=session["user_id"],
        claims={
            "wallet": session["wallet"],
        },
    )

    session["last_seen"] = datetime.now(UTC)

    return session


###############################################################################


def validate_session(
    session_id: str,
) -> bool:
    """
    Validate active session.
    """

    return session_id in _ACTIVE_SESSIONS


###############################################################################


def session_statistics() -> dict:
    """
    Session runtime statistics.
    """

    return {
        "active_sessions": len(_ACTIVE_SESSIONS),
        "timestamp": datetime.now(UTC).isoformat(),
    }

###############################################################################
# Security Helpers
###############################################################################

_NONCES: dict[str, datetime] = {}
_CSRF_TOKENS: set[str] = set()


def generate_nonce() -> str:
    nonce = secrets.token_urlsafe(NONCE_LENGTH)
    _NONCES[nonce] = datetime.now(UTC)
    return nonce


def verify_nonce(nonce: str, max_age: int = 300) -> bool:
    created = _NONCES.get(nonce)
    if created is None:
        return False

    valid = (datetime.now(UTC) - created).total_seconds() <= max_age

    if valid:
        _NONCES.pop(nonce, None)

    return valid


def generate_csrf() -> str:
    token = secrets.token_urlsafe(CSRF_TOKEN_LENGTH)
    _CSRF_TOKENS.add(token)
    return token


def verify_csrf(token: str) -> bool:
    if token in _CSRF_TOKENS:
        _CSRF_TOKENS.remove(token)
        return True
    return False


def generate_secret(length: int = 64) -> str:
    return secrets.token_hex(length)


def secure_compare(a: str, b: str) -> bool:
    return secrets.compare_digest(a, b)


###############################################################################
# Rate Limiting
###############################################################################

_RATE_LIMIT: dict[str, list[datetime]] = {}


def _check_limit(
    key: str,
    limit: int,
    window_seconds: int,
) -> bool:

    now = datetime.now(UTC)

    history = _RATE_LIMIT.setdefault(key, [])

    history[:] = [
        t for t in history
        if (now - t).total_seconds() < window_seconds
    ]

    if len(history) >= limit:
        return False

    history.append(now)

    return True


def login_limit(identifier: str) -> bool:
    return _check_limit(
        f"login:{identifier}",
        limit=5,
        window_seconds=300,
    )


def api_limit(identifier: str) -> bool:
    return _check_limit(
        f"api:{identifier}",
        limit=200,
        window_seconds=60,
    )


def wallet_limit(wallet: str) -> bool:
    return _check_limit(
        f"wallet:{wallet}",
        limit=50,
        window_seconds=60,
    )


def clear_limits() -> None:
    _RATE_LIMIT.clear()


###############################################################################
# Runtime
###############################################################################

def diagnostics() -> dict:

    return {

        "active_nonces": len(_NONCES),

        "csrf_tokens": len(_CSRF_TOKENS),

        "rate_limit_entries": len(_RATE_LIMIT),

        "timestamp": datetime.now(UTC).isoformat(),

    }


def security_statistics() -> dict:

    return {

        "nonces": len(_NONCES),

        "csrf": len(_CSRF_TOKENS),

        "rate_limits": len(_RATE_LIMIT),

    }


def reset_statistics() -> None:

    _NONCES.clear()

    _CSRF_TOKENS.clear()

    _RATE_LIMIT.clear()


###############################################################################
# Utilities
###############################################################################

def current_timestamp() -> datetime:
    return datetime.now(UTC)


def expiration_time(
    minutes: int,
) -> datetime:
    return datetime.now(UTC) + timedelta(minutes=minutes)


def random_string(
    length: int = 32,
) -> str:
    return secrets.token_urlsafe(length)


def summary() -> dict:

    return {

        "jwt_algorithm": JWT_ALGORITHM,

        "access_token_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,

        "refresh_token_days": REFRESH_TOKEN_EXPIRE_DAYS,

        "api_key_length": API_KEY_LENGTH,

        "active_sessions": len(_ACTIVE_SESSIONS),

        "statistics": security_statistics(),

    }                    