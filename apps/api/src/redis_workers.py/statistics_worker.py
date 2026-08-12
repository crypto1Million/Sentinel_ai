"""
Statistics Worker
=================

Consumes statistics jobs from Redis and updates analytics.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

###############################################################################
# StatisticsWorker
###############################################################################


class StatisticsWorker:
    """
    Statistics aggregation worker.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        queue=None,
        repository=None,
        publisher=None,
    ):

        self.queue = queue
        self.repository = repository
        self.publisher = publisher

        self.running = False

        self.logger = logging.getLogger("statistics_worker")

    ###########################################################################

    async def start(self):

        self.running = True

        self.logger.info("Statistics Worker Started")

        while self.running:

            await self.consume_statistics_jobs()

    ###########################################################################

    async def stop(self):

        self.running = False

        self.logger.info("Statistics Worker Stopped")

    ###########################################################################

    async def restart(self):

        await self.stop()

        await self.start()

    ###########################################################################
    # Queue
    ###########################################################################

    async def consume_statistics_jobs(self):

        await asyncio.sleep(0.1)

    ###########################################################################

    async def enqueue_statistics(
        self,
        payload: dict,
    ):

        return {
            "queued": True,
            "payload": payload,
        }

    ###########################################################################

    async def acknowledge(
        self,
        job_id: str,
    ):

        return {
            "job": job_id,
            "status": "acknowledged",
        }

    ###########################################################################

    async def reject(
        self,
        job_id: str,
    ):

        return {
            "job": job_id,
            "status": "rejected",
        }

    ###########################################################################
    # Processing
    ###########################################################################

    async def refresh_statistics(self):

        await self.calculate_wallet_metrics()

        await self.calculate_token_metrics()

        await self.calculate_graph_metrics()

        await self.update_dashboard()

        await self.cache_statistics()

        await self.publish_statistics()

        return True

    ###########################################################################

    async def calculate_wallet_metrics(self):

        return {
            "wallets": 0,
        }

    ###########################################################################

    async def calculate_token_metrics(self):

        return {
            "tokens": 0,
        }

    ###########################################################################

    async def calculate_graph_metrics(self):

        return {
            "nodes": 0,
            "edges": 0,
        }

    ###########################################################################

    async def update_dashboard(self):

        if self.repository:

            return True

    ###########################################################################

    async def cache_statistics(self):

        return True

    ###########################################################################

    async def publish_statistics(self):

        if self.publisher:

            self.publisher(
                {
                    "event": "statistics_updated"
                }
            )

    ###########################################################################
    # Runtime
    ###########################################################################

    async def heartbeat(self):

        return {
            "worker": "statistics",
            "running": self.running,
            "timestamp": datetime.utcnow().isoformat(),
        }

    ###########################################################################

    async def diagnostics(self):

        return {
            "worker": "statistics",
            "running": self.running,
        }

    ###########################################################################

    async def summary(self):

        return {
            "worker": "StatisticsWorker",
        }


###############################################################################
# Utilities
###############################################################################


def validate_job(
    payload,
):

    return isinstance(payload, dict)


###############################################################################


def normalize_metrics(
    metrics: dict,
):

    return metrics


###############################################################################


async def retry_job(
    coroutine,
    retries: int = 3,
):

    for attempt in range(retries):

        try:

            return await coroutine()

        except Exception:

            if attempt == retries - 1:

                raise

            await asyncio.sleep(1)