from __future__ import annotations

from fastapi import APIRouter, WebSocket
from fastapi import WebSocketDisconnect

from realtime.bus import get_realtime_bus


router = APIRouter()


@router.websocket(
    "/ws/tokens"
)
async def token_stream(
    websocket: WebSocket,
) -> None:
    await websocket.accept()

    bus = get_realtime_bus()

    try:
        async for event in bus.subscribe(
            event_types={
                "token.updated",
                "pool.updated",
                "launchpad.detected",
            }
        ):
            await websocket.send_json(
                event.to_wire()
            )

    except WebSocketDisconnect:
        return

    except Exception:
        # Client disconnects or transport errors should
        # not terminate the entire API process.
        try:
            await websocket.close(
                code=1011
            )
        except Exception:
            pass