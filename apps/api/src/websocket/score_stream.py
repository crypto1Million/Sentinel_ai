from __future__ import annotations

from fastapi import APIRouter, WebSocket
from fastapi import WebSocketDisconnect

from realtime.bus import get_realtime_bus


router = APIRouter()


@router.websocket(
    "/ws/scores"
)
async def score_stream(
    websocket: WebSocket,
) -> None:
    await websocket.accept()

    bus = get_realtime_bus()

    try:
        async for event in bus.subscribe(
            event_types={
                "score.updated",
            }
        ):
            await websocket.send_json(
                event.to_wire()
            )

    except WebSocketDisconnect:
        return

    except Exception:
        try:
            await websocket.close(
                code=1011
            )
        except Exception:
            pass