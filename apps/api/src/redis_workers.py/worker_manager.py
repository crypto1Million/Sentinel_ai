"""
Worker Manager
==============

Controls all Redis background workers.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import logging

###############################################################################
# WorkerManager
###############################################################################


class WorkerManager:
    """
    Registers and controls all workers.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self):

        self.logger = logging.getLogger("worker_manager")

        self._workers = {}

    ###########################################################################

    def register_worker(
        self,
        name: str,
        worker,
    ):

        self._workers[name] = worker

    ###########################################################################

    def unregister_worker(
        self,
        name: str,
    ):

        self._workers.pop(name, None)

    ###########################################################################

    def workers(self):

        return self._workers

    ###########################################################################
    # Lifecycle
    ###########################################################################

    async def start_all(self):

        for worker in self._workers.values():

            await worker.start()

    ###########################################################################

    async def stop_all(self):

        for worker in self._workers.values():

            await worker.stop()

    ###########################################################################

    async def restart_all(self):

        for worker in self._workers.values():

            await worker.restart()

    ###########################################################################

    async def start_worker(
        self,
        name: str,
    ):

        if name in self._workers:

            await self._workers[name].start()

    ###########################################################################

    async def stop_worker(
        self,
        name: str,
    ):

        if name in self._workers:

            await self._workers[name].stop()

    ###########################################################################

    async def restart_worker(
        self,
        name: str,
    ):

        if name in self._workers:

            await self._workers[name].restart()

    ###########################################################################
    # Monitoring
    ###########################################################################

    async def worker_status(self):

        status = {}

        for name, worker in self._workers.items():

            status[name] = await worker.summary()

        return status

    ###########################################################################

    def running_workers(self):

        return [
            name
            for name, worker in self._workers.items()
            if getattr(worker, "running", False)
        ]

    ###########################################################################

    def failed_workers(self):

        return []

    ###########################################################################

    async def diagnostics(self):

        return {
            "registered_workers": len(self._workers),
            "running_workers": self.running_workers(),
            "failed_workers": self.failed_workers(),
        }

    ###########################################################################

    async def health(self):

        return {
            "healthy": len(self.failed_workers()) == 0,
        }

    ###########################################################################
    # Runtime
    ###########################################################################

    async def summary(self):

        return {
            "workers": list(self._workers.keys()),
        }


###############################################################################
# Utilities
###############################################################################


def build_registry():

    return {}


###############################################################################


def validate_worker(
    worker,
):

    required = [
        "start",
        "stop",
        "restart",
    ]

    return all(
        hasattr(worker, method)
        for method in required
    )