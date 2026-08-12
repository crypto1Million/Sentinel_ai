from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError


# ============================================================
# Configuration
# ============================================================

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "CHANGE_ME_IN_PRODUCTION",
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_EXPIRE_DAYS = 30


# ============================================================
# Exception
# ============================================================

class JWTException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


# ============================================================
# Helpers
# ============================================================

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# ============================================================
# Token Creation
# ============================================================

def create_access_token(
    user_id: str,
    email: str | None = None,
    username: str | None = None,
    roles: list[str] | None = None,
    permissions: list[str] | None = None,
    expires_delta: timedelta | None = None,
) -> str:

    expire = utc_now() + (
        expires_delta
        or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": user_id,
        "email": email,
        "username": username,
        "roles": roles or [],
        "permissions": permissions or [],
        "type": "access",
        "iat": utc_now(),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_refresh_token(
    user_id: str,
    expires_delta: timedelta | None = None,
) -> str:

    expire = utc_now() + (
        expires_delta
        or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": utc_now(),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ============================================================
# Decode
# ============================================================

def decode_token(token: str) -> dict[str, Any]:

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except ExpiredSignatureError:
        raise JWTException("Token expired.")

    except InvalidTokenError:
        raise JWTException("Invalid token.")


# ============================================================
# Verification
# ============================================================

def verify_access_token(
    token: str,
) -> dict[str, Any]:

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise JWTException("Access token required.")

    return payload


def verify_refresh_token(
    token: str,
) -> dict[str, Any]:

    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise JWTException("Refresh token required.")

    return payload


# ============================================================
# Refresh
# ============================================================

def generate_new_access_token(
    refresh_token: str,
) -> str:

    payload = verify_refresh_token(refresh_token)

    return create_access_token(
        user_id=payload["sub"],
    )


# ============================================================
# User Helpers
# ============================================================

def get_user_id(
    token: str,
) -> str:

    payload = verify_access_token(token)

    return payload["sub"]


def get_username(
    token: str,
) -> str | None:

    return verify_access_token(token).get("username")


def get_email(
    token: str,
) -> str | None:

    return verify_access_token(token).get("email")


def get_roles(
    token: str,
) -> list[str]:

    return verify_access_token(token).get("roles", [])


def get_permissions(
    token: str,
) -> list[str]:

    return verify_access_token(token).get(
        "permissions",
        [],
    )


# ============================================================
# Authorization
# ============================================================

def has_role(
    token: str,
    role: str,
) -> bool:

    return role in get_roles(token)


def has_permission(
    token: str,
    permission: str,
) -> bool:

    return permission in get_permissions(token)


# ============================================================
# Token Metadata
# ============================================================

def token_expiration(
    token: str,
):

    return decode_token(token)["exp"]


def token_type(
    token: str,
):

    return decode_token(token)["type"]


def is_token_expired(
    token: str,
) -> bool:

    try:
        decode_token(token)
        return False

    except JWTException:
        return True


# ============================================================
# Bearer Extraction
# ============================================================

def extract_bearer_token(
    authorization: str,
) -> str:

    if not authorization:
        raise JWTException(
            "Missing Authorization header."
        )

    if not authorization.startswith("Bearer "):
        raise JWTException(
            "Invalid Authorization header."
        )

    return authorization.replace(
        "Bearer ",
        "",
    )


# ============================================================
# Optional Debug
# ============================================================

if __name__ == "__main__":

    access = create_access_token(
        user_id="12345",
        username="aditya",
        email="user@example.com",
        roles=["admin"],
        permissions=["trade", "billing"],
    )

    refresh = create_refresh_token(
        user_id="12345",
    )

    print(access)
    print(refresh)

    print(verify_access_token(access))
    print(verify_refresh_token(refresh))