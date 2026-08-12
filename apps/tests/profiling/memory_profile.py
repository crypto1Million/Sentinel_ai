"""
Memory Profiling
================

Profiles memory consumption of Sentinel AI operations.
"""

from __future__ import annotations

import tracemalloc
import unittest


def run_memory_profile():

    tracemalloc.start()

    # Replace with actual Sentinel workload.
    data = [
        {
            "wallet": f"Wallet{i}",
            "score": i % 100,
        }
        for i in range(100_000)
    ]

    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return {
        "current_bytes": current,
        "peak_bytes": peak,
        "objects": len(data),
    }


class MemoryProfileTests(unittest.TestCase):

    def test_memory_usage(self):

        result = run_memory_profile()

        self.assertGreaterEqual(
            result["peak_bytes"],
            result["current_bytes"],
        )


if __name__ == "__main__":
    unittest.main()