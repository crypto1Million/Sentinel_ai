###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from copy import deepcopy
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

###############################################################################
# OpenAPI Configuration
###############################################################################


def custom_openapi(
    app: FastAPI,
) -> dict[str, Any]:
    """
    Generate customized OpenAPI schema.
    """

    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=api_metadata()["title"],
        version=api_metadata()["version"],
        description=api_metadata()["description"],
        routes=app.routes,
    )

    schema["components"]["securitySchemes"] = security_scheme()

    inject_examples(schema)
    inject_tags(schema)

    app.openapi_schema = schema

    return app.openapi_schema


###############################################################################


def api_metadata() -> dict[str, str]:
    """
    API metadata.
    """

    return {
        "title": "WalletDNA API",
        "version": "1.0.0",
        "description": "Wallet Intelligence API",
    }


###############################################################################


def security_scheme() -> dict[str, Any]:
    """
    JWT Bearer security.
    """

    return {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }


###############################################################################


def websocket_schema() -> dict[str, Any]:
    """
    WebSocket metadata.
    """

    return {
        "wallet_stream": "/ws/wallet",
        "graph_stream": "/ws/graph",
        "alerts_stream": "/ws/alerts",
    }


###############################################################################


def examples_schema() -> dict[str, Any]:
    """
    Global example payloads.
    """

    return {
        "wallet": {
            "address": "ExampleWalletAddress",
        },
        "token": {
            "mint": "ExampleTokenMint",
        },
    }


###############################################################################
# Runtime
###############################################################################


def diagnostics() -> dict[str, Any]:
    """
    OpenAPI diagnostics.
    """

    return {
        "custom_openapi": True,
        "security": True,
    }


###############################################################################


def summary() -> dict[str, Any]:
    """
    OpenAPI summary.
    """

    return {
        "version": api_metadata()["version"],
        "title": api_metadata()["title"],
    }


###############################################################################
# Utilities
###############################################################################


def inject_examples(
    schema: dict[str, Any],
) -> None:
    """
    Inject global examples.
    """

    schema.setdefault(
        "x-examples",
        examples_schema(),
    )


###############################################################################


def inject_tags(
    schema: dict[str, Any],
) -> None:
    """
    Inject API tags.
    """

    schema.setdefault(
        "tags",
        [],
    )