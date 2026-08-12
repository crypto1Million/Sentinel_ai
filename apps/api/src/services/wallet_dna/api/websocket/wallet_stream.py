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


class WalletConnectionManager:
    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    ###########################################################################

    async def connect(
        self,
        wallet: str,
        websocket: WebSocket,
    ):
        await websocket.accept()
        self.connections[wallet].add(websocket)

    ###########################################################################

    async def disconnect(
        self,
        wallet: str,
        websocket: WebSocket,
    ):
        self.connections[wallet].discard(websocket)

        if not self.connections[wallet]:
            self.connections.pop(wallet, None)

    ###########################################################################

    async def subscribe_wallet(
        self,
        wallet: str,
        websocket: WebSocket,
    ):
        self.connections[wallet].add(websocket)

    ###########################################################################

    async def unsubscribe_wallet(
        self,
        wallet: str,
        websocket: WebSocket,
    ):
        self.connections[wallet].discard(websocket)

    ###########################################################################

    def active_connections(
        self,
    ) -> int:
        return sum(
            len(v)
            for v in self.connections.values()
        )


###############################################################################

manager = WalletConnectionManager()

###############################################################################
# Connection
###############################################################################


@router.websocket("/wallet/{wallet}")
async def stream_wallet(
    websocket: WebSocket,
    wallet: str,
):
    await manager.connect(wallet, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(wallet, websocket)


###############################################################################
# Streaming
###############################################################################


async def wallet_updates(
    wallet: str,
    payload: dict,
):
    await broadcast(wallet, payload)


###############################################################################


async def wallet_score_updates(
    wallet: str,
    score: dict,
):
    await broadcast(
        wallet,
        {
            "type": "wallet_score",
            "data": score,
        },
    )


###############################################################################


async def wallet_activity_updates(
    wallet: str,
    activity: dict,
):
    await broadcast(
        wallet,
        {
            "type": "wallet_activity",
            "data": activity,
        },
    )


###############################################################################


async def heartbeat():
    while True:

        for wallet in list(manager.connections.keys()):

            await broadcast(
                wallet,
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
        "stream": "wallet",
        "connections": manager.active_connections(),
    }


###############################################################################
# Utilities
###############################################################################


async def broadcast(
    wallet: str,
    payload: dict,
):
    message = build_message(payload)

    for websocket in list(manager.connections.get(wallet, [])):
        await websocket.send_text(message)


###############################################################################


def build_message(
    payload: Any,
) -> str:
    return json.dumps(payload)