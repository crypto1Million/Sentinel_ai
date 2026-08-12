"""
Redis Client
============

Low-level Redis connection manager used throughout Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Dict, Optional

import redis

###############################################################################
# RedisClient
###############################################################################


class RedisClient:
    """
    Base Redis client.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True,
    ):

        self.host = host

        self.port = port

        self.db = db

        self.password = password

        self.decode_responses = decode_responses

        self.connection: Optional[
            redis.Redis
        ] = None

    ###########################################################################

    def connect(self) -> redis.Redis:
        """
        Connect to Redis.
        """

        self.connection = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=self.decode_responses,
        )

        self.connection.ping()

        return self.connection

    ###########################################################################

    def disconnect(self):
        """
        Close connection.
        """

        if self.connection:

            self.connection.close()

            self.connection = None

    ###########################################################################

    def health(self) -> Dict[str, Any]:
        """
        Connection health.
        """

        try:

            if self.connection:

                self.connection.ping()

                return {
                    "healthy": True,
                    "host": self.host,
                    "port": self.port,
                    "db": self.db,
                }

            return {
                "healthy": False,
                "reason": "Not connected",
            }

        except Exception as exc:

            return {
                "healthy": False,
                "error": str(exc),
            }

    ###########################################################################
    # Base Operations
    ###########################################################################

    def get(
        self,
        key: str,
    ) -> Any:

        return self.connection.get(key)

    ###########################################################################

    def set(
        self,
        key: str,
        value: Any,
        ex: Optional[int] = None,
    ):

        return self.connection.set(
            key,
            value,
            ex=ex,
        )

    ###########################################################################

    def delete(
        self,
        key: str,
    ):

        return self.connection.delete(key)

    ###########################################################################

    def exists(
        self,
        key: str,
    ):

        return bool(
            self.connection.exists(key)
        )

    ###########################################################################

    def expire(
        self,
        key: str,
        seconds: int,
    ):

        return self.connection.expire(
            key,
            seconds,
        )

    ###########################################################################

    def ttl(
        self,
        key: str,
    ):

        return self.connection.ttl(key)

    ###########################################################################

    def keys(
        self,
        pattern: str = "*",
    ):

        return self.connection.keys(pattern)

    ###########################################################################

    def flushdb(self):

        return self.connection.flushdb()

    ###########################################################################

    def flushall(self):

        return self.connection.flushall()

    ###########################################################################

    def ping(self):

        return self.connection.ping()

    ###########################################################################

    def info(self):

        return self.connection.info()

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "client": "RedisClient",
            "connected": self.connection
            is not None,
            "host": self.host,
            "port": self.port,
            "db": self.db,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "Redis",
            "status": (
                "connected"
                if self.connection
                else "disconnected"
            ),
        }

    ###########################################################################
    # Utilities
    ###########################################################################

    @property
    def is_connected(self) -> bool:

        return self.connection is not None

    ###########################################################################

    def connection_url(self) -> str:

        return (
            f"redis://{self.host}:{self.port}/{self.db}"
        )

    ###########################################################################

    def reconnect(self):

        self.disconnect()

        return self.connect()