from __future__ import annotations

import asyncio
import logging
import re
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from realtime.bus import get_realtime_bus

logger = logging.getLogger("sentinel.websocket")
router = APIRouter()

CLIENT_EVENT_TYPES = {
    "token.updated", "wallet.updated", "score.updated", "alert.created",
    "pool.updated", "launchpad.detected", "rug.updated",
    "market_intelligence.updated", "wallet_dna.updated", "j7.updated",
    "narrative.updated",
}
CURSOR_PATTERN = re.compile(r"^[0-9]+-[0-9]+$")


@router.websocket("/ws/events")
async def events_stream(websocket: WebSocket) -> None:
    bus = get_realtime_bus()
    origin = websocket.headers.get("origin")
    if not origin or origin not in bus.settings.CORS_ORIGINS:
        await websocket.close(code=4403, reason="Origin not allowed")
        return

    ticket = websocket.query_params.get("ticket")
    if not ticket:
        await websocket.close(code=4401, reason="Authentication required")
        return

    ticket_key = f"{bus.settings.REDIS_STREAM_PREFIX}:ws-ticket:{ticket}"
    user_id = await bus.redis.getdel(ticket_key)
    if not user_id:
        await websocket.close(code=4401, reason="Invalid or expired ticket")
        return

    # Validate the replay cursor before subscribing; never interpolate arbitrary input.
    last_id = websocket.query_params.get("last_id") or "$"
    if last_id != "$" and not CURSOR_PATTERN.fullmatch(last_id):
        last_id = "$"

    await websocket.accept()

    async def forward_events() -> None:
        async for event in bus.subscribe(event_types=CLIENT_EVENT_TYPES, last_id=last_id):
            # Private events must be explicitly addressed to this authenticated user.
            if event.visibility == "private" and event.recipient_user_id != str(user_id):
                continue
            if event.recipient_user_id and event.recipient_user_id != str(user_id):
                continue
            await websocket.send_json(event.to_wire())

    async def watch_disconnect() -> None:
        while True:
            message = await websocket.receive()
            if message.get("type") == "websocket.disconnect":
                return

    event_task = asyncio.create_task(forward_events())
    disconnect_task = asyncio.create_task(watch_disconnect())
    try:
        done, _pending = await asyncio.wait(
            {event_task, disconnect_task},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in done:
            task.result()
    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        raise
    except Exception:
        logger.exception("Realtime WebSocket stream failed")
        try:
            await websocket.close(code=1011, reason="Realtime stream unavailable")
        except Exception:
            pass
    finally:
        for task in (event_task, disconnect_task):
            if not task.done():
                task.cancel()
        await asyncio.gather(event_task, disconnect_task, return_exceptions=True)
