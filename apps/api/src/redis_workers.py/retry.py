"""
Retry Manager
=============

Reusable retry system for Sentinel AI workers.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

###############################################################################
# RetryManager
###############################################################################


class RetryManager:
    """
    Generic retry handler.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        retries: int = 3,
        delay: float = 1.0,
    ):

        self.retries = retries
        self.delay = delay

        self.logger = logging.getLogger("retry_manager")

    ###########################################################################
    # Retry
    ###########################################################################

    async def retry(
        self,
        coroutine,
    ):

        for attempt in range(self.retries):

            try:

                return await coroutine()

            except Exception as exc:

                self.logger.warning(
                    f"Retry {attempt+1}/{self.retries}: {exc}"
                )

                if attempt == self.retries - 1:

                    raise

                await asyncio.sleep(
                    self.fixed_backoff(attempt)
                )

    ###########################################################################

    def exponential_backoff(
        self,
        attempt: int,
    ) -> float:

        return self.delay * (2**attempt)

    ###########################################################################

    def fixed_backoff(
        self,
        attempt: int,
    ) -> float:

        return self.delay

    ###########################################################################

    async def retry_forever(
        self,
        coroutine,
    ):

        attempt = 0

        while True:

            try:

                return await coroutine()

            except Exception as exc:

                attempt += 1

                self.logger.warning(
                    f"Retry Forever Attempt {attempt}: {exc}"
                )

                await asyncio.sleep(
                    self.exponential_backoff(
                        min(attempt, 6)
                    )
                )

    ###########################################################################

    def diagnostics(self):

        return {
            "retries": self.retries,
            "delay": self.delay,
        }

    ###########################################################################
    # Runtime
    ###########################################################################

    def summary(self):

        return {
            "retry_strategy": "generic",
            "max_retries": self.retries,
        }


###############################################################################
# Utilities
###############################################################################


def sleep_time(
    delay: float,
    attempt: int,
):

    return delay * (2**attempt)


###############################################################################


def retry_metadata():

    return {
        "created": datetime.utcnow().isoformat(),
        "component": "RetryManager",
    }