###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import re
from typing import Any

###############################################################################
# Constants
###############################################################################

MAX_QUERY_LENGTH = 256
MAX_LIMIT = 100

###############################################################################
# Query Validation
###############################################################################


def validate_query(
    query: str,
) -> bool:
    """
    Validate generic query.
    """

    if not query:
        return False

    query = normalize_query(query)

    return 1 <= len(query) <= MAX_QUERY_LENGTH


###############################################################################


def validate_search(
    search: str,
) -> bool:
    """
    Validate search string.
    """

    return validate_query(search)


###############################################################################


def validate_filters(
    filters: dict[str, Any],
) -> bool:
    """
    Validate filter payload.
    """

    return isinstance(filters, dict)


###############################################################################


def validate_sort(
    field: str,
    order: str,
) -> bool:
    """
    Validate sorting options.
    """

    return (
        bool(field)
        and order.lower() in {"asc", "desc"}
    )


###############################################################################


def validate_pagination(
    limit: int,
    offset: int,
) -> bool:
    """
    Validate pagination.
    """

    return (
        0 <= offset
        and 1 <= limit <= MAX_LIMIT
    )


###############################################################################


def sanitize_query(
    query: str,
) -> str:
    """
    Sanitize search query.
    """

    query = normalize_query(query)

    return re.sub(
        r"[^\w\s\-.:]",
        "",
        query,
    )


###############################################################################
# Runtime
###############################################################################


def diagnostics() -> dict[str, Any]:
    """
    Validator diagnostics.
    """

    return {
        "validator": "query",
        "max_length": MAX_QUERY_LENGTH,
        "max_limit": MAX_LIMIT,
    }


###############################################################################


def summary() -> dict[str, Any]:
    """
    Validator summary.
    """

    return {
        "query_validation": True,
        "filter_validation": True,
        "pagination_validation": True,
    }


###############################################################################
# Utilities
###############################################################################


def normalize_query(
    query: str,
) -> str:
    """
    Normalize query string.
    """

    return " ".join(query.strip().split())


###############################################################################


def parse_query(
    query: str,
) -> list[str]:
    """
    Split normalized query into tokens.
    """

    return normalize_query(query).split()