"""
Redis Pub/Sub Manager
=====================

High-level Publish / Subscribe messaging interface for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import json
import threading
from typing import Any, Callable, Dict, List, Optional

###############################################################################
# PubSubManager
###############################################################################


class PubSubManager:
    """
    Redis Publish / Subscribe Manager.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        redis_client,
    ):

        self.redis = redis_client

        self.pubsub = None

        self.listener_thread = None

        self.running = False

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(self):

        self.pubsub = self.redis.connection.pubsub()

        return self.pubsub

    ###########################################################################

    def disconnect(self):

        if self.pubsub:

            self.pubsub.close()

        self.running = False

    ###########################################################################
    # Publish
    ###########################################################################

    def publish(
        self,
        channel: str,
        message: Any,
    ):

        payload = build_message(message)

        return self.redis.connection.publish(
            channel,
            payload,
        )

    ###########################################################################
    # Subscribe
    ###########################################################################

    def subscribe(
        self,
        channel: str,
    ):

        self.pubsub.subscribe(channel)

    ###########################################################################

    def unsubscribe(
        self,
        channel: str,
    ):

        self.pubsub.unsubscribe(channel)

    ###########################################################################
    # Listening
    ###########################################################################

    def listen(
        self,
        callback: Callable[[Dict], None],
    ):

        self.running = True

        def _worker():

            while self.running:

                message = self.pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=1,
                )

                if message:

                    callback(
                        normalize_message(message)
                    )

        self.listener_thread = threading.Thread(
            target=_worker,
            daemon=True,
        )

        self.listener_thread.start()

    ###########################################################################
    # Broadcast Helpers
    ###########################################################################

    def broadcast_wallet(
        self,
        wallet: Dict,
    ):

        return self.publish(
            "wallet.events",
            wallet,
        )

    ###########################################################################

    def broadcast_token(
        self,
        token: Dict,
    ):

        return self.publish(
            "token.events",
            token,
        )

    ###########################################################################

    def broadcast_graph(
        self,
        graph: Dict,
    ):

        return self.publish(
            "graph.events",
            graph,
        )

    ###########################################################################

    def broadcast_statistics(
        self,
        stats: Dict,
    ):

        return self.publish(
            "statistics.events",
            stats,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "PubSubManager",
            "connected": self.pubsub is not None,
            "running": self.running,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Redis",
            "component": "Pub/Sub",
        }


###############################################################################
# Utilities
###############################################################################


def build_message(
    payload: Any,
) -> str:

    return json.dumps(payload)


###############################################################################


def normalize_message(
    message: Dict,
) -> Dict:

    return {
        "channel": message.get("channel"),
        "pattern": message.get("pattern"),
        "data": deserialize(
            message.get("data"),
        ),
    }


###############################################################################


def deserialize(
    payload: Any,
):

    try:

        return json.loads(payload)

    except Exception:

        return payload


###############################################################################


def event_channel(
    namespace: str,
) -> str:

    return f"{namespace}.events"