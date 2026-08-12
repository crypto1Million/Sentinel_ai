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


class StatisticsConnectionManager:
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

    async def subscribe_statistics(
        self,
        channel: str,
        websocket: WebSocket,
    ):
        self.connections[channel].add(websocket)

    ###########################################################################

    async def unsubscribe_statistics(
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

manager = StatisticsConnectionManager()

###############################################################################
# Connection
###############################################################################


@router.websocket("/statistics/{channel}")
async def stream_statistics(
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


async def metrics_updates(
    channel: str,
    metrics: dict,
):
    await broadcast(
        channel,
        {
            "type": "metrics_update",
            "data": metrics,
        },
    )


###############################################################################


async def runtime_updates(
    channel: str,
    runtime: dict,
):
    await broadcast(
        channel,
        {
            "type": "runtime_update",
            "data": runtime,
        },
    )


###############################################################################


async def dashboard_updates(
    channel: str,
    dashboard: dict,
):
    await broadcast(
        channel,
        {
            "type": "dashboard_update",
            "data": dashboard,
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
        "stream": "statistics",
        "connections": manager.active_connections(),
    }


###############################################################################
# Utilities
###############################################################################


async def broadcast(
    channel: str,
    payload: dict,
):
    message = build_statistics_message(payload)

    for websocket in list(
        manager.connections.get(
            channel,
            [],
        )
    ):
        await websocket.send_text(message)


###############################################################################


def build_statistics_message(
    payload: Any,
) -> str:
    return json.dumps(payload)