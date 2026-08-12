"""
Sentinel AI - CPU Profiler
==========================

Profiles CPU usage of Sentinel components and reports the most
expensive functions.

Run directly:

    python apps/tests/profiling/cpu_profile.py
"""

from __future__ import annotations

import cProfile
import io
import pstats
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

DEFAULT_SORT = "cumulative"
DEFAULT_LINES = 30


# ----------------------------------------------------------------------
# Profile Result
# ----------------------------------------------------------------------

@dataclass
class ProfileResult:

    name: str
    elapsed_seconds: float
    profile_output: str


# ----------------------------------------------------------------------
# CPU Profiler
# ----------------------------------------------------------------------

class CPUProfiler:

    def __init__(
        self,
        sort: str = DEFAULT_SORT,
        lines: int = DEFAULT_LINES,
    ):

        self.sort = sort
        self.lines = lines

        self.results: list[ProfileResult] = []

    # ------------------------------------------------------------------
    # Profile Callable
    # ------------------------------------------------------------------

    def profile(
        self,
        name: str,
        function: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:

        profiler = cProfile.Profile()

        start = time.perf_counter()

        profiler.enable()

        try:

            result = function(
                *args,
                **kwargs,
            )

        finally:

            profiler.disable()

        elapsed = time.perf_counter() - start

        output = io.StringIO()

        stats = pstats.Stats(
            profiler,
            stream=output,
        )

        stats.strip_dirs()
        stats.sort_stats(self.sort)
        stats.print_stats(self.lines)

        profile_output = output.getvalue()

        self.results.append(
            ProfileResult(
                name=name,
                elapsed_seconds=elapsed,
                profile_output=profile_output,
            )
        )

        return result

    # ------------------------------------------------------------------
    # Context Manager
    # ------------------------------------------------------------------

    @contextmanager
    def section(
        self,
        name: str,
    ):

        profiler = cProfile.Profile()

        start = time.perf_counter()

        profiler.enable()

        try:

            yield profiler

        finally:

            profiler.disable()

            elapsed = time.perf_counter() - start

            output = io.StringIO()

            stats = pstats.Stats(
                profiler,
                stream=output,
            )

            stats.strip_dirs()
            stats.sort_stats(self.sort)
            stats.print_stats(self.lines)

            self.results.append(
                ProfileResult(
                    name=name,
                    elapsed_seconds=elapsed,
                    profile_output=output.getvalue(),
                )
            )

    # ------------------------------------------------------------------
    # Print Results
    # ------------------------------------------------------------------

    def print_results(self):

        print()
        print("=" * 80)
        print("SENTINEL AI CPU PROFILING RESULTS")
        print("=" * 80)

        if not self.results:

            print("No profiling results collected.")

            return

        for result in self.results:

            print()
            print("-" * 80)

            print(
                f"{result.name}: "
                f"{result.elapsed_seconds:.6f}s"
            )

            print("-" * 80)

            print(result.profile_output)


# ----------------------------------------------------------------------
# Example Sentinel Workload
# ----------------------------------------------------------------------

def mock_wallet_analysis():

    total = 0

    for i in range(100_000):

        total += (
            i * 2
            + i % 7
            + i % 11
        )

    return total


def mock_token_analysis():

    total = 0

    for i in range(100_000):

        total += (
            i * 3
            + i % 5
            + i % 13
        )

    return total


def mock_rug_radar():

    total = 0

    for i in range(100_000):

        total += (
            i % 3
            + i % 17
            + i % 19
        )

    return total


def mock_sentinel_score():

    total = 0

    for i in range(100_000):

        total += (
            i % 2
            + i % 5
            + i % 7
            + i % 11
        )

    return total


# ----------------------------------------------------------------------
# Sentinel CPU Profile
# ----------------------------------------------------------------------

def run_profile():

    profiler = CPUProfiler(
        sort="cumulative",
        lines=30,
    )

    profiler.profile(
        "Wallet Analysis",
        mock_wallet_analysis,
    )

    profiler.profile(
        "Token Analysis",
        mock_token_analysis,
    )

    profiler.profile(
        "Rug Radar",
        mock_rug_radar,
    )

    profiler.profile(
        "Sentinel Score",
        mock_sentinel_score,
    )

    profiler.print_results()


# ----------------------------------------------------------------------
# Runtime Diagnostics
# ----------------------------------------------------------------------

def diagnostics():

    return {
        "profiler": "cpu",
        "engine": "cProfile",
        "status": "ready",
    }


def summary():

    return {
        "service": "sentinel-cpu-profiler",
        "status": "ready",
    }


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 80)
    print("SENTINEL AI CPU PROFILER")
    print("=" * 80)

    print("Starting CPU profiling...")

    run_profile()

    print()
    print("=" * 80)
    print("CPU PROFILING COMPLETE")
    print("=" * 80)