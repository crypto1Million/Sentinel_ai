###############################################################################
# Standard Library
###############################################################################

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar
from uuid import uuid4

###############################################################################
# FastAPI
###############################################################################

from fastapi import status

from fastapi.responses import (
    JSONResponse,
    Response,
)

###############################################################################
# Internal Schemas
###############################################################################

from wallet_dna.api.schemas import (
    SuccessResponse,
    ErrorResponse,
    MessageResponse,
    PaginationResponse,
    HealthResponse,
    StatusResponse,
    ExportResponse,
    StatisticsResponse,
)

###############################################################################
# Internal Configuration
###############################################################################

from wallet_dna.api.version import API_VERSION

###############################################################################
# Constants
###############################################################################

DEFAULT_SUCCESS_MESSAGE = "Success"

DEFAULT_ERROR_MESSAGE = "An unexpected error occurred."

DEFAULT_CONTENT_TYPE = "application/json"

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

API_VERSION = "v1"

###############################################################################
# Response Headers
###############################################################################

HEADER_REQUEST_ID = "X-Request-ID"

HEADER_PROCESS_TIME = "X-Process-Time"

HEADER_API_VERSION = "X-API-Version"

HEADER_CONTENT_TYPE = "Content-Type"

###############################################################################
# Success Responses
###############################################################################

def success(
    data: Any = None,
    message: str = "Success",
) -> JSONResponse:
    """
    Standard 200 response.
    """

    payload = SuccessResponse(

        message=message,

        data=data,

    )

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content=payload.model_dump(mode="json"),

    )


###############################################################################


def created(
    data: Any = None,
    message: str = "Resource created.",
) -> JSONResponse:
    """
    Standard 201 response.
    """

    payload = SuccessResponse(

        message=message,

        data=data,

    )

    return JSONResponse(

        status_code=status.HTTP_201_CREATED,

        content=payload.model_dump(mode="json"),

    )


###############################################################################


def accepted(
    data: Any = None,
    message: str = "Request accepted.",
) -> JSONResponse:
    """
    Standard 202 response.
    """

    payload = SuccessResponse(

        message=message,

        data=data,

    )

    return JSONResponse(

        status_code=status.HTTP_202_ACCEPTED,

        content=payload.model_dump(mode="json"),

    )


###############################################################################


def no_content() -> Response:
    """
    Standard 204 response.
    """

    return Response(

        status_code=status.HTTP_204_NO_CONTENT,

    )


###############################################################################


def message(
    message: str,
) -> JSONResponse:
    """
    Message-only response.
    """

    payload = MessageResponse(

        message=message,

    )

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content=payload.model_dump(mode="json"),

    )

###############################################################################
# Error Responses
###############################################################################

def error(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    error_code: str | None = None,
    details: Any = None,
) -> JSONResponse:
    """
    Generic error response.
    """

    payload = ErrorResponse(
        error=message,
        error_code=error_code,
        details=details,
    )

    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(mode="json"),
    )


###############################################################################


def bad_request(
    message: str = "Bad request.",
    details: Any = None,
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
        error_code="BAD_REQUEST",
        details=details,
    )


###############################################################################


def unauthorized(
    message: str = "Unauthorized.",
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_code="UNAUTHORIZED",
    )


###############################################################################


def forbidden(
    message: str = "Forbidden.",
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_403_FORBIDDEN,
        error_code="FORBIDDEN",
    )


###############################################################################


def not_found(
    message: str = "Resource not found.",
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="NOT_FOUND",
    )


###############################################################################


def conflict(
    message: str = "Conflict detected.",
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_409_CONFLICT,
        error_code="CONFLICT",
    )


###############################################################################


def validation_error(
    details: Any,
    message: str = "Validation failed.",
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_ERROR",
        details=details,
    )


###############################################################################


def rate_limited(
    retry_after: int = 60,
    message: str = "Rate limit exceeded.",
) -> JSONResponse:

    response = error(
        message=message,
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        error_code="RATE_LIMITED",
    )

    response.headers["Retry-After"] = str(retry_after)

    return response


###############################################################################


def server_error(
    message: str = "Internal server error.",
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_SERVER_ERROR",
    )


###############################################################################


def service_unavailable(
    message: str = "Service unavailable.",
) -> JSONResponse:

    return error(
        message=message,
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        error_code="SERVICE_UNAVAILABLE",
    )

###############################################################################
# Pagination Responses
###############################################################################

def paginated_response(
    *,
    items: list[Any],
    page: int,
    page_size: int,
    total_items: int,
    message: str = "Success",
) -> JSONResponse:
    """
    Standard page-based response.
    """

    total_pages = (
        (total_items + page_size - 1) // page_size
        if page_size > 0
        else 0
    )

    payload = PaginationResponse(

        message=message,

        items=items,

        page=page,

        page_size=page_size,

        total_items=total_items,

        total_pages=total_pages,

        has_next=page < total_pages,

        has_previous=page > 1,

    )

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content=payload.model_dump(mode="json"),

    )


###############################################################################


def cursor_response(
    *,
    items: list[Any],
    next_cursor: str | None,
    previous_cursor: str | None = None,
    has_more: bool = False,
    message: str = "Success",
) -> JSONResponse:
    """
    Standard cursor-based response.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content={

            "success": True,

            "message": message,

            "items": items,

            "pagination": {

                "next_cursor": next_cursor,

                "previous_cursor": previous_cursor,

                "has_more": has_more,

            },

            "timestamp": datetime.utcnow().isoformat(),

        },

    )        

###############################################################################
# Export Responses
###############################################################################

from fastapi.responses import FileResponse

###############################################################################


def export_started(
    export_id: str,
    message: str = "Export started.",
) -> JSONResponse:
    """
    Export job accepted.
    """

    return JSONResponse(

        status_code=status.HTTP_202_ACCEPTED,

        content={

            "success": True,

            "message": message,

            "export_id": export_id,

            "status": "running",

            "timestamp": datetime.utcnow().isoformat(),

        },

    )


###############################################################################


def export_completed(
    export_id: str,
    filename: str,
    download_url: str,
    message: str = "Export completed.",
) -> JSONResponse:
    """
    Export completed successfully.
    """

    payload = ExportResponse(

        export_id=export_id,

        filename=filename,

        format=filename.split(".")[-1],

        status=ExportStatus.COMPLETED,

        download_url=download_url,

    )

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content=payload.model_dump(mode="json"),

    )


###############################################################################


def export_failed(
    export_id: str,
    reason: str,
) -> JSONResponse:
    """
    Export failed.
    """

    payload = ExportResponse(

        export_id=export_id,

        filename="",

        format="",

        status=ExportStatus.FAILED,

        download_url=None,

    )

    data = payload.model_dump(mode="json")

    data["reason"] = reason

    return JSONResponse(

        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

        content=data,

    )


###############################################################################


def download(
    file_path: str,
    filename: str,
) -> FileResponse:
    """
    Download exported file.
    """

    return FileResponse(

        path=file_path,

        filename=filename,

        media_type="application/octet-stream",

    )

###############################################################################
# Statistics Responses
###############################################################################

def statistics(
    data: StatisticsResponse,
) -> JSONResponse:
    """
    Standard statistics response.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content={

            "success": True,

            "message": "Statistics generated.",

            "data": data.model_dump(mode="json"),

            "timestamp": datetime.utcnow().isoformat(),

        },

    )


###############################################################################


def metrics(
    metrics: list[Metric],
) -> JSONResponse:
    """
    Return metric collection.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content={

            "success": True,

            "message": "Metrics retrieved.",

            "metrics": [

                metric.model_dump(mode="json")

                for metric in metrics

            ],

            "count": len(metrics),

            "timestamp": datetime.utcnow().isoformat(),

        },

    )


###############################################################################


def diagnostics(
    runtime: RuntimeMeta,
) -> JSONResponse:
    """
    Runtime diagnostics response.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content={

            "success": True,

            "message": "Diagnostics report.",

            "runtime": runtime.model_dump(mode="json"),

            "timestamp": datetime.utcnow().isoformat(),

        },

    )

###############################################################################
# Health Responses
###############################################################################

def health(
    response: HealthResponse,
) -> JSONResponse:
    """
    General health status.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content=response.model_dump(mode="json"),

    )


###############################################################################


def ready(
    message: str = "Service is ready.",
) -> JSONResponse:
    """
    Readiness probe.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content={

            "success": True,

            "status": "ready",

            "message": message,

            "timestamp": datetime.utcnow().isoformat(),

        },

    )


###############################################################################


def live(
    message: str = "Service is alive.",
) -> JSONResponse:
    """
    Liveness probe.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content={

            "success": True,

            "status": "alive",

            "message": message,

            "timestamp": datetime.utcnow().isoformat(),

        },

    )


###############################################################################


def version() -> JSONResponse:
    """
    API version response.
    """

    return JSONResponse(

        status_code=status.HTTP_200_OK,

        content={

            "api_version": API_VERSION,

            "generated_at": datetime.utcnow().isoformat(),

        },

    )

###############################################################################
# Runtime Responses
###############################################################################

def runtime_status(
    runtime: RuntimeMeta,
) -> JSONResponse:
    """
    Runtime status response.
    """

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "runtime": runtime.model_dump(mode="json"),
            "timestamp": timestamp(),
        },
    )


###############################################################################


def progress(
    task_id: str,
    current: int,
    total: int,
    message: str = "Task in progress.",
) -> JSONResponse:
    """
    Progress response.
    """

    percentage = (
        round((current / total) * 100, 2)
        if total > 0
        else 0.0
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "task_id": task_id,
            "current": current,
            "total": total,
            "percentage": percentage,
            "message": message,
            "timestamp": timestamp(),
        },
    )


###############################################################################


def task_started(
    task_id: str,
    message: str = "Task started.",
) -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "success": True,
            "task_id": task_id,
            "status": "started",
            "message": message,
            "timestamp": timestamp(),
        },
    )


###############################################################################


def task_completed(
    task_id: str,
    result: Any = None,
    message: str = "Task completed.",
) -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "task_id": task_id,
            "status": "completed",
            "result": result,
            "message": message,
            "timestamp": timestamp(),
        },
    )


###############################################################################


def task_failed(
    task_id: str,
    reason: str,
) -> JSONResponse:

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "task_id": task_id,
            "status": "failed",
            "reason": reason,
            "timestamp": timestamp(),
        },
    )


###############################################################################
# Utilities
###############################################################################

def timestamp() -> str:
    """
    Current UTC timestamp.
    """

    return datetime.utcnow().isoformat()


###############################################################################


def response_id() -> str:
    """
    Unique response identifier.
    """

    return str(uuid4())


###############################################################################


def envelope(
    *,
    success: bool,
    data: Any = None,
    message: str = "",
) -> dict:
    """
    Standard response envelope.
    """

    return {
        "id": response_id(),
        "success": success,
        "message": message,
        "data": data,
        "timestamp": timestamp(),
    }


###############################################################################


def headers() -> dict[str, str]:
    """
    Standard API response headers.
    """

    return {
        HEADER_REQUEST_ID: response_id(),
        HEADER_API_VERSION: API_VERSION,
        HEADER_CONTENT_TYPE: "application/json",
    }                
