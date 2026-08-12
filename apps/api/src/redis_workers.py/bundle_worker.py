"""
Bundle Worker
=============

Consumes bundle detection jobs from Redis and updates bundle intelligence.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

###############################################################################
# BundleWorker
###############################################################################


class BundleWorker:
    """
    Bundle detection worker.
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

        self.logger = logging.getLogger("bundle_worker")

    ###########################################################################

    async def start(self):

        self.running = True

        self.logger.info("Bundle Worker Started")

        while self.running:

            await self.consume_bundle_jobs()

    ###########################################################################

    async def stop(self):

        self.running = False

        self.logger.info("Bundle Worker Stopped")

    ###########################################################################

    async def restart(self):

        await self.stop()

        await self.start()

    ###########################################################################
    # Queue
    ###########################################################################

    async def consume_bundle_jobs(self):

        await asyncio.sleep(0.1)

    ###########################################################################

    async def enqueue_bundle(
        self,
        mint: str,
    ):

        return {
            "mint": mint,
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

    async def detect_bundle(
        self,
        mint: str,
    ):

        bundle = await self.analyze_bundle(mint)

        score = await self.score_bundle(bundle)

        await self.update_bundle(bundle)

        await self.cache_bundle(bundle)

        await self.publish_bundle(bundle)

        return score

    ###########################################################################

    async def analyze_bundle(
        self,
        mint: str,
    ):

        return {
            "mint": mint,
            "wallets": [],
        }

    ###########################################################################

    async def score_bundle(
        self,
        bundle,
    ):

        return {
            "bundle_score": 0,
        }

    ###########################################################################

    async def update_bundle(
        self,
        bundle,
    ):

        if self.repository:

            return True

    ###########################################################################

    async def cache_bundle(
        self,
        bundle,
    ):

        return True

    ###########################################################################

    async def publish_bundle(
        self,
        bundle,
    ):

        if self.publisher:

            self.publisher(bundle)

    ###########################################################################
    # Runtime
    ###########################################################################

    async def heartbeat(self):

        return {
            "worker": "bundle",
            "running": self.running,
            "timestamp": datetime.utcnow().isoformat(),
        }

    ###########################################################################

    async def diagnostics(self):

        return {
            "worker": "bundle",
            "running": self.running,
        }

    ###########################################################################

    async def summary(self):

        return {
            "worker": "BundleWorker",
        }


###############################################################################
# Utilities
###############################################################################


def validate_bundle(
    bundle,
):

    return bundle is not None


###############################################################################


def validate_job(
    payload,
):

    return "mint" in payload


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