from __future__ import annotations

import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from auth.dependencies import get_current_payload
from realtime.bus import get_realtime_bus


router = APIRouter()


@router.post("/ticket")
async def create_realtime_ticket(
    payload: dict[str, Any] = Depends(get_current_payload),
) -> dict[str, Any]:
    """
    Exchange the app's JWT for a short-lived,
    single-use WebSocket ticket.
    """

    user_id = str(payload.get("sub") or "").strip()

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user identity is missing",
        )

    bus = get_realtime_bus()

    ticket = secrets.token_urlsafe(32)

    key = (
        f"{bus.settings.REDIS_STREAM_PREFIX}:"
        f"ws-ticket:{ticket}"
    )

    stored = await bus.redis.set(
        name=key,
        value=user_id,
        ex=30,
        nx=True,
    )

    if not stored:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not allocate a realtime ticket",
        )

    return {
        "ticket": ticket,
        "expires_in": 30,
    }