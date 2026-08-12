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


class GraphConnectionManager:
    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    ###########################################################################

    async def connect(
        self,
        graph_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()
        self.connections[graph_id].add(websocket)

    ###########################################################################

    async def disconnect(
        self,
        graph_id: str,
        websocket: WebSocket,
    ):
        self.connections[graph_id].discard(websocket)

        if not self.connections[graph_id]:
            self.connections.pop(graph_id, None)

    ###########################################################################

    async def subscribe_graph(
        self,
        graph_id: str,
        websocket: WebSocket,
    ):
        self.connections[graph_id].add(websocket)

    ###########################################################################

    async def unsubscribe_graph(
        self,
        graph_id: str,
        websocket: WebSocket,
    ):
        self.connections[graph_id].discard(websocket)

    ###########################################################################

    def active_connections(
        self,
    ) -> int:
        return sum(
            len(v)
            for v in self.connections.values()
        )


###############################################################################

manager = GraphConnectionManager()

###############################################################################
# Connection
###############################################################################


@router.websocket("/graph/{graph_id}")
async def stream_graph(
    websocket: WebSocket,
    graph_id: str,
):
    await manager.connect(graph_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(graph_id, websocket)


###############################################################################
# Streaming
###############################################################################


async def node_updates(
    graph_id: str,
    node: dict,
):
    await broadcast(
        graph_id,
        {
            "type": "node_update",
            "data": node,
        },
    )


###############################################################################


async def edge_updates(
    graph_id: str,
    edge: dict,
):
    await broadcast(
        graph_id,
        {
            "type": "edge_update",
            "data": edge,
        },
    )


###############################################################################


async def graph_refresh(
    graph_id: str,
):
    await broadcast(
        graph_id,
        {
            "type": "graph_refresh",
        },
    )


###############################################################################


async def heartbeat():
    while True:

        for graph_id in list(manager.connections.keys()):

            await broadcast(
                graph_id,
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
        "stream": "graph",
        "connections": manager.active_connections(),
    }


###############################################################################
# Utilities
###############################################################################


async def broadcast(
    graph_id: str,
    payload: dict,
):
    message = build_graph_message(payload)

    for websocket in list(manager.connections.get(graph_id, [])):
        await websocket.send_text(message)


###############################################################################


def build_graph_message(
    payload: Any,
) -> str:
    return json.dumps(payload)