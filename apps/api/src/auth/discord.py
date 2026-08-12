"""
apps/api/src/auth/discord.py

Discord OAuth Authentication
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

DISCORD_CLIENT_ID = os.getenv(
    "DISCORD_CLIENT_ID",
    "",
)

DISCORD_CLIENT_SECRET = os.getenv(
    "DISCORD_CLIENT_SECRET",
    "",
)

DISCORD_REDIRECT_URI = os.getenv(
    "DISCORD_REDIRECT_URI",
    "http://localhost:8000/auth/discord/callback",
)

DISCORD_AUTH_URL = (
    "https://discord.com/api/oauth2/authorize"
)

DISCORD_TOKEN_URL = (
    "https://discord.com/api/oauth2/token"
)

DISCORD_USER_URL = (
    "https://discord.com/api/users/@me"
)


# ============================================================
# Authorization URL
# ============================================================

def get_discord_auth_url(
    state: str,
) -> str:

    return (
        f"{DISCORD_AUTH_URL}"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify%20email"
        f"&state={state}"
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
            DISCORD_TOKEN_URL,
            data={
                "client_id": DISCORD_CLIENT_ID,
                "client_secret": DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": DISCORD_REDIRECT_URI,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discord token exchange failed.",
        )

    return response.json()


# ============================================================
# Get User
# ============================================================

async def get_discord_user(
    access_token: str,
) -> dict[str, Any]:

    async with httpx.AsyncClient() as client:

        response = await client.get(
            DISCORD_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to fetch Discord profile.",
        )

    return response.json()


# ============================================================
# Avatar
# ============================================================

def avatar_url(
    user_id: str,
    avatar: str | None,
) -> str | None:

    if not avatar:
        return None

    return (
        f"https://cdn.discordapp.com/avatars/"
        f"{user_id}/{avatar}.png"
    )


# ============================================================
# Normalize User
# ============================================================

def normalize_discord_user(
    discord_user: dict[str, Any],
) -> dict[str, Any]:

    return {
        "provider": "discord",

        "provider_id": discord_user.get("id"),

        "username": discord_user.get("username"),

        "global_name": discord_user.get(
            "global_name"
        ),

        "discriminator": discord_user.get(
            "discriminator"
        ),

        "email": discord_user.get(
            "email"
        ),

        "verified": discord_user.get(
            "verified",
            False,
        ),

        "locale": discord_user.get(
            "locale"
        ),

        "avatar": avatar_url(
            discord_user.get("id"),
            discord_user.get("avatar"),
        ),

        "banner": discord_user.get(
            "banner"
        ),

        "accent_color": discord_user.get(
            "accent_color"
        ),

        "premium_type": discord_user.get(
            "premium_type"
        ),
    }


# ============================================================
# Complete Login
# ============================================================

async def authenticate_discord(
    code: str,
) -> dict[str, Any]:

    token_data = await exchange_code_for_token(
        code
    )

    access_token = token_data["access_token"]

    discord_user = await get_discord_user(
        access_token
    )

    return normalize_discord_user(
        discord_user
    )