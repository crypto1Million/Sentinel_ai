###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

###############################################################################
# Constants
###############################################################################

DEFAULT_PAGE = 1

DEFAULT_LIMIT = 25

MAX_LIMIT = 500

DEFAULT_OFFSET = 0

DEFAULT_SORT_FIELD = "created_at"

DEFAULT_SORT_ORDER = "desc"

CURSOR_SEPARATOR = ":"

CURSOR_ENCODING = "utf-8"

###############################################################################
# Base Models
###############################################################################

class PaginationConfig(BaseModel):
    """
    Global pagination configuration.
    """

    default_page: int = DEFAULT_PAGE

    default_limit: int = DEFAULT_LIMIT

    max_limit: int = MAX_LIMIT

    default_offset: int = DEFAULT_OFFSET


###############################################################################


class CursorConfig(BaseModel):
    """
    Cursor pagination configuration.
    """

    enabled: bool = True

    separator: str = CURSOR_SEPARATOR

    encoding: str = CURSOR_ENCODING

    max_page_size: int = MAX_LIMIT


###############################################################################


class SortConfig(BaseModel):
    """
    Global sorting configuration.
    """

    default_field: str = DEFAULT_SORT_FIELD

    default_order: str = DEFAULT_SORT_ORDER

    allowed_fields: list[str] = Field(
        default_factory=list,
    )

    case_sensitive: bool = False

###############################################################################
# Offset Pagination
###############################################################################

class PaginationRequest(BaseModel):
    """
    Offset pagination request.
    """

    page: int = Field(DEFAULT_PAGE, ge=1)

    limit: int = Field(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT)


###############################################################################


class PaginationResponse(BaseModel):
    """
    Offset pagination response.
    """

    page: int

    limit: int

    total: int

    pages: int

    has_next: bool

    has_previous: bool


###############################################################################


def paginate(
    items: list[Any],
    request: PaginationRequest,
) -> list[Any]:
    """
    Apply offset pagination.
    """

    start = (request.page - 1) * request.limit

    end = start + request.limit

    return items[start:end]


###############################################################################


def page_count(
    total: int,
    limit: int,
) -> int:
    """
    Calculate total pages.
    """

    if total == 0:
        return 0

    return (total + limit - 1) // limit


###############################################################################


def has_next(
    page: int,
    total: int,
    limit: int,
) -> bool:
    """
    Determine if another page exists.
    """

    return page < page_count(total, limit)


###############################################################################
# Cursor Pagination
###############################################################################

class CursorRequest(BaseModel):
    """
    Cursor pagination request.
    """

    cursor: str | None = None

    limit: int = Field(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT)


###############################################################################


class CursorResponse(BaseModel):
    """
    Cursor pagination response.
    """

    cursor: str | None

    next_cursor: str | None

    previous_cursor: str | None

    limit: int

    has_next: bool


###############################################################################


def encode_cursor(
    value: str,
) -> str:
    """
    Encode cursor.
    """

    import base64

    return base64.urlsafe_b64encode(
        value.encode(CURSOR_ENCODING)
    ).decode(CURSOR_ENCODING)


###############################################################################


def decode_cursor(
    cursor: str,
) -> str:
    """
    Decode cursor.
    """

    import base64

    return base64.urlsafe_b64decode(
        cursor.encode(CURSOR_ENCODING)
    ).decode(CURSOR_ENCODING)


###############################################################################


def cursor_paginate(
    items: list[Any],
    request: CursorRequest,
) -> list[Any]:
    """
    Simple cursor pagination.

    Real implementation should query
    the database directly.
    """

    if request.cursor is None:

        return items[: request.limit]

    return items[: request.limit]


###############################################################################


def next_cursor(
    last_item_id: str | None,
) -> str | None:
    """
    Generate next cursor.
    """

    if last_item_id is None:

        return None

    return encode_cursor(last_item_id)

###############################################################################
# Sorting
###############################################################################

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


###############################################################################


class SortField(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    NAME = "name"
    SCORE = "score"
    VALUE = "value"


###############################################################################


class SortRequest(BaseModel):
    """
    Sorting request.
    """

    field: str = DEFAULT_SORT_FIELD

    order: SortOrder = SortOrder.DESC


###############################################################################


def apply_sort(
    items: list[Any],
    request: SortRequest,
) -> list[Any]:
    """
    Apply sorting.
    """

    reverse = request.order == SortOrder.DESC

    return sorted(
        items,
        key=lambda x: getattr(x, request.field, None)
        if hasattr(x, request.field)
        else x.get(request.field),
        reverse=reverse,
    )


###############################################################################


def validate_sort(
    request: SortRequest,
    config: SortConfig,
) -> bool:
    """
    Validate sortable field.
    """

    if not config.allowed_fields:
        return True

    return request.field in config.allowed_fields


###############################################################################
# Filtering
###############################################################################

class DateFilter(BaseModel):
    """
    Date range filter.
    """

    start: datetime | None = None
    end: datetime | None = None


###############################################################################


class RangeFilter(BaseModel):
    """
    Numeric range filter.
    """

    minimum: float | None = None
    maximum: float | None = None


###############################################################################


class SearchFilter(BaseModel):
    """
    Text search filter.
    """

    query: str | None = None


###############################################################################


class FilterRequest(BaseModel):
    """
    Generic filter request.
    """

    search: SearchFilter | None = None

    date: DateFilter | None = None

    range: RangeFilter | None = None


###############################################################################


def apply_filters(
    items: list[Any],
    filters: FilterRequest,
) -> list[Any]:
    """
    Apply basic filtering.

    Database-backed implementations
    should perform filtering directly
    in SQL/Cypher.
    """

    result = items

    if filters.search and filters.search.query:

        q = filters.search.query.lower()

        result = [

            item

            for item in result

            if q in str(item).lower()

        ]

    return result


###############################################################################


def validate_filters(
    filters: FilterRequest,
) -> bool:
    """
    Validate filter values.
    """

    if (
        filters.range
        and filters.range.minimum is not None
        and filters.range.maximum is not None
    ):

        if filters.range.minimum > filters.range.maximum:

            return False

    if (
        filters.date
        and filters.date.start
        and filters.date.end
    ):

        if filters.date.start > filters.date.end:

            return False

    return True

###############################################################################
# Utilities
###############################################################################

_PAGINATION_STATS = {
    "requests": 0,
    "items_processed": 0,
}


###############################################################################


def limit(
    value: int | None,
) -> int:
    """
    Normalize page size.
    """

    if value is None:
        return DEFAULT_LIMIT

    return max(1, min(value, MAX_LIMIT))


###############################################################################


def offset(
    page: int,
    page_limit: int,
) -> int:
    """
    Calculate offset.
    """

    return max(0, (page - 1) * page_limit)


###############################################################################


def page_number(
    page_offset: int,
    page_limit: int,
) -> int:
    """
    Calculate page number from offset.
    """

    return (page_offset // page_limit) + 1


###############################################################################


def total_pages(
    total_items: int,
    page_limit: int,
) -> int:
    """
    Calculate total pages.
    """

    if total_items <= 0:
        return 0

    return (total_items + page_limit - 1) // page_limit


###############################################################################


def metadata(
    *,
    total: int,
    page: int,
    page_limit: int,
) -> dict[str, Any]:
    """
    Pagination metadata.
    """

    return {
        "page": page,
        "limit": page_limit,
        "total": total,
        "pages": total_pages(total, page_limit),
        "offset": offset(page, page_limit),
        "has_next": page < total_pages(total, page_limit),
        "has_previous": page > 1,
    }


###############################################################################


def summary() -> dict[str, Any]:
    """
    Pagination configuration summary.
    """

    return {
        "default_page": DEFAULT_PAGE,
        "default_limit": DEFAULT_LIMIT,
        "max_limit": MAX_LIMIT,
        "cursor_enabled": CursorConfig().enabled,
    }


###############################################################################
# Runtime
###############################################################################

def pagination_statistics() -> dict[str, Any]:
    """
    Runtime statistics.
    """

    return dict(_PAGINATION_STATS)


###############################################################################


def diagnostics() -> dict[str, Any]:
    """
    Pagination diagnostics.
    """

    return {
        "configuration": summary(),
        "statistics": pagination_statistics(),
        "healthy": True,
    }


###############################################################################


def reset_statistics() -> None:
    """
    Reset runtime statistics.
    """

    _PAGINATION_STATS["requests"] = 0
    _PAGINATION_STATS["items_processed"] = 0

###############################################################################
# Helpers
###############################################################################

def build_response(
    items: list[Any],
    request: PaginationRequest,
    total: int,
) -> dict[str, Any]:
    """
    Build a standard offset-pagination response.
    """

    paginated_items = paginate(
        items,
        request,
    )

    _PAGINATION_STATS["requests"] += 1
    _PAGINATION_STATS["items_processed"] += len(paginated_items)

    return {
        "items": paginated_items,
        "meta": metadata(
            total=total,
            page=request.page,
            page_limit=request.limit,
        ),
    }


###############################################################################


def build_cursor_response(
    items: list[Any],
    request: CursorRequest,
    next_token: str | None,
) -> dict[str, Any]:
    """
    Build a cursor-pagination response.
    """

    _PAGINATION_STATS["requests"] += 1
    _PAGINATION_STATS["items_processed"] += len(items)

    response = CursorResponse(
        cursor=request.cursor,
        next_cursor=next_token,
        previous_cursor=None,
        limit=request.limit,
        has_next=next_token is not None,
    )

    return {
        "items": items,
        "meta": response.model_dump(),
    }


###############################################################################


def validate_limit(
    value: int,
) -> int:
    """
    Validate page size.
    """

    if value < 1:
        raise ValueError("Limit must be greater than zero.")

    if value > MAX_LIMIT:
        raise ValueError(
            f"Limit cannot exceed {MAX_LIMIT}."
        )

    return value


###############################################################################


def validate_offset(
    value: int,
) -> int:
    """
    Validate offset.
    """

    if value < 0:
        raise ValueError(
            "Offset cannot be negative."
        )

    return value                