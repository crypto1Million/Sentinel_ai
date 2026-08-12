"""
Scheduler Flow Integration Tests
================================
"""

from __future__ import annotations

import unittest


class SchedulerFlowTests(unittest.TestCase):

    def setUp(self):
        self.scheduler = self.mock_scheduler()

    def tearDown(self):
        self.scheduler = None

    # Scheduler Flow

    def test_job_schedule(self): ...
    def test_job_execution(self): ...
    def test_worker_dispatch(self): ...
    def test_recurring_jobs(self): ...
    def test_scheduler_restart(self): ...

    # Runtime

    def diagnostics(self): ...
    def summary(self): ...

    def mock_scheduler(self):
        return {}


if __name__ == "__main__":
    unittest.main()