"""
Helius WebSocket
================

Real-time WebSocket client for Helius Solana subscriptions.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, Optional

import websockets

###############################################################################
# Helius WebSocket
###############################################################################


class HeliusWebSocket:
    """
    Helius WebSocket Client.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        api_key: str,
    ):

        self.api_key = api_key

        self.websocket = None

        self.connected = False

        self.subscription_id = 0

    ###########################################################################
    # Connection
    ###########################################################################

    async def connect(self):

        self.websocket = await websockets.connect(
            websocket_url(self.api_key),
        )

        self.connected = True

    ###########################################################################

    async def disconnect(self):

        if self.websocket:

            await self.websocket.close()

        self.connected = False

    ###########################################################################

    async def reconnect(self):

        await self.disconnect()

        await self.connect()

    ###########################################################################

    async def heartbeat(self):

        if self.connected:

            await self.websocket.ping()

    ###########################################################################
    # Subscriptions
    ###########################################################################

    async def account_subscribe(
        self,
        wallet: str,
    ):

        payload = subscription_payload(
            "accountSubscribe",
            [wallet],
            self.subscription_id,
        )

        self.subscription_id += 1

        await self.send(payload)

    ###########################################################################

    async def logs_subscribe(self):

        payload = subscription_payload(
            "logsSubscribe",
            ["all"],
            self.subscription_id,
        )

        self.subscription_id += 1

        await self.send(payload)

    ###########################################################################

    async def signature_subscribe(
        self,
        signature: str,
    ):

        payload = subscription_payload(
            "signatureSubscribe",
            [signature],
            self.subscription_id,
        )

        self.subscription_id += 1

        await self.send(payload)

    ###########################################################################

    async def slot_subscribe(self):

        payload = subscription_payload(
            "slotSubscribe",
            [],
            self.subscription_id,
        )

        self.subscription_id += 1

        await self.send(payload)

    ###########################################################################

    async def block_subscribe(self):

        payload = subscription_payload(
            "blockSubscribe",
            ["all"],
            self.subscription_id,
        )

        self.subscription_id += 1

        await self.send(payload)

    ###########################################################################

    async def unsubscribe(
        self,
        subscription: int,
    ):

        payload = subscription_payload(
            "unsubscribe",
            [subscription],
            self.subscription_id,
        )

        await self.send(payload)

    ###########################################################################
    # Streaming
    ###########################################################################

    async def receive(self):

        message = await self.websocket.recv()

        return self.parse_message(message)

    ###########################################################################

    async def send(
        self,
        payload: Dict,
    ):

        await self.websocket.send(
            json.dumps(payload),
        )

    ###########################################################################

    def parse_message(
        self,
        message: str,
    ):

        return json.loads(message)

    ###########################################################################

    async def dispatch(self):

        while self.connected:

            yield await self.receive()

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "connected": self.connected,
            "subscriptions": self.subscription_id,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Helius WebSocket",
            "connected": self.connected,
        }


###############################################################################
# Utilities
###############################################################################


def subscription_payload(
    method: str,
    params: list,
    request_id: int,
):

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params,
    }


###############################################################################


def websocket_url(
    api_key: str,
):

    return (
        "wss://mainnet.helius-rpc.com/"
        f"?api-key={api_key}"
    )