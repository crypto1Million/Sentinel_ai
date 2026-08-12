"""
Redis Events
============

Redis Pub/Sub event manager for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import json
import logging
from datetime import datetime

import redis

###############################################################################
# RedisEvents
###############################################################################


class RedisEvents:
    """
    Redis Pub/Sub wrapper.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
    ):

        self.redis_url = redis_url

        self.client = redis.Redis.from_url(
            redis_url,
            decode_responses=True,
        )

        self.pubsub = self.client.pubsub()

        self.logger = logging.getLogger("redis_events")

    ###########################################################################
    # Pub/Sub
    ###########################################################################

    def publish(
        self,
        channel: str,
        payload: dict,
    ):

        self.client.publish(
            event_channel(channel),
            json.dumps(build_event(channel, payload)),
        )

    ###########################################################################

    def subscribe(
        self,
        channel: str,
    ):

        self.pubsub.subscribe(
            event_channel(channel),
        )

    ###########################################################################

    def unsubscribe(
        self,
        channel: str,
    ):

        self.pubsub.unsubscribe(
            event_channel(channel),
        )

    ###########################################################################

    def listen(self):

        for message in self.pubsub.listen():

            if message["type"] == "message":

                yield json.loads(message["data"])

    ###########################################################################

    def diagnostics(self):

        return {
            "connected": True,
            "redis_url": self.redis_url,
        }

    ###########################################################################
    # Event Types
    ###########################################################################

    def wallet_event(
        self,
        payload: dict,
    ):

        self.publish(
            "wallet",
            payload,
        )

    ###########################################################################

    def funding_event(
        self,
        payload: dict,
    ):

        self.publish(
            "funding",
            payload,
        )

    ###########################################################################

    def bundle_event(
        self,
        payload: dict,
    ):

        self.publish(
            "bundle",
            payload,
        )

    ###########################################################################

    def statistics_event(
        self,
        payload: dict,
    ):

        self.publish(
            "statistics",
            payload,
        )

    ###########################################################################

    def runtime_event(
        self,
        payload: dict,
    ):

        self.publish(
            "runtime",
            payload,
        )

    ###########################################################################

    def alert_event(
        self,
        payload: dict,
    ):

        self.publish(
            "alerts",
            payload,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "pubsub": "active",
            "events": [
                "wallet",
                "funding",
                "bundle",
                "statistics",
                "runtime",
                "alerts",
            ],
        }


###############################################################################
# Utilities
###############################################################################


def build_event(
    event_type: str,
    payload: dict,
):

    return {
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload,
    }


###############################################################################


def event_channel(
    name: str,
):

    return f"sentinel:{name}"