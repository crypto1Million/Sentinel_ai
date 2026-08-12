"""
Heartbeat
=========

Worker heartbeat management for Sentinel AI.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

###############################################################################
# Heartbeat
###############################################################################


class Heartbeat:
    """
    Tracks worker heartbeat status.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self):

        self._heartbeats: Dict[str, str] = {}

    ###########################################################################
    # Heartbeat Operations
    ###########################################################################

    def send(
        self,
        worker: str,
    ):

        self._heartbeats[worker] = timestamp()

        return heartbeat_payload(worker)

    ###########################################################################

    def receive(
        self,
        worker: str,
        heartbeat: dict,
    ):

        self._heartbeats[worker] = heartbeat.get(
            "timestamp",
            timestamp(),
        )

        return True

    ###########################################################################

    def check_alive(
        self,
        worker: str,
    ):

        return worker in self._heartbeats

    ###########################################################################

    def last_seen(
        self,
        worker: str,
    ):

        return self._heartbeats.get(worker)

    ###########################################################################

    def diagnostics(self):

        return {
            "workers": len(self._heartbeats),
            "heartbeats": self._heartbeats,
        }

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "active_workers": list(self._heartbeats.keys()),
            "count": len(self._heartbeats),
        }


###############################################################################
# Utilities
###############################################################################


def heartbeat_payload(
    worker: str,
):

    return {
        "worker": worker,
        "status": "alive",
        "timestamp": timestamp(),
    }


###############################################################################


def timestamp():

    return datetime.now(
        timezone.utc
    ).isoformat()