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


class FundingConnectionManager:
    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    ###########################################################################

    async def connect(
        self,
        funding_id: str,
        websocket: WebSocket,
    ):
        await websocket.accept()
        self.connections[funding_id].add(websocket)

    ###########################################################################

    async def disconnect(
        self,
        funding_id: str,
        websocket: WebSocket,
    ):
        self.connections[funding_id].discard(websocket)

        if not self.connections[funding_id]:
            self.connections.pop(funding_id, None)

    ###########################################################################

    async def subscribe_funding(
        self,
        funding_id: str,
        websocket: WebSocket,
    ):
        self.connections[funding_id].add(websocket)

    ###########################################################################

    async def unsubscribe_funding(
        self,
        funding_id: str,
        websocket: WebSocket,
    ):
        self.connections[funding_id].discard(websocket)

    ###########################################################################

    def active_connections(
        self,
    ) -> int:
        return sum(
            len(v)
            for v in self.connections.values()
        )


###############################################################################

manager = FundingConnectionManager()

###############################################################################
# Connection
###############################################################################


@router.websocket("/funding/{funding_id}")
async def stream_funding(
    websocket: WebSocket,
    funding_id: str,
):
    await manager.connect(
        funding_id,
        websocket,
    )

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(
            funding_id,
            websocket,
        )


###############################################################################
# Streaming
###############################################################################


async def funding_updates(
    funding_id: str,
    funding: dict,
):
    await broadcast(
        funding_id,
        {
            "type": "funding_update",
            "data": funding,
        },
    )


###############################################################################


async def transaction_updates(
    funding_id: str,
    transaction: dict,
):
    await broadcast(
        funding_id,
        {
            "type": "transaction_update",
            "data": transaction,
        },
    )


###############################################################################


async def funding_chain_updates(
    funding_id: str,
    chain: dict,
):
    await broadcast(
        funding_id,
        {
            "type": "funding_chain_update",
            "data": chain,
        },
    )


###############################################################################


async def heartbeat():
    while True:

        for funding_id in list(
            manager.connections.keys()
        ):

            await broadcast(
                funding_id,
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
        "stream": "funding",
        "connections": manager.active_connections(),
    }


###############################################################################
# Utilities
###############################################################################


async def broadcast(
    funding_id: str,
    payload: dict,
):
    message = build_message(payload)

    for websocket in list(
        manager.connections.get(
            funding_id,
            [],
        )
    ):
        await websocket.send_text(message)


###############################################################################


def build_message(
    payload: Any,
) -> str:
    return json.dumps(payload)