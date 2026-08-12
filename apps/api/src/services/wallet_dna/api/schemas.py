###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

###############################################################################
# Base Models
###############################################################################

class APIModel(BaseModel):
    """
    Base schema for all API models.
    """

    model_config = ConfigDict(

        from_attributes=True,

        populate_by_name=True,

        extra="ignore",

        validate_assignment=True,

        str_strip_whitespace=True,

    )


###############################################################################


class TimestampModel(APIModel):
    """
    Common timestamp fields.
    """

    created_at: Optional[datetime] = Field(

        default=None,

        description="Creation timestamp",

    )

    updated_at: Optional[datetime] = Field(

        default=None,

        description="Last update timestamp",

    )


###############################################################################


class PaginationModel(APIModel):
    """
    Shared pagination metadata.
    """

    page: int = Field(

        default=1,

        ge=1,

        description="Current page",

    )

    page_size: int = Field(

        default=50,

        ge=1,

        le=500,

        description="Items per page",

    )

    total_items: int = Field(

        default=0,

        ge=0,

        description="Total available items",

    )

    total_pages: int = Field(

        default=0,

        ge=0,

        description="Total number of pages",

    )

    has_next: bool = Field(

        default=False,

        description="Next page exists",

    )

    has_previous: bool = Field(

        default=False,

        description="Previous page exists",

    )

###############################################################################
# Pagination Schemas
###############################################################################

from typing import Generic, Optional, TypeVar

from pydantic import Field

T = TypeVar("T")

###############################################################################


class PaginationRequest(APIModel):
    """
    Standard pagination request.
    """

    page: int = Field(

        default=1,

        ge=1,

        description="Requested page number",

    )

    page_size: int = Field(

        default=50,

        ge=1,

        le=500,

        description="Number of records per page",

    )


###############################################################################


class PaginationResponse(
    PaginationModel,
    Generic[T],
):
    """
    Generic paginated response.
    """

    items: list[T] = Field(

        default_factory=list,

        description="Returned items",

    )


###############################################################################


class CursorPagination(APIModel):
    """
    Cursor-based pagination.

    Used for infinite scrolling and
    high-performance graph queries.
    """

    cursor: Optional[str] = Field(

        default=None,

        description="Current cursor",

    )

    next_cursor: Optional[str] = Field(

        default=None,

        description="Next cursor",

    )

    previous_cursor: Optional[str] = Field(

        default=None,

        description="Previous cursor",

    )

    limit: int = Field(

        default=100,

        ge=1,

        le=1000,

        description="Maximum returned records",

    )

    has_more: bool = Field(

        default=False,

        description="More records available",

    )

###############################################################################
# Sorting Schemas
###############################################################################

from enum import Enum

from pydantic import Field

###############################################################################


class SortOrder(str, Enum):
    """
    Supported sorting directions.
    """

    ASC = "asc"

    DESC = "desc"


###############################################################################


class SortRequest(APIModel):
    """
    Generic sorting request.
    """

    sort_by: str = Field(

        default="created_at",

        description="Field used for sorting",

        examples=[

            "created_at",

            "balance",

            "wallet_score",

            "volume",

            "holders",

            "market_cap",

        ],

    )

    order: SortOrder = Field(

        default=SortOrder.DESC,

        description="Sorting direction",

    )

    ignore_case: bool = Field(

        default=True,

        description="Case-insensitive string sorting",

    )

    nulls_last: bool = Field(

        default=True,

        description="Place NULL values at the end",

    )

###############################################################################
# Filtering Schemas
###############################################################################

from datetime import datetime
from typing import Any, Optional

from pydantic import Field

###############################################################################


class DateFilter(APIModel):
    """
    Filter records by date/time range.
    """

    start_date: Optional[datetime] = Field(
        default=None,
        description="Start datetime",
    )

    end_date: Optional[datetime] = Field(
        default=None,
        description="End datetime",
    )


###############################################################################


class RangeFilter(APIModel):
    """
    Numeric range filter.
    """

    minimum: Optional[float] = Field(
        default=None,
        description="Minimum value",
    )

    maximum: Optional[float] = Field(
        default=None,
        description="Maximum value",
    )


###############################################################################


class SearchFilter(APIModel):
    """
    Generic text search.
    """

    query: str = Field(
        default="",
        description="Search query",
    )

    exact_match: bool = Field(
        default=False,
        description="Require exact match",
    )

    case_sensitive: bool = Field(
        default=False,
        description="Case-sensitive search",
    )

    fuzzy: bool = Field(
        default=True,
        description="Enable fuzzy matching",
    )


###############################################################################


class FilterRequest(APIModel):
    """
    Generic API filter object.
    """

    search: Optional[SearchFilter] = None

    date: Optional[DateFilter] = None

    numeric: Optional[RangeFilter] = None

    tags: list[str] = Field(
        default_factory=list,
        description="Filter tags",
    )

    labels: list[str] = Field(
        default_factory=list,
        description="Wallet or token labels",
    )

    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description="Custom filters",
    )

###############################################################################
# Generic Response Schemas
###############################################################################

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import Field

T = TypeVar("T")

###############################################################################


class SuccessResponse(APIModel, Generic[T]):
    """
    Generic success response.
    """

    success: bool = Field(
        default=True,
        description="Request status",
    )

    message: str = Field(
        default="Success",
        description="Response message",
    )

    data: Optional[T] = Field(
        default=None,
        description="Response payload",
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp",
    )


###############################################################################


class ErrorResponse(APIModel):
    """
    Generic error response.
    """

    success: bool = Field(
        default=False,
        description="Request status",
    )

    error: str = Field(
        ...,
        description="Error message",
    )

    error_code: Optional[str] = Field(
        default=None,
        description="Internal error code",
    )

    details: Optional[Any] = Field(
        default=None,
        description="Additional error details",
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp",
    )


###############################################################################


class MessageResponse(APIModel):
    """
    Simple message response.
    """

    success: bool = Field(
        default=True,
    )

    message: str = Field(
        ...,
        description="Response message",
    )


###############################################################################


class HealthResponse(APIModel):
    """
    Health endpoint response.
    """

    status: str = Field(
        default="healthy",
    )

    uptime: float = Field(
        default=0.0,
        description="Seconds since startup",
    )

    version: str = Field(
        ...,
        description="API version",
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )


###############################################################################


class StatusResponse(APIModel):
    """
    Runtime status response.
    """

    service: str = Field(
        ...,
        description="Service name",
    )

    status: str = Field(
        default="running",
    )

    version: str = Field(
        ...,
    )

    ready: bool = Field(
        default=True,
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )

###############################################################################
# Validation Schemas
###############################################################################

class ErrorDetail(APIModel):
    """
    Individual validation error.
    """

    field: str = Field(
        ...,
        description="Field name",
    )

    message: str = Field(
        ...,
        description="Validation message",
    )

    value: Any | None = Field(
        default=None,
        description="Invalid value",
    )


###############################################################################


class FieldError(APIModel):
    """
    Field validation error.
    """

    field: str = Field(
        ...,
    )

    errors: list[str] = Field(
        default_factory=list,
    )


###############################################################################


class ValidationError(APIModel):
    """
    Generic validation response.
    """

    success: bool = False

    error: str = "Validation failed"

    details: list[ErrorDetail] = Field(
        default_factory=list,
    )


###############################################################################
# Metadata Schemas
###############################################################################

class PaginationMeta(APIModel):
    """
    Pagination metadata.
    """

    page: int

    page_size: int

    total_items: int

    total_pages: int

    has_next: bool

    has_previous: bool


###############################################################################


class QueryMeta(APIModel):
    """
    Query execution metadata.
    """

    execution_time_ms: float = Field(
        default=0.0,
    )

    cached: bool = Field(
        default=False,
    )

    records_returned: int = Field(
        default=0,
    )

    query: str | None = None


###############################################################################


class RuntimeMeta(APIModel):
    """
    Runtime information.
    """

    uptime_seconds: float = Field(
        default=0.0,
    )

    cpu_usage: float = Field(
        default=0.0,
    )

    memory_usage: float = Field(
        default=0.0,
    )

    active_requests: int = Field(
        default=0,
    )


###############################################################################


class VersionMeta(APIModel):
    """
    Version metadata.
    """

    api_version: str

    build_version: str

    git_commit: str | None = None

    environment: str

    release_date: datetime                


###############################################################################
# Statistics Schemas
###############################################################################

class Metric(APIModel):
    """
    Generic metric.
    """

    name: str = Field(...)

    value: float | int = Field(...)

    unit: str | None = Field(default=None)

    description: str | None = Field(default=None)


###############################################################################


class Counter(APIModel):
    """
    Counter metric.
    """

    name: str = Field(...)

    count: int = Field(..., ge=0)


###############################################################################


class StatisticsResponse(APIModel):
    """
    Generic statistics response.
    """

    metrics: list[Metric] = Field(
        default_factory=list,
    )

    counters: list[Counter] = Field(
        default_factory=list,
    )

    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


###############################################################################
# Authentication Schemas
###############################################################################

class APIKeySchema(APIModel):
    """
    API Key.
    """

    api_key: str = Field(...)

    expires_at: datetime | None = None


###############################################################################


class JWTToken(APIModel):
    """
    JWT Token.
    """

    access_token: str

    token_type: str = "bearer"

    expires_in: int


###############################################################################


class WalletSchema(APIModel):
    """
    Connected wallet.
    """

    address: str

    label: str | None = None

    verified: bool = False


###############################################################################


class UserSchema(APIModel):
    """
    Authenticated user.
    """

    id: str

    username: str

    email: str | None = None

    is_admin: bool = False

    wallet: WalletSchema | None = None

    created_at: datetime | None = None

###############################################################################
# Export Schemas
###############################################################################

from enum import Enum
from typing import Any

###############################################################################


class ExportStatus(str, Enum):
    """
    Export task status.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


###############################################################################


class ExportRequest(APIModel):
    """
    Export request.
    """

    format: str = Field(
        default="json",
        examples=[
            "json",
            "csv",
            "graphml",
            "neo4j",
            "snapshot",
        ],
    )

    compression: bool = False

    include_metadata: bool = True

    filters: dict[str, Any] = Field(
        default_factory=dict,
    )


###############################################################################


class ExportResponse(APIModel):
    """
    Export response.
    """

    export_id: str

    filename: str

    format: str

    status: ExportStatus

    download_url: str | None = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


###############################################################################
# Utilities
###############################################################################

class ExampleGenerator:
    """
    Generates OpenAPI examples.
    """

    @staticmethod
    def wallet() -> dict:

        return {

            "address": "5PjM9...abc",

            "label": "Smart Money",

            "verified": True,

        }

    ###########################################################################

    @staticmethod
    def token() -> dict:

        return {

            "mint": "So11111111111111111111111111111111111111112",

            "symbol": "SOL",

            "name": "Solana",

        }

    ###########################################################################

    @staticmethod
    def export() -> dict:

        return {

            "format": "graphml",

            "compression": True,

            "include_metadata": True,

        }


###############################################################################


class SchemaVersion(APIModel):
    """
    Schema version information.
    """

    version: str = "1.0.0"

    api_version: str = API_VERSION

    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


###############################################################################


class JSONEncoder:
    """
    Shared JSON encoder helpers.
    """

    @staticmethod
    def encode(
        obj: Any,
    ) -> Any:
        """
        Convert Python objects into JSON-safe values.
        """

        if isinstance(obj, datetime):

            return obj.isoformat()

        if isinstance(obj, Enum):

            return obj.value

        if hasattr(obj, "model_dump"):

            return obj.model_dump()

        return obj        