###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any, Optional

from fastapi import status

###############################################################################
# Base Exception
###############################################################################

class WalletDNAException(Exception):
    """
    Base exception for the Wallet DNA platform.

    All custom exceptions should inherit
    from this class.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "WALLET_DNA_ERROR",
        details: Optional[Any] = None,
    ) -> None:

        super().__init__(message)

        self.message = message

        self.status_code = status_code

        self.error_code = error_code

        self.details = details

    ###########################################################################

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the exception.
        """

        return {

            "success": False,

            "error": self.message,

            "error_code": self.error_code,

            "details": self.details,

        }

    ###########################################################################

    def __str__(self) -> str:

        return self.message

###############################################################################
# Authentication Exceptions
###############################################################################

class AuthenticationError(WalletDNAException):
    """
    General authentication failure.
    """

    def __init__(
        self,
        message: str = "Authentication failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
            details=details,
        )


###############################################################################


class AuthorizationError(WalletDNAException):
    """
    Permission denied.
    """

    def __init__(
        self,
        message: str = "Access denied.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
            details=details,
        )


###############################################################################


class InvalidAPIKey(AuthenticationError):
    """
    Invalid API key.
    """

    def __init__(
        self,
        message: str = "Invalid API key.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "INVALID_API_KEY"


###############################################################################


class InvalidJWT(AuthenticationError):
    """
    Invalid JWT token.
    """

    def __init__(
        self,
        message: str = "Invalid JWT token.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "INVALID_JWT"


###############################################################################


class WalletSignatureError(AuthenticationError):
    """
    Wallet signature verification failed.
    """

    def __init__(
        self,
        message: str = "Wallet signature verification failed.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "WALLET_SIGNATURE_ERROR"


###############################################################################


class SessionExpired(AuthenticationError):
    """
    Session has expired.
    """

    def __init__(
        self,
        message: str = "Session expired.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "SESSION_EXPIRED"

###############################################################################
# Authentication Exceptions
###############################################################################

class AuthenticationError(WalletDNAException):
    """
    General authentication failure.
    """

    def __init__(
        self,
        message: str = "Authentication failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
            details=details,
        )


###############################################################################


class AuthorizationError(WalletDNAException):
    """
    Permission denied.
    """

    def __init__(
        self,
        message: str = "Access denied.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
            details=details,
        )


###############################################################################


class InvalidAPIKey(AuthenticationError):
    """
    Invalid API key.
    """

    def __init__(
        self,
        message: str = "Invalid API key.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "INVALID_API_KEY"


###############################################################################


class InvalidJWT(AuthenticationError):
    """
    Invalid JWT token.
    """

    def __init__(
        self,
        message: str = "Invalid JWT token.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "INVALID_JWT"


###############################################################################


class WalletSignatureError(AuthenticationError):
    """
    Wallet signature verification failed.
    """

    def __init__(
        self,
        message: str = "Wallet signature verification failed.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "WALLET_SIGNATURE_ERROR"


###############################################################################


class SessionExpired(AuthenticationError):
    """
    Session has expired.
    """

    def __init__(
        self,
        message: str = "Session expired.",
    ) -> None:

        super().__init__(
            message=message,
        )

        self.error_code = "SESSION_EXPIRED"

###############################################################################
# Validation Exceptions
###############################################################################

class ValidationException(WalletDNAException):
    """
    Base validation exception.
    """

    def __init__(
        self,
        message: str = "Validation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details,
        )


###############################################################################


class WalletValidationError(ValidationException):
    """
    Wallet validation error.
    """

    def __init__(
        self,
        message: str = "Invalid wallet address.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "WALLET_VALIDATION_ERROR"


###############################################################################


class TokenValidationError(ValidationException):
    """
    Token validation error.
    """

    def __init__(
        self,
        message: str = "Invalid token.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "TOKEN_VALIDATION_ERROR"


###############################################################################


class GraphValidationError(ValidationException):
    """
    Graph validation error.
    """

    def __init__(
        self,
        message: str = "Graph validation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "GRAPH_VALIDATION_ERROR"


###############################################################################


class QueryValidationError(ValidationException):
    """
    Search/query validation error.
    """

    def __init__(
        self,
        message: str = "Invalid query.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "QUERY_VALIDATION_ERROR"


###############################################################################
# Database Exceptions
###############################################################################

class DatabaseError(WalletDNAException):
    """
    Base database exception.
    """

    def __init__(
        self,
        message: str = "Database operation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
            details=details,
        )


###############################################################################


class RedisError(DatabaseError):
    """
    Redis exception.
    """

    def __init__(
        self,
        message: str = "Redis operation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "REDIS_ERROR"


###############################################################################


class Neo4jError(DatabaseError):
    """
    Neo4j exception.
    """

    def __init__(
        self,
        message: str = "Neo4j operation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "NEO4J_ERROR"


###############################################################################


class ClickHouseError(DatabaseError):
    """
    ClickHouse exception.
    """

    def __init__(
        self,
        message: str = "ClickHouse operation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "CLICKHOUSE_ERROR"


###############################################################################


class TransactionError(DatabaseError):
    """
    Database transaction exception.
    """

    def __init__(
        self,
        message: str = "Transaction failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "TRANSACTION_ERROR"

###############################################################################
# Graph Exceptions
###############################################################################

class GraphError(WalletDNAException):
    """
    Base graph-analysis exception.
    """

    def __init__(
        self,
        message: str = "Graph operation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="GRAPH_ERROR",
            details=details,
        )


###############################################################################


class ClusterError(GraphError):
    """
    Wallet cluster analysis failure.
    """

    def __init__(
        self,
        message: str = "Cluster analysis failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "CLUSTER_ERROR"


###############################################################################


class FundingError(GraphError):
    """
    Funding graph analysis failure.
    """

    def __init__(
        self,
        message: str = "Funding analysis failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "FUNDING_ERROR"


###############################################################################


class BundleError(GraphError):
    """
    Bundle detection failure.
    """

    def __init__(
        self,
        message: str = "Bundle detection failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "BUNDLE_ERROR"


###############################################################################


class WalletDNAError(GraphError):
    """
    Wallet DNA engine failure.
    """

    def __init__(
        self,
        message: str = "Wallet DNA analysis failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "WALLET_DNA_ERROR"

###############################################################################
# Search Exceptions
###############################################################################

class SearchError(WalletDNAException):
    """
    Base search exception.
    """

    def __init__(
        self,
        message: str = "Search operation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="SEARCH_ERROR",
            details=details,
        )


###############################################################################


class WalletNotFound(SearchError):
    """
    Wallet not found.
    """

    def __init__(
        self,
        wallet: str,
    ) -> None:

        super().__init__(
            message=f"Wallet '{wallet}' not found.",
        )

        self.error_code = "WALLET_NOT_FOUND"


###############################################################################


class TokenNotFound(SearchError):
    """
    Token not found.
    """

    def __init__(
        self,
        token: str,
    ) -> None:

        super().__init__(
            message=f"Token '{token}' not found.",
        )

        self.error_code = "TOKEN_NOT_FOUND"


###############################################################################


class DeployerNotFound(SearchError):
    """
    Deployer not found.
    """

    def __init__(
        self,
        deployer: str,
    ) -> None:

        super().__init__(
            message=f"Deployer '{deployer}' not found.",
        )

        self.error_code = "DEPLOYER_NOT_FOUND"


###############################################################################


class BundleNotFound(SearchError):
    """
    Bundle not found.
    """

    def __init__(
        self,
        bundle: str,
    ) -> None:

        super().__init__(
            message=f"Bundle '{bundle}' not found.",
        )

        self.error_code = "BUNDLE_NOT_FOUND"


###############################################################################


class ClusterNotFound(SearchError):
    """
    Cluster not found.
    """

    def __init__(
        self,
        cluster: str,
    ) -> None:

        super().__init__(
            message=f"Cluster '{cluster}' not found.",
        )

        self.error_code = "CLUSTER_NOT_FOUND"

###############################################################################
# Export Exceptions
###############################################################################

class ExportError(WalletDNAException):
    """
    Base export exception.
    """

    def __init__(
        self,
        message: str = "Export operation failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="EXPORT_ERROR",
            details=details,
        )


###############################################################################


class ExportFailed(ExportError):
    """
    Export job failed.
    """

    def __init__(
        self,
        message: str = "Export failed.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            details=details,
        )

        self.error_code = "EXPORT_FAILED"


###############################################################################


class UnsupportedFormat(ExportError):
    """
    Unsupported export format.
    """

    def __init__(
        self,
        export_format: str,
    ) -> None:

        super().__init__(
            message=f"Unsupported export format: {export_format}",
        )

        self.error_code = "UNSUPPORTED_EXPORT_FORMAT"


###############################################################################


class FileGenerationError(ExportError):
    """
    File generation failed.
    """

    def __init__(
        self,
        filename: str,
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=f"Failed to generate file: {filename}",
            details=details,
        )

        self.error_code = "FILE_GENERATION_ERROR"

###############################################################################
# Runtime Exceptions
###############################################################################

class RateLimitExceeded(WalletDNAException):
    """
    Request rate limit exceeded.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details,
        )


###############################################################################


class ServiceUnavailable(WalletDNAException):
    """
    Backend service unavailable.
    """

    def __init__(
        self,
        message: str = "Service unavailable.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="SERVICE_UNAVAILABLE",
            details=details,
        )


###############################################################################


class TimeoutException(WalletDNAException):
    """
    Request timed out.
    """

    def __init__(
        self,
        message: str = "Operation timed out.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            error_code="TIMEOUT_EXCEPTION",
            details=details,
        )


###############################################################################


class InternalRuntimeError(WalletDNAException):
    """
    Unexpected runtime failure.
    """

    def __init__(
        self,
        message: str = "Internal runtime error.",
        details: Any | None = None,
    ) -> None:

        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="INTERNAL_RUNTIME_ERROR",
            details=details,
        )

###############################################################################
# FastAPI Exception Handlers
###############################################################################

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


###############################################################################


async def walletdna_exception_handler(
    request: Request,
    exc: WalletDNAException,
) -> JSONResponse:
    """
    Handle all custom Wallet DNA exceptions.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


###############################################################################


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle FastAPI/Pydantic validation errors.
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation failed.",
            "error_code": "REQUEST_VALIDATION_ERROR",
            "details": exc.errors(),
        },
    )


###############################################################################


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """
    Handle HTTP exceptions.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "error_code": "HTTP_EXCEPTION",
        },
    )


###############################################################################


async def runtime_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Catch unexpected runtime exceptions.
    """

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error.",
            "error_code": "UNHANDLED_EXCEPTION",
        },
    )


###############################################################################


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register all exception handlers.
    """

    app.add_exception_handler(
        WalletDNAException,
        walletdna_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        runtime_exception_handler,
    )

###############################################################################
# Utilities
###############################################################################

def format_error(
    exc: WalletDNAException,
) -> dict[str, Any]:
    """
    Convert an exception into a standardized
    error payload.
    """

    return {
        "success": False,
        "error": exc.message,
        "error_code": exc.error_code,
        "details": exc.details,
        "status_code": exc.status_code,
    }


###############################################################################


def build_response(
    *,
    success: bool,
    message: str,
    data: Any | None = None,
    error_code: str | None = None,
) -> dict[str, Any]:
    """
    Build a standardized API response.
    """

    return {
        "success": success,
        "message": message,
        "error_code": error_code,
        "data": data,
    }


###############################################################################


def diagnostics() -> dict[str, Any]:
    """
    Exception module diagnostics.
    """

    return {
        "module": "wallet_dna.api.exceptions",
        "base_exception": WalletDNAException.__name__,
        "registered_handlers": [
            "walletdna_exception_handler",
            "validation_exception_handler",
            "http_exception_handler",
            "runtime_exception_handler",
        ],
        "custom_exception_count": len(
            WalletDNAException.__subclasses__()
        ),
        "status": "healthy",
    }                                                                            