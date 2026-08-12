###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import json
import math
import time
from functools import wraps
from typing import Any
from typing import Callable
from typing import Iterable

###############################################################################
# SQL Utilities
###############################################################################


def compile_query(
    query: str,
) -> str:
    """
    Normalize SQL query.
    """

    return " ".join(
        query.strip().split()
    )


###############################################################################


def sanitize_parameters(
    parameters: dict | None,
) -> dict:
    """
    Prevent None parameters.
    """

    return parameters or {}


###############################################################################


def normalize_result(
    rows: Iterable[Any],
) -> list:
    """
    Normalize DB output.
    """

    return list(rows)


###############################################################################


def explain_query(
    query: str,
) -> str:
    """
    Generate EXPLAIN query.
    """

    return f"EXPLAIN {compile_query(query)}"


###############################################################################


def optimize_query(
    query: str,
) -> str:
    """
    Placeholder optimizer.
    """

    return compile_query(query)


###############################################################################
# Graph Utilities
###############################################################################


def node_id(
    label: str,
    value: str,
) -> str:
    """
    Generate node id.
    """

    return f"{label}:{value}"


###############################################################################


def edge_id(
    source: str,
    target: str,
    relationship: str,
) -> str:
    """
    Generate edge id.
    """

    return f"{source}:{relationship}:{target}"


###############################################################################


def graph_metadata(
    nodes: int,
    edges: int,
) -> dict:
    """
    Graph metadata.
    """

    return {
        "nodes": nodes,
        "edges": edges,
    }


###############################################################################


def graph_statistics(
    nodes: int,
    edges: int,
) -> dict:
    """
    Graph statistics.
    """

    density = 0.0

    if nodes > 1:

        density = edges / (
            nodes * (nodes - 1)
        )

    return {
        "nodes": nodes,
        "edges": edges,
        "density": round(density, 6),
    }


###############################################################################
# Cache Utilities
###############################################################################


def cache_key(
    namespace: str,
    identifier: str,
) -> str:
    """
    Generate cache key.
    """

    return f"{namespace}:{identifier}"


###############################################################################


def cache_ttl(
    minutes: int,
) -> int:
    """
    Minutes → Seconds.
    """

    return minutes * 60


###############################################################################


def serialize(
    value: Any,
) -> str:
    """
    Serialize object.
    """

    return json.dumps(value)


###############################################################################


def deserialize(
    value: str | None,
) -> Any:
    """
    Deserialize object.
    """

    if value is None:
        return None

    try:
        return json.loads(value)

    except Exception:
        return value


###############################################################################
# Runtime
###############################################################################


def diagnostics() -> dict:
    """
    Diagnostics.
    """

    return {
        "module": "repositories.utils",
        "status": "healthy",
    }


###############################################################################


def summary() -> dict:
    """
    Runtime summary.
    """

    return {
        "utilities": [
            "sql",
            "graph",
            "cache",
            "helpers",
        ]
    }


###############################################################################
# Helpers
###############################################################################


def safe_execute(
    func: Callable,
    *args,
    **kwargs,
):
    """
    Execute safely.
    """

    try:
        return func(
            *args,
            **kwargs,
        )

    except Exception:
        return None


###############################################################################


def retry(
    retries: int = 3,
    delay: float = 0.5,
):
    """
    Retry decorator.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(
            *args,
            **kwargs,
        ):

            last_error = None

            for _ in range(retries):

                try:
                    return func(
                        *args,
                        **kwargs,
                    )

                except Exception as error:

                    last_error = error

                    time.sleep(delay)

            raise last_error

        return wrapper

    return decorator


###############################################################################


def chunk(
    items: list,
    size: int,
):
    """
    Split list into chunks.
    """

    for index in range(
        0,
        len(items),
        size,
    ):
        yield items[
            index : index + size
        ]


###############################################################################


def timer(
    func: Callable,
):
    """
    Execution timer decorator.
    """

    @wraps(func)
    def wrapper(
        *args,
        **kwargs,
    ):

        start = time.perf_counter()

        result = func(
            *args,
            **kwargs,
        )

        end = time.perf_counter()

        print(
            f"{func.__name__}: "
            f"{end-start:.6f}s"
        )

        return result

    return wrapper