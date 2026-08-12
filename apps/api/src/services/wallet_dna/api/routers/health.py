###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from api.responses import success
from api.version import (
    API_VERSION,
    BUILD_NUMBER,
)

###############################################################################
# Router
###############################################################################

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

###############################################################################
# GET Endpoints
###############################################################################

@router.get("/")
async def health():
    """
    General health endpoint.
    """

    return success(
        {
            "status": "healthy",
        }
    )


###############################################################################


@router.get("/ready")
async def ready():
    """
    Readiness probe.
    """

    return success(
        {
            "ready": True,
        }
    )


###############################################################################


@router.get("/live")
async def live():
    """
    Liveness probe.
    """

    return success(
        {
            "live": True,
        }
    )


###############################################################################


@router.get("/version")
async def version():
    """
    API version.
    """

    return success(
        {
            "version": API_VERSION,
            "build": BUILD_NUMBER,
        }
    )


###############################################################################


@router.get("/dependencies")
async def dependencies():
    """
    External dependency status.
    """
    pass


###############################################################################


@router.get("/metrics")
async def metrics():
    """
    Runtime metrics.
    """
    pass


###############################################################################


@router.get("/uptime")
async def uptime():
    """
    Service uptime.
    """
    pass


###############################################################################


@router.get("/diagnostics")
async def diagnostics():
    """
    Diagnostics.
    """
    pass


###############################################################################


@router.get("/status")
async def status():
    """
    Overall status.
    """
    pass


###############################################################################
# Runtime
###############################################################################

@router.get("/summary")
async def router_summary():
    """
    Router summary.
    """

    return {
        "router": "health",
        "version": API_VERSION,
        "endpoints": 9,
    }


###############################################################################
# Utilities
###############################################################################

def build_health_response(
    data: Any,
) -> dict:
    """
    Standard health response.
    """

    return success(data)