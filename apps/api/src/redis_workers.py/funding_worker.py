"""
Funding Worker
==============

Consumes funding-chain jobs from Redis and updates funding intelligence.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

###############################################################################
# FundingWorker
###############################################################################


class FundingWorker:
    """
    Funding chain worker.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        queue=None,
        repository=None,
        graph_repository=None,
        publisher=None,
    ):

        self.queue = queue
        self.repository = repository
        self.graph_repository = graph_repository
        self.publisher = publisher

        self.running = False

        self.logger = logging.getLogger("funding_worker")

    ###########################################################################

    async def start(self):

        self.running = True

        self.logger.info("Funding Worker Started")

        while self.running:

            await self.consume_funding_jobs()

    ###########################################################################

    async def stop(self):

        self.running = False

        self.logger.info("Funding Worker Stopped")

    ###########################################################################

    async def restart(self):

        await self.stop()

        await self.start()

    ###########################################################################
    # Queue
    ###########################################################################

    async def consume_funding_jobs(self):

        await asyncio.sleep(0.1)

    ###########################################################################

    async def enqueue_funding(
        self,
        signature: str,
    ):

        return {
            "signature": signature,
            "queued": True,
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

    async def process_funding(
        self,
        signature: str,
    ):

        chain = await self.trace_chain(signature)

        await self.update_graph(chain)

        await self.update_database(chain)

        await self.cache_chain(chain)

        await self.publish_chain(chain)

        return chain

    ###########################################################################

    async def trace_chain(
        self,
        signature: str,
    ):

        return {
            "signature": signature,
            "chain": [],
        }

    ###########################################################################

    async def update_graph(
        self,
        chain,
    ):

        if self.graph_repository:

            return True

    ###########################################################################

    async def update_database(
        self,
        chain,
    ):

        if self.repository:

            return True

    ###########################################################################

    async def cache_chain(
        self,
        chain,
    ):

        return True

    ###########################################################################

    async def publish_chain(
        self,
        chain,
    ):

        if self.publisher:

            self.publisher(chain)

    ###########################################################################
    # Runtime
    ###########################################################################

    async def heartbeat(self):

        return {
            "worker": "funding",
            "running": self.running,
            "timestamp": datetime.utcnow().isoformat(),
        }

    ###########################################################################

    async def diagnostics(self):

        return {
            "worker": "funding",
            "running": self.running,
        }

    ###########################################################################

    async def summary(self):

        return {
            "worker": "FundingWorker",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_chain(
    chain,
):

    return chain


###############################################################################


def validate_job(
    payload,
):

    return "signature" in payload


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