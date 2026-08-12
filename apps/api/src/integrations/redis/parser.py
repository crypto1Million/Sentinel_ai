"""
Redis Parser
============

Serialization / Deserialization helpers.
"""

from __future__ import annotations

import json
from typing import Any, Dict


###############################################################################
# RedisParser
###############################################################################


class RedisParser:

    ###########################################################################
    # Serialization
    ###########################################################################

    def serialize(
        self,
        value: Any,
    ) -> str:

        return json.dumps(value)

    ###########################################################################

    def deserialize(
        self,
        value: str,
    ):

        try:

            return json.loads(value)

        except Exception:

            return value

    ###########################################################################
    # Message Parsing
    ###########################################################################

    def parse_message(
        self,
        message: Dict,
    ):

        return normalize_message(message)

    ###########################################################################

    def parse_cache(
        self,
        value: str,
    ):

        return self.deserialize(value)

    ###########################################################################

    def parse_stream(
        self,
        message: Dict,
    ):

        return normalize_message(message)

    ###########################################################################

    def parse_pubsub(
        self,
        message: Dict,
    ):

        return normalize_message(message)

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "RedisParser",
        }

    ###########################################################################

    def summary(self):

        return {
            "status": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_message(
    message: Dict,
):

    return {
        "channel": message.get("channel"),
        "data": message.get("data"),
    }


###############################################################################


def build_message(
    channel: str,
    payload: Any,
):

    return {
        "channel": channel,
        "payload": payload,
    }