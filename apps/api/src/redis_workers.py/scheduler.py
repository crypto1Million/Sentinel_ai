"""
Scheduler
=========

Schedules recurring Redis worker jobs.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

###############################################################################
# Scheduler
###############################################################################


class Scheduler:
    """
    APScheduler wrapper for Sentinel AI.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self):

        self.logger = logging.getLogger("scheduler")

        self.scheduler = AsyncIOScheduler()

    ###########################################################################

    def start(self):

        self.scheduler.start()

        self.logger.info("Scheduler Started")

    ###########################################################################

    def stop(self):

        self.scheduler.shutdown(wait=False)

        self.logger.info("Scheduler Stopped")

    ###########################################################################

    def restart(self):

        self.stop()

        self.start()

    ###########################################################################
    # Scheduling
    ###########################################################################

    def schedule_wallet_refresh(
        self,
        func,
    ):

        self.add_job(
            "wallet_refresh",
            func,
            "*/5 * * * *",
        )

    ###########################################################################

    def schedule_statistics(
        self,
        func,
    ):

        self.add_job(
            "statistics_refresh",
            func,
            "*/10 * * * *",
        )

    ###########################################################################

    def schedule_cleanup(
        self,
        func,
    ):

        self.add_job(
            "cleanup",
            func,
            "0 * * * *",
        )

    ###########################################################################

    def schedule_graph_rebuild(
        self,
        func,
    ):

        self.add_job(
            "graph_rebuild",
            func,
            "0 */6 * * *",
        )

    ###########################################################################

    def schedule_cache_cleanup(
        self,
        func,
    ):

        self.add_job(
            "cache_cleanup",
            func,
            "30 * * * *",
        )

    ###########################################################################

    def schedule_runtime(
        self,
        func,
    ):

        self.add_job(
            "runtime",
            func,
            "*/1 * * * *",
        )

    ###########################################################################
    # Jobs
    ###########################################################################

    def add_job(
        self,
        job_id: str,
        func,
        cron: str,
    ):

        trigger = CronTrigger.from_crontab(cron)

        self.scheduler.add_job(
            func=func,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
        )

    ###########################################################################

    def remove_job(
        self,
        job_id: str,
    ):

        self.scheduler.remove_job(job_id)

    ###########################################################################

    def pause_job(
        self,
        job_id: str,
    ):

        self.scheduler.pause_job(job_id)

    ###########################################################################

    def resume_job(
        self,
        job_id: str,
    ):

        self.scheduler.resume_job(job_id)

    ###########################################################################

    def list_jobs(self):

        return self.scheduler.get_jobs()

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "running": self.scheduler.running,
            "jobs": len(self.scheduler.get_jobs()),
        }

    ###########################################################################

    def summary(self):

        return {
            "jobs": [
                job.id
                for job in self.scheduler.get_jobs()
            ]
        }


###############################################################################
# Utilities
###############################################################################


def cron_expression(
    expression: str,
):

    return CronTrigger.from_crontab(expression)


###############################################################################


def next_run(
    scheduler: AsyncIOScheduler,
    job_id: str,
):

    job = scheduler.get_job(job_id)

    if job:

        return job.next_run_time

    return None