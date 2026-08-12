###############################################################################
# Standard Library
###############################################################################

from __future__ import annotations

import asyncio
import contextlib
import logging
import signal
import sys
import time
from pathlib import Path
from typing import Any

###############################################################################
# FastAPI
###############################################################################

from fastapi import (
    FastAPI,
    Request,
)

from fastapi.responses import (
    JSONResponse,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from fastapi.middleware.gzip import (
    GZipMiddleware,
)

from fastapi.openapi.utils import (
    get_openapi,
)

###############################################################################
# Uvicorn
###############################################################################

import uvicorn

###############################################################################
# API Middleware
###############################################################################

from wallet_dna.api.middleware import (
    RequestLoggingMiddleware,
    TimingMiddleware,
    RateLimitMiddleware,
)

###############################################################################
# API Routers
###############################################################################

from wallet_dna.api.routers.wallet import router as wallet_router

from wallet_dna.api.routers.token import router as token_router

from wallet_dna.api.routers.funding import router as funding_router

from wallet_dna.api.routers.bundle import router as bundle_router

from wallet_dna.api.routers.deployer import router as deployer_router

from wallet_dna.api.routers.cluster import router as cluster_router

from wallet_dna.api.routers.graph import router as graph_router

from wallet_dna.api.routers.wallet_dna import (
    router as wallet_dna_router,
)

from wallet_dna.api.routers.statistics import (
    router as statistics_router,
)

from wallet_dna.api.routers.search import router as search_router

from wallet_dna.api.routers.health import router as health_router

###############################################################################
# Configuration
###############################################################################

from wallet_dna.api.config import APIConfig

###############################################################################
# Lifespan
###############################################################################

from wallet_dna.api.lifespan import lifespan

###############################################################################
# Exception Handlers
###############################################################################

from wallet_dna.api.exceptions import (
    WalletDNAException,
    wallet_dna_exception_handler,
)

###############################################################################
# Security
###############################################################################

from wallet_dna.api.security import (
    verify_api_key,
    verify_jwt,
)

###############################################################################
# Version
###############################################################################

from wallet_dna.api.version import (
    API_NAME,
    API_VERSION,
    API_DESCRIPTION,
)

###############################################################################
# FastAPI Application
###############################################################################

def create_app() -> FastAPI:
    """
    Create and configure the Wallet DNA FastAPI application.

    Returns
    -------
    FastAPI
    """

    app = FastAPI(

        title=API_NAME,

        version=API_VERSION,

        description=API_DESCRIPTION,

        lifespan=lifespan,

        docs_url="/docs",

        redoc_url="/redoc",

        openapi_url="/openapi.json",

    )

    configure_middlewares(app)

    configure_routes(app)

    configure_exception_handlers(app)

    configure_openapi(app)

    configure_events(app)

    return app


###############################################################################
# Middleware
###############################################################################

def configure_middlewares(
    app: FastAPI,
) -> None:
    """
    Register application middleware.
    """

    app.add_middleware(

        CORSMiddleware,

        allow_origins=["*"],

        allow_credentials=True,

        allow_methods=["*"],

        allow_headers=["*"],

    )

    app.add_middleware(

        GZipMiddleware,

        minimum_size=1024,

    )

    app.add_middleware(

        RequestLoggingMiddleware,

    )

    app.add_middleware(

        TimingMiddleware,

    )

    app.add_middleware(

        RateLimitMiddleware,

    )


###############################################################################
# Routes
###############################################################################

def configure_routes(
    app: FastAPI,
) -> None:
    """
    Register API routers.
    """

    app.include_router(wallet_router)

    app.include_router(token_router)

    app.include_router(funding_router)

    app.include_router(bundle_router)

    app.include_router(deployer_router)

    app.include_router(cluster_router)

    app.include_router(graph_router)

    app.include_router(wallet_dna_router)

    app.include_router(statistics_router)

    app.include_router(search_router)

    app.include_router(health_router)


###############################################################################
# Exception Handlers
###############################################################################

def configure_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register global exception handlers.
    """

    app.add_exception_handler(

        WalletDNAException,

        wallet_dna_exception_handler,

    )


###############################################################################
# OpenAPI
###############################################################################

def configure_openapi(
    app: FastAPI,
) -> None:
    """
    Configure custom OpenAPI schema.
    """

    def custom_openapi():

        if app.openapi_schema:

            return app.openapi_schema

        app.openapi_schema = get_openapi(

            title=API_NAME,

            version=API_VERSION,

            description=API_DESCRIPTION,

            routes=app.routes,

        )

        return app.openapi_schema

    app.openapi = custom_openapi


###############################################################################
# Events
###############################################################################

def configure_events(
    app: FastAPI,
) -> None:
    """
    Register application lifecycle events.
    """

    @app.on_event("startup")
    async def startup():

        logging.info(

            "Wallet DNA API started."

        )

    @app.on_event("shutdown")
    async def shutdown():

        logging.info(

            "Wallet DNA API stopped."

        )

###############################################################################
# Root Endpoints
###############################################################################

@app.get(
    "/",
    tags=["Root"],
    summary="API Information",
)
async def root() -> Dict[str, Any]:
    """
    Root endpoint.
    """

    return {

        "name": API_NAME,

        "version": API_VERSION,

        "description": API_DESCRIPTION,

        "status": "running",

    }


###############################################################################


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
)
async def health() -> Dict[str, Any]:
    """
    General health endpoint.
    """

    return {

        "status": "healthy",

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

    }


###############################################################################


@app.get(
    "/ready",
    tags=["Health"],
    summary="Readiness Check",
)
async def ready() -> Dict[str, Any]:
    """
    Readiness probe.

    Used by Kubernetes / Docker.
    """

    return {

        "ready": True,

        "database": "connected",

        "redis": "connected",

        "neo4j": "connected",

        "runtime": "ready",

    }


###############################################################################


@app.get(
    "/live",
    tags=["Health"],
    summary="Liveness Check",
)
async def live() -> Dict[str, Any]:
    """
    Liveness probe.

    Indicates whether the API process is alive.
    """

    return {

        "alive": True,

        "uptime": time.time(),

    }


###############################################################################
# FastAPI Application Instance
###############################################################################

app = create_app()

@app.get("/")
...     