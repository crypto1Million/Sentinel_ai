###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

###############################################################################
# WebSocket Router
###############################################################################

router = APIRouter()

###############################################################################
# Connection Manager
###############################################################################


class AlertsConnectionManager:
    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    ###########################################################################

    async def connect(
        self,
        channel: str,
        websocket: WebSocket,
    ):
        await websocket.accept()
        self.connections[channel].add(websocket)

    ###########################################################################

    async def disconnect(
        self,
        channel: str,
        websocket: WebSocket,
    ):
        self.connections[channel].discard(websocket)

        if not self.connections[channel]:
            self.connections.pop(channel, None)

    ###########################################################################

    async def subscribe_alerts(
        self,
        channel: str,
        websocket: WebSocket,
    ):
        self.connections[channel].add(websocket)

    ###########################################################################

    async def unsubscribe_alerts(
        self,
        channel: str,
        websocket: WebSocket,
    ):
        self.connections[channel].discard(websocket)

    ###########################################################################

    def active_connections(
        self,
    ) -> int:
        return sum(
            len(v)
            for v in self.connections.values()
        )


###############################################################################

manager = AlertsConnectionManager()

###############################################################################
# Connection
###############################################################################


@router.websocket("/alerts/{channel}")
async def stream_alerts(
    websocket: WebSocket,
    channel: str,
):
    await manager.connect(
        channel,
        websocket,
    )

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(
            channel,
            websocket,
        )


###############################################################################
# Streaming
###############################################################################


async def wallet_alerts(
    channel: str,
    payload: dict,
):
    await broadcast(
        channel,
        {
            "type": "wallet_alert",
            "data": payload,
        },
    )


###############################################################################


async def token_alerts(
    channel: str,
    payload: dict,
):
    await broadcast(
        channel,
        {
            "type": "token_alert",
            "data": payload,
        },
    )


###############################################################################


async def rug_alerts(
    channel: str,
    payload: dict,
):
    await broadcast(
        channel,
        {
            "type": "rug_alert",
            "data": payload,
        },
    )


###############################################################################


async def whale_alerts(
    channel: str,
    payload: dict,
):
    await broadcast(
        channel,
        {
            "type": "whale_alert",
            "data": payload,
        },
    )


###############################################################################


async def AI_alerts(
    channel: str,
    payload: dict,
):
    await broadcast(
        channel,
        {
            "type": "ai_alert",
            "data": payload,
        },
    )


###############################################################################


async def heartbeat():
    while True:

        for channel in list(
            manager.connections.keys()
        ):

            await broadcast(
                channel,
                {
                    "type": "heartbeat",
                },
            )

        await asyncio.sleep(30)


###############################################################################
# Runtime
###############################################################################


def diagnostics():
    return {
        "connections": manager.active_connections(),
    }


###############################################################################


def summary():
    return {
        "stream": "alerts",
        "connections": manager.active_connections(),
    }


###############################################################################
# Utilities
###############################################################################


async def broadcast(
    channel: str,
    payload: dict,
):
    message = build_alert_message(payload)

    for websocket in list(
        manager.connections.get(
            channel,
            [],
        )
    ):
        await websocket.send_text(message)


###############################################################################


def build_alert_message(
    payload: Any,
) -> str:
    return json.dumps(payload)