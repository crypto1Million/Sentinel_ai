"""
Worker Profiling
================

Profiles Sentinel AI background-worker execution.
"""

from __future__ import annotations

import cProfile
import pstats
import unittest


def worker_operation():

    # Replace with actual worker workload.
    processed = 0

    for _ in range(100_000):
        processed += 1

    return processed


def run_worker_profile():

    profiler = cProfile.Profile()

    profiler.enable()

    result = worker_operation()

    profiler.disable()

    stats = pstats.Stats(profiler)

    stats.sort_stats("cumulative")
    stats.print_stats(30)

    return result


class WorkerProfileTests(unittest.TestCase):

    def test_worker_profile(self):

        result = run_worker_profile()

        self.assertEqual(
            result,
            100_000,
        )


if __name__ == "__main__":
    unittest.main()