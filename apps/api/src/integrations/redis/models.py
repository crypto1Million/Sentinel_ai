"""
Redis Models
============
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


###############################################################################
# CacheEntryModel
###############################################################################


class CacheEntryModel(BaseModel):

    key: str

    value: Any

    ttl: Optional[int] = None


###############################################################################
# PubSubMessageModel
###############################################################################


class PubSubMessageModel(BaseModel):

    channel: str

    payload: Dict = Field(
        default_factory=dict
    )


###############################################################################
# StreamMessageModel
###############################################################################


class StreamMessageModel(BaseModel):

    stream: str

    message_id: Optional[str] = None

    payload: Dict = Field(
        default_factory=dict
    )


###############################################################################
# LockModel
###############################################################################


class LockModel(BaseModel):

    resource: str

    owner: Optional[str] = None

    timeout: int = 30


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "models": [
            "CacheEntryModel",
            "PubSubMessageModel",
            "StreamMessageModel",
            "LockModel",
        ]
    }


###############################################################################
# Utilities
###############################################################################


def validators():

    return {
        "cache_key": "string",
        "stream": "string",
        "channel": "string",
        "lock": "unique",
    }