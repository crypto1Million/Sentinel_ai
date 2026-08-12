"""
Wallet Worker
=============

Consumes wallet jobs from Redis and updates Sentinel intelligence.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

###############################################################################
# WalletWorker
###############################################################################


class WalletWorker:
    """
    Wallet ingestion worker.
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

        self.logger = logging.getLogger("wallet_worker")

    ###########################################################################

    async def start(self):

        self.running = True

        self.logger.info("Wallet Worker Started")

        while self.running:

            await self.consume_wallet_jobs()

    ###########################################################################

    async def stop(self):

        self.running = False

        self.logger.info("Wallet Worker Stopped")

    ###########################################################################

    async def restart(self):

        await self.stop()

        await self.start()

    ###########################################################################
    # Queue
    ###########################################################################

    async def consume_wallet_jobs(self):

        await asyncio.sleep(0.1)

    ###########################################################################

    async def enqueue_wallet(
        self,
        wallet: str,
    ):

        return {
            "wallet": wallet,
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

    async def process_wallet(
        self,
        wallet: str,
    ):

        data = await self.fetch_wallet(wallet)

        analysis = await self.analyze_wallet(data)

        score = await self.score_wallet(analysis)

        await self.update_wallet(wallet, score)

        await self.cache_wallet(wallet)

        await self.publish_wallet(wallet)

        return score

    ###########################################################################

    async def fetch_wallet(
        self,
        wallet: str,
    ):

        if self.repository:

            return self.repository.get_wallet(wallet)

        return {
            "wallet": wallet,
        }

    ###########################################################################

    async def analyze_wallet(
        self,
        wallet_data,
    ):

        return wallet_data

    ###########################################################################

    async def score_wallet(
        self,
        wallet_data,
    ):

        return {
            "wallet_score": 0,
        }

    ###########################################################################

    async def update_wallet(
        self,
        wallet: str,
        score,
    ):

        if self.repository:

            self.repository.update_wallet(
                wallet,
                score,
            )

    ###########################################################################

    async def cache_wallet(
        self,
        wallet: str,
    ):

        return True

    ###########################################################################

    async def publish_wallet(
        self,
        wallet: str,
    ):

        if self.publisher:

            self.publisher(wallet)

    ###########################################################################
    # Runtime
    ###########################################################################

    async def heartbeat(self):

        return {
            "worker": "wallet",
            "running": self.running,
            "timestamp": datetime.utcnow().isoformat(),
        }

    ###########################################################################

    async def diagnostics(self):

        return {
            "worker": "wallet",
            "running": self.running,
        }

    ###########################################################################

    async def summary(self):

        return {
            "worker": "WalletWorker",
        }


###############################################################################
# Utilities
###############################################################################


def build_payload(
    wallet: str,
):

    return {
        "wallet": wallet,
    }


###############################################################################


def validate_job(
    payload,
):

    return "wallet" in payload


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