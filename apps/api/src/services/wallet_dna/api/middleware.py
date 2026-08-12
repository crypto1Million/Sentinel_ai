###############################################################################
# Standard Library
###############################################################################

from __future__ import annotations

import logging
import time
import uuid
from typing import Callable

###############################################################################
# FastAPI / Starlette
###############################################################################

from fastapi import Request
from fastapi.responses import Response, JSONResponse

from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from starlette.types import (
    ASGIApp,
)

###############################################################################
# Internal Modules
###############################################################################

from wallet_dna.api.config import APIConfig
from wallet_dna.api.dependencies import (
    get_rate_limiter,
    get_metrics,
)

###############################################################################
# Logger
###############################################################################

logger = logging.getLogger("wallet_dna.middleware")

###############################################################################
# Constants
###############################################################################

REQUEST_ID_HEADER = "X-Request-ID"

PROCESS_TIME_HEADER = "X-Process-Time"

API_VERSION_HEADER = "X-API-Version"

MAX_REQUEST_SIZE = 50 * 1024 * 1024  # 50 MB

###############################################################################
# Base Middleware
###############################################################################

class WalletDNABaseMiddleware(BaseHTTPMiddleware):
    """
    Base middleware for all Wallet DNA middleware.
    """

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:

        super().__init__(app)

        self.config = APIConfig()

        self.metrics = get_metrics()

        self.rate_limiter = get_rate_limiter()

###############################################################################
# Request Logging Middleware
###############################################################################

class RequestLoggingMiddleware(
    WalletDNABaseMiddleware,
):
    """
    Logs every request and response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        start_time = time.perf_counter()

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        self.log_request(
            request=request,
            request_id=request_id,
        )

        try:

            response = await call_next(
                request
            )

            duration = (
                time.perf_counter() - start_time
            )

            response.headers[
                REQUEST_ID_HEADER
            ] = request_id

            self.log_response(

                request=request,

                response=response,

                duration=duration,

                request_id=request_id,

            )

            return response

        except Exception as exc:

            duration = (
                time.perf_counter() - start_time
            )

            self.log_exception(

                request=request,

                exception=exc,

                duration=duration,

                request_id=request_id,

            )

            raise


    ###########################################################################

    def log_request(
        self,
        request: Request,
        request_id: str,
    ) -> None:
        """
        Log incoming request.
        """

        logger.info(

            "REQUEST | %s | %s | %s | %s",

            request_id,

            request.method,

            request.url.path,

            request.client.host
            if request.client
            else "unknown",

        )


    ###########################################################################

    def log_response(
        self,
        request: Request,
        response: Response,
        duration: float,
        request_id: str,
    ) -> None:
        """
        Log outgoing response.
        """

        logger.info(

            "RESPONSE | %s | %s | %s | %d | %.3f sec",

            request_id,

            request.method,

            request.url.path,

            response.status_code,

            duration,

        )


    ###########################################################################

    def log_exception(
        self,
        request: Request,
        exception: Exception,
        duration: float,
        request_id: str,
    ) -> None:
        """
        Log request exception.
        """

        logger.exception(

            "EXCEPTION | %s | %s | %s | %.3f sec | %s",

            request_id,

            request.method,

            request.url.path,

            duration,

            str(exception),

        )

###############################################################################
# Timing Middleware
###############################################################################

class TimingMiddleware(
    WalletDNABaseMiddleware,
):
    """
    Measures request execution time.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        start = self.start_timer()

        response = await call_next(request)

        elapsed = self.stop_timer(start)

        self.add_header(
            response=response,
            elapsed=elapsed,
        )

        return response

    ###########################################################################

    @staticmethod
    def start_timer() -> float:
        """
        Start high-resolution timer.
        """

        return time.perf_counter()

    ###########################################################################

    @staticmethod
    def stop_timer(
        started_at: float,
    ) -> float:
        """
        Stop timer.

        Returns
        -------
        float
            Seconds elapsed.
        """

        return time.perf_counter() - started_at

    ###########################################################################

    def add_header(
        self,
        response: Response,
        elapsed: float,
    ) -> None:
        """
        Attach timing information to the response.
        """

        response.headers[
            PROCESS_TIME_HEADER
        ] = f"{elapsed:.6f}"

        response.headers[
            API_VERSION_HEADER
        ] = API_VERSION

        logger.debug(

            "Process Time: %.6f sec",

            elapsed,

        )

        if self.metrics:

            self.metrics.record_request_time(
                elapsed
            )

###############################################################################
# Rate Limit Middleware
###############################################################################

class RateLimitMiddleware(
    WalletDNABaseMiddleware,
):
    """
    Redis-backed API rate limiting middleware.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        if not await self.check_limit(client_ip):

            return self.reject_request(client_ip)

        await self.increment_counter(client_ip)

        return await call_next(request)

    ###########################################################################

    async def check_limit(
        self,
        client_ip: str,
    ) -> bool:
        """
        Check whether the client is allowed to make another request.
        """

        current = await self.rate_limiter.get_counter(
            client_ip
        )

        return current < self.config.RATE_LIMIT_REQUESTS

    ###########################################################################

    async def increment_counter(
        self,
        client_ip: str,
    ) -> None:
        """
        Increment request counter.
        """

        await self.rate_limiter.increment(

            key=client_ip,

            ttl=self.config.RATE_LIMIT_WINDOW,

        )

    ###########################################################################

    def reject_request(
        self,
        client_ip: str,
    ) -> JSONResponse:
        """
        Return HTTP 429 response.
        """

        logger.warning(

            "Rate limit exceeded: %s",

            client_ip,

        )

        return JSONResponse(

            status_code=429,

            content={

                "success": False,

                "error": "Rate limit exceeded.",

                "retry_after": self.config.RATE_LIMIT_WINDOW,

            },

            headers={

                "Retry-After": str(
                    self.config.RATE_LIMIT_WINDOW
                ),

            },

        )

###############################################################################
# Request ID Middleware
###############################################################################

class RequestIDMiddleware(
    WalletDNABaseMiddleware,
):
    """
    Generates a unique Request ID for every request.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        request_id = self.generate_id()

        request.state.request_id = request_id

        response = await call_next(request)

        self.attach_id(

            response=response,

            request_id=request_id,

        )

        return response

    ###########################################################################

    @staticmethod
    def generate_id() -> str:
        """
        Generate a unique request identifier.

        Returns
        -------
        str
        """

        return str(uuid.uuid4())

    ###########################################################################

    def attach_id(
        self,
        response: Response,
        request_id: str,
    ) -> None:
        """
        Attach Request ID to response headers.
        """

        response.headers[
            REQUEST_ID_HEADER
        ] = request_id

        logger.debug(

            "Assigned Request ID: %s",

            request_id,

        )

###############################################################################
# Security Headers Middleware
###############################################################################

class SecurityHeadersMiddleware(
    WalletDNABaseMiddleware,
):
    """
    Adds standard security headers to every response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        response = await call_next(request)

        self.add_headers(response)

        self.remove_server_header(response)

        return response

    ###########################################################################

    def add_headers(
        self,
        response: Response,
    ) -> None:
        """
        Apply security headers.
        """

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"

        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"

        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; "
            "connect-src 'self' https: wss:;"
        )

        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

    ###########################################################################

    def remove_server_header(
        self,
        response: Response,
    ) -> None:
        """
        Remove framework/server identification headers.
        """

        response.headers.pop("server", None)

        response.headers.pop("Server", None)

        response.headers.pop("x-powered-by", None)

        response.headers.pop("X-Powered-By", None)

###############################################################################
# Compression Middleware
###############################################################################

import gzip
from io import BytesIO


class CompressionMiddleware(
    WalletDNABaseMiddleware,
):
    """
    Compresses large API responses using GZip.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        response = await call_next(request)

        if self.skip_small_payloads(response):
            return response

        return await self.gzip_response(response)

    ###########################################################################

    async def gzip_response(
        self,
        response: Response,
    ) -> Response:
        """
        Compress response body using GZip.

        Returns
        -------
        Response
        """

        body = b""

        async for chunk in response.body_iterator:
            body += chunk

        compressed = gzip.compress(body)

        headers = dict(response.headers)

        headers["Content-Encoding"] = "gzip"

        headers["Content-Length"] = str(len(compressed))

        headers["Vary"] = "Accept-Encoding"

        return Response(

            content=compressed,

            status_code=response.status_code,

            headers=headers,

            media_type=response.media_type,

        )

    ###########################################################################

    def skip_small_payloads(
        self,
        response: Response,
    ) -> bool:
        """
        Skip compression for small responses.

        Returns
        -------
        bool
        """

        content_length = response.headers.get(
            "Content-Length"
        )

        if content_length is None:
            return False

        return int(content_length) < 1024

###############################################################################
# CORS Middleware Factory
###############################################################################

from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp


class CORSMiddlewareFactory:
    """
    Factory for creating configured CORS middleware.
    """

    ###########################################################################

    @staticmethod
    def create(
        app: ASGIApp,
    ) -> CORSMiddleware:
        """
        Create a configured CORSMiddleware instance.

        Returns
        -------
        CORSMiddleware
        """

        config = APIConfig()

        return CORSMiddleware(

            app=app,

            allow_origins=config.CORS_ALLOW_ORIGINS,

            allow_credentials=config.CORS_ALLOW_CREDENTIALS,

            allow_methods=config.CORS_ALLOW_METHODS,

            allow_headers=config.CORS_ALLOW_HEADERS,

            expose_headers=config.CORS_EXPOSE_HEADERS,

            max_age=config.CORS_MAX_AGE,

        )

    ###########################################################################

    @staticmethod
    def configure(
        app,
    ) -> None:
        """
        Register CORS middleware with FastAPI.
        """

        config = APIConfig()

        app.add_middleware(

            CORSMiddleware,

            allow_origins=config.CORS_ALLOW_ORIGINS,

            allow_credentials=config.CORS_ALLOW_CREDENTIALS,

            allow_methods=config.CORS_ALLOW_METHODS,

            allow_headers=config.CORS_ALLOW_HEADERS,

            expose_headers=config.CORS_EXPOSE_HEADERS,

            max_age=config.CORS_MAX_AGE,

        )

###############################################################################
# Middleware Utilities
###############################################################################

from typing import Any


def client_ip(
    request: Request,
) -> str:
    """
    Return the real client IP address.
    """

    forwarded = request.headers.get(
        "X-Forwarded-For"
    )

    if forwarded:

        return forwarded.split(",")[0].strip()

    if request.client:

        return request.client.host

    return "unknown"


###############################################################################


def user_agent(
    request: Request,
) -> str:
    """
    Return client User-Agent.
    """

    return request.headers.get(

        "User-Agent",

        "unknown",

    )


###############################################################################


async def request_size(
    request: Request,
) -> int:
    """
    Return request body size in bytes.
    """

    body = await request.body()

    return len(body)


###############################################################################


def diagnostics() -> dict[str, Any]:
    """
    Return middleware diagnostics.
    """

    return {

        "request_logging": True,

        "timing": True,

        "rate_limiting": True,

        "request_id": True,

        "security_headers": True,

        "compression": True,

        "cors": True,

        "version": API_VERSION,

    }

###############################################################################
# Middleware Registry
###############################################################################

def register_middlewares(
    app,
) -> None:
    """
    Register all Wallet DNA middleware
    in the correct execution order.
    """

    ###########################################################################
    # Infrastructure
    ###########################################################################

    CORSMiddlewareFactory.configure(app)

    app.add_middleware(

        CompressionMiddleware,

    )

    ###########################################################################
    # Security
    ###########################################################################

    app.add_middleware(

        SecurityHeadersMiddleware,

    )

    app.add_middleware(

        RequestIDMiddleware,

    )

    ###########################################################################
    # Runtime
    ###########################################################################

    app.add_middleware(

        TimingMiddleware,

    )

    app.add_middleware(

        RateLimitMiddleware,

    )

    ###########################################################################
    # Logging
    ###########################################################################

    app.add_middleware(

        RequestLoggingMiddleware,

    )

    logger.info(

        "Wallet DNA middleware registered."

    )


###############################################################################


def middleware_summary() -> dict:
    """
    Return registered middleware information.
    """

    return {

        "registered": [

            "CORSMiddleware",

            "CompressionMiddleware",

            "SecurityHeadersMiddleware",

            "RequestIDMiddleware",

            "TimingMiddleware",

            "RateLimitMiddleware",

            "RequestLoggingMiddleware",

        ],

        "count": 7,

        "status": "active",

    }            
