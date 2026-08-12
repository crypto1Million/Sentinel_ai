import asyncio

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from websocket.manager import manager


router = APIRouter()


@router.websocket(
    "/ws/tokens"
)
async def token_stream(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            data = {

                "type":
                "token_update",

                "market_cap":
                100000,

                "volume":
                50000,

                "holders":
                1200
            }

            await websocket.send_json(
                data
            )

            await asyncio.sleep(2)

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )