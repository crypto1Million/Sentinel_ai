"""
Queue Manager
=============

Redis queue abstraction used by Sentinel AI workers.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import json
import logging

import redis

###############################################################################
# QueueManager
###############################################################################


class QueueManager:
    """
    Redis Queue Manager.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
    ):

        self.redis_url = redis_url

        self.client = None

        self.logger = logging.getLogger("queue_manager")

    ###########################################################################

    def connect(self):

        self.client = redis.Redis.from_url(
            self.redis_url,
            decode_responses=True,
        )

        return self.client

    ###########################################################################

    def disconnect(self):

        if self.client:

            self.client.close()

    ###########################################################################

    def diagnostics(self):

        return {
            "connected": self.client is not None,
            "redis_url": self.redis_url,
        }

    ###########################################################################
    # Queue Operations
    ###########################################################################

    def enqueue(
        self,
        queue: str,
        message: dict,
    ):

        self.client.rpush(
            queue_key(queue),
            json.dumps(normalize_message(message)),
        )

    ###########################################################################

    def dequeue(
        self,
        queue: str,
    ):

        result = self.client.lpop(
            queue_key(queue),
        )

        if result:

            return json.loads(result)

        return None

    ###########################################################################

    def acknowledge(
        self,
        job_id: str,
    ):

        self.logger.info(
            f"Acknowledged Job {job_id}"
        )

        return True

    ###########################################################################

    def reject(
        self,
        job_id: str,
    ):

        self.logger.warning(
            f"Rejected Job {job_id}"
        )

        return True

    ###########################################################################

    def requeue(
        self,
        queue: str,
        message: dict,
    ):

        self.enqueue(
            queue,
            message,
        )

    ###########################################################################

    def purge(
        self,
        queue: str,
    ):

        self.client.delete(
            queue_key(queue),
        )

    ###########################################################################

    def queue_size(
        self,
        queue: str,
    ):

        return self.client.llen(
            queue_key(queue),
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "connected": self.client is not None,
            "redis": self.redis_url,
        }


###############################################################################
# Utilities
###############################################################################


def queue_key(
    queue: str,
):

    return f"sentinel:{queue}"


###############################################################################


def normalize_message(
    message: dict,
):

    return message