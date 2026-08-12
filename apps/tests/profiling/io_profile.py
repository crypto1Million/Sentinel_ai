"""
I/O Profiling
=============

Profiles disk/network I/O related operations.
"""

from __future__ import annotations

import tempfile
import time
import unittest


def run_io_profile():

    payload = b"sentinel-ai-test-data" * 10000

    start = time.perf_counter()

    with tempfile.NamedTemporaryFile() as file:

        file.write(payload)
        file.flush()

        file.seek(0)
        file.read()

    elapsed = time.perf_counter() - start

    return {
        "bytes": len(payload),
        "elapsed_seconds": elapsed,
        "bytes_per_second": len(payload) / max(elapsed, 1e-9),
    }


class IOProfileTests(unittest.TestCase):

    def test_io_throughput(self):

        result = run_io_profile()

        self.assertGreater(
            result["bytes_per_second"],
            0,
        )


if __name__ == "__main__":
    unittest.main()