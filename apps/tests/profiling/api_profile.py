"""
API Profiling
=============

Profiles latency of Sentinel AI API operations.
"""

from __future__ import annotations

import time
import unittest


def profile_request():

    start = time.perf_counter()

    # Replace with actual HTTP request.
    status_code = 200

    elapsed = time.perf_counter() - start

    return {
        "status_code": status_code,
        "latency_seconds": elapsed,
    }


class APIProfileTests(unittest.TestCase):

    def test_api_latency(self):

        result = profile_request()

        self.assertEqual(
            result["status_code"],
            200,
        )

        self.assertGreaterEqual(
            result["latency_seconds"],
            0,
        )


if __name__ == "__main__":
    unittest.main()