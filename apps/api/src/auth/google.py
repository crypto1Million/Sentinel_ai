"""
apps/api/src/auth/google.py

Google OAuth Authentication
Sentinel AI
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import HTTPException, status

# ============================================================
# Configuration
# ============================================================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

GOOGLE_CLIENT_SECRET = os.getenv(
    "GOOGLE_CLIENT_SECRET",
    "",
)

GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI",
    "http://localhost:8000/auth/google/callback",
)

GOOGLE_AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
)

GOOGLE_TOKEN_URL = (
    "https://oauth2.googleapis.com/token"
)

GOOGLE_USERINFO_URL = (
    "https://openidconnect.googleapis.com/v1/userinfo"
)


# ============================================================
# Authorization URL
# ============================================================

def get_google_auth_url(
    state: str,
) -> str:
    return (
        f"{GOOGLE_AUTH_URL}"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&state={state}"
        f"&access_type=offline"
        f"&prompt=consent"
    )


# ============================================================
# Exchange Code
# ============================================================

async def exchange_code_for_token(
    code: str,
) -> dict[str, Any]:

    async with httpx.AsyncClient() as client:

        response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
                "code": code,
            },
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google token exchange failed.",
        )

    return response.json()


# ============================================================
# User Info
# ============================================================

async def get_google_user(
    access_token: str,
) -> dict[str, Any]:

    async with httpx.AsyncClient() as client:

        response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to fetch Google profile.",
        )

    return response.json()


# ============================================================
# Normalize User
# ============================================================

def normalize_google_user(
    google_user: dict[str, Any],
) -> dict[str, Any]:

    return {
        "provider": "google",
        "provider_id": google_user.get("sub"),
        "email": google_user.get("email"),
        "email_verified": google_user.get(
            "email_verified",
            False,
        ),
        "name": google_user.get("name"),
        "first_name": google_user.get(
            "given_name"
        ),
        "last_name": google_user.get(
            "family_name"
        ),
        "picture": google_user.get(
            "picture"
        ),
        "locale": google_user.get(
            "locale"
        ),
    }


# ============================================================
# Login Flow
# ============================================================

async def authenticate_google(
    code: str,
) -> dict[str, Any]:

    token_data = await exchange_code_for_token(
        code,
    )

    access_token = token_data["access_token"]

    google_user = await get_google_user(
        access_token,
    )

    return normalize_google_user(
        google_user,
    )