import asyncio

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from websocket.manager import manager


router = APIRouter()


@router.websocket(
    "/ws/scores"
)
async def score_stream(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            data = {

                "type":
                "score_update",

                "token":
                "ROCHI",

                "sentinel_score":
                92,

                "grade":
                "S"
            }

            await websocket.send_json(
                data
            )

            await asyncio.sleep(5)

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )