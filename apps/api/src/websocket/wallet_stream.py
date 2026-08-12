import asyncio

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from websocket.manager import manager


router = APIRouter()


@router.websocket(
    "/ws/wallets"
)
async def wallet_stream(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            data = {

                "type":
                "wallet_update",

                "wallet":
                "ABC123",

                "classification":
                "SMART_MONEY",

                "action":
                "BUY"
            }

            await websocket.send_json(
                data
            )

            await asyncio.sleep(3)

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )