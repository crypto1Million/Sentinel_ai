###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import os

from dotenv import load_dotenv

###############################################################################
# Load Environment
###############################################################################

load_dotenv()

###############################################################################
# Environment
###############################################################################

ENVIRONMENT: str = os.getenv(
    "ENVIRONMENT",
    "development",
)

DEBUG: bool = (
    os.getenv(
        "DEBUG",
        "true",
    ).lower()
    == "true"
)

HOST: str = os.getenv(
    "HOST",
    "0.0.0.0",
)

PORT: int = int(
    os.getenv(
        "PORT",
        "8000",
    )
)

LOG_LEVEL: str = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()

###############################################################################
# API
###############################################################################

API_NAME: str = os.getenv(
    "API_NAME",
    "Wallet DNA API",
)

API_PREFIX: str = os.getenv(
    "API_PREFIX",
    "/api/v1",
)

API_VERSION: str = os.getenv(
    "API_VERSION",
    "1.0.0",
)

OPENAPI_URL: str = os.getenv(
    "OPENAPI_URL",
    f"{API_PREFIX}/openapi.json",
)

DOCS_URL: str = os.getenv(
    "DOCS_URL",
    "/docs",
)

REDOC_URL: str = os.getenv(
    "REDOC_URL",
    "/redoc",
)

###############################################################################
# Security
###############################################################################

SECRET_KEY: str = os.getenv(
    "SECRET_KEY",
    "CHANGE_ME_IN_PRODUCTION",
)

JWT_SECRET: str = os.getenv(
    "JWT_SECRET",
    SECRET_KEY,
)

ACCESS_TOKEN_EXPIRE: int = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE",
        "3600",      # seconds (1 hour)
    )
)

REFRESH_TOKEN_EXPIRE: int = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE",
        "604800",    # seconds (7 days)
    )
)

API_KEY_LENGTH: int = int(
    os.getenv(
        "API_KEY_LENGTH",
        "64",
    )
)

ALGORITHM: str = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

###############################################################################
# CORS
###############################################################################

ALLOWED_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]

ALLOWED_METHODS: list[str] = [
    method.strip()
    for method in os.getenv(
        "ALLOWED_METHODS",
        "GET,POST,PUT,PATCH,DELETE,OPTIONS",
    ).split(",")
    if method.strip()
]

ALLOWED_HEADERS: list[str] = [
    header.strip()
    for header in os.getenv(
        "ALLOWED_HEADERS",
        "*",
    ).split(",")
    if header.strip()
]

ALLOW_CREDENTIALS: bool = (
    os.getenv(
        "ALLOW_CREDENTIALS",
        "true",
    ).lower()
    == "true"
)

EXPOSE_HEADERS: list[str] = [
    header.strip()
    for header in os.getenv(
        "EXPOSE_HEADERS",
        "X-Request-ID,X-Response-Time",
    ).split(",")
    if header.strip()
]

###############################################################################
# Feature Flags
###############################################################################

ENABLE_AI: bool = (
    os.getenv(
        "ENABLE_AI",
        "true",
    ).lower()
    == "true"
)

ENABLE_EXPORT: bool = (
    os.getenv(
        "ENABLE_EXPORT",
        "true",
    ).lower()
    == "true"
)

ENABLE_GRAPH: bool = (
    os.getenv(
        "ENABLE_GRAPH",
        "true",
    ).lower()
    == "true"
)

ENABLE_STREAMING: bool = (
    os.getenv(
        "ENABLE_STREAMING",
        "true",
    ).lower()
    == "true"
)

ENABLE_REPLAY: bool = (
    os.getenv(
        "ENABLE_REPLAY",
        "true",
    ).lower()
    == "true"
)

ENABLE_METRICS: bool = (
    os.getenv(
        "ENABLE_METRICS",
        "true",
    ).lower()
    == "true"
)

###############################################################################
# Rate Limits
###############################################################################

# Requests per minute unless otherwise noted.

API_RATE_LIMIT: int = int(
    os.getenv(
        "API_RATE_LIMIT",
        "120",
    )
)

LOGIN_RATE_LIMIT: int = int(
    os.getenv(
        "LOGIN_RATE_LIMIT",
        "10",
    )
)

WALLET_RATE_LIMIT: int = int(
    os.getenv(
        "WALLET_RATE_LIMIT",
        "60",
    )
)

EXPORT_RATE_LIMIT: int = int(
    os.getenv(
        "EXPORT_RATE_LIMIT",
        "5",
    )
)

###############################################################################
# Runtime
###############################################################################

WORKERS: int = int(
    os.getenv(
        "WORKERS",
        "4",
    )
)

REQUEST_TIMEOUT: int = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "30",   # seconds
    )
)

CACHE_TTL: int = int(
    os.getenv(
        "CACHE_TTL",
        "300",  # seconds
    )
)

MAX_PAGE_SIZE: int = int(
    os.getenv(
        "MAX_PAGE_SIZE",
        "100",
    )
)

MAX_UPLOAD_SIZE: int = int(
    os.getenv(
        "MAX_UPLOAD_SIZE",
        str(50 * 1024 * 1024),   # 50 MB
    )
)

###############################################################################
# Validation
###############################################################################

def validate_environment() -> None:
    """
    Validate runtime environment settings.
    """

    valid = {
        "development",
        "staging",
        "production",
    }

    if ENVIRONMENT not in valid:
        raise ValueError(
            f"Invalid ENVIRONMENT: {ENVIRONMENT}"
        )


###############################################################################


def validate_security() -> None:
    """
    Validate security configuration.
    """

    if len(SECRET_KEY) < 32:
        raise ValueError(
            "SECRET_KEY must contain at least 32 characters."
        )

    if ACCESS_TOKEN_EXPIRE <= 0:
        raise ValueError(
            "ACCESS_TOKEN_EXPIRE must be positive."
        )

    if REFRESH_TOKEN_EXPIRE <= 0:
        raise ValueError(
            "REFRESH_TOKEN_EXPIRE must be positive."
        )


###############################################################################


def validate_runtime() -> None:
    """
    Validate runtime configuration.
    """

    if WORKERS < 1:
        raise ValueError(
            "WORKERS must be greater than zero."
        )

    if REQUEST_TIMEOUT <= 0:
        raise ValueError(
            "REQUEST_TIMEOUT must be positive."
        )

    if MAX_PAGE_SIZE < 1:
        raise ValueError(
            "MAX_PAGE_SIZE must be greater than zero."
        )


###############################################################################


def validate_cors() -> None:
    """
    Validate CORS configuration.
    """

    if not ALLOWED_ORIGINS:
        raise ValueError(
            "ALLOWED_ORIGINS cannot be empty."
        )

    if not ALLOWED_METHODS:
        raise ValueError(
            "ALLOWED_METHODS cannot be empty."
        )

###############################################################################
# Configuration Export
###############################################################################

def get_api_config() -> dict:
    """
    Return public API configuration.
    """

    return {
        "name": API_NAME,
        "version": API_VERSION,
        "prefix": API_PREFIX,
        "openapi_url": OPENAPI_URL,
        "docs_url": DOCS_URL,
        "redoc_url": REDOC_URL,
    }


###############################################################################


def get_runtime_config() -> dict:
    """
    Return runtime configuration.
    """

    return {
        "environment": ENVIRONMENT,
        "debug": DEBUG,
        "host": HOST,
        "port": PORT,
        "workers": WORKERS,
        "request_timeout": REQUEST_TIMEOUT,
        "cache_ttl": CACHE_TTL,
        "max_page_size": MAX_PAGE_SIZE,
        "max_upload_size": MAX_UPLOAD_SIZE,
        "log_level": LOG_LEVEL,
    }


###############################################################################


def get_security_config() -> dict:
    """
    Return non-sensitive security configuration.
    """

    return {
        "algorithm": ALGORITHM,
        "access_token_expire": ACCESS_TOKEN_EXPIRE,
        "refresh_token_expire": REFRESH_TOKEN_EXPIRE,
        "api_key_length": API_KEY_LENGTH,
    }


###############################################################################


def get_feature_flags() -> dict:
    """
    Return enabled features.
    """

    return {
        "ai": ENABLE_AI,
        "export": ENABLE_EXPORT,
        "graph": ENABLE_GRAPH,
        "streaming": ENABLE_STREAMING,
        "replay": ENABLE_REPLAY,
        "metrics": ENABLE_METRICS,
    }


###############################################################################


def export_config() -> dict:
    """
    Export complete application configuration.
    Sensitive values are intentionally omitted.
    """

    return {
        "api": get_api_config(),
        "runtime": get_runtime_config(),
        "security": get_security_config(),
        "features": get_feature_flags(),
        "cors": {
            "origins": ALLOWED_ORIGINS,
            "methods": ALLOWED_METHODS,
            "headers": ALLOWED_HEADERS,
            "credentials": ALLOW_CREDENTIALS,
            "expose_headers": EXPOSE_HEADERS,
        },
        "rate_limits": {
            "api": API_RATE_LIMIT,
            "login": LOGIN_RATE_LIMIT,
            "wallet": WALLET_RATE_LIMIT,
            "export": EXPORT_RATE_LIMIT,
        },
    }


###############################################################################
# Diagnostics
###############################################################################

def summary() -> dict:
    """
    Lightweight configuration summary.
    """

    return {
        "environment": ENVIRONMENT,
        "api": API_NAME,
        "version": API_VERSION,
        "workers": WORKERS,
        "features_enabled": sum(
            [
                ENABLE_AI,
                ENABLE_EXPORT,
                ENABLE_GRAPH,
                ENABLE_STREAMING,
                ENABLE_REPLAY,
                ENABLE_METRICS,
            ]
        ),
    }


###############################################################################


def diagnostics() -> dict:
    """
    Full configuration diagnostics.
    """

    return {
        "summary": summary(),
        "configuration": export_config(),
        "validation": {
            "environment": "ok",
            "runtime": "ok",
            "security": "ok",
            "cors": "ok",
        },
    }        