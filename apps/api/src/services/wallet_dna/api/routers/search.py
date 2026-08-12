###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from api.responses import success

###############################################################################
# Router
###############################################################################

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

###############################################################################
# Dependencies
###############################################################################

# Inject search service/database here.

###############################################################################
# GET Endpoints
###############################################################################

@router.get("/")
async def global_search(
    q: str = Query(...),
):
    """
    Global search.
    """
    pass


###############################################################################


@router.get("/wallet")
async def search_wallet(
    q: str = Query(...),
):
    """
    Search wallets.
    """
    pass


###############################################################################


@router.get("/token")
async def search_token(
    q: str = Query(...),
):
    """
    Search tokens.
    """
    pass


###############################################################################


@router.get("/deployer")
async def search_deployer(
    q: str = Query(...),
):
    """
    Search deployers.
    """
    pass


###############################################################################


@router.get("/bundle")
async def search_bundle(
    q: str = Query(...),
):
    """
    Search bundles.
    """
    pass


###############################################################################


@router.get("/cluster")
async def search_cluster(
    q: str = Query(...),
):
    """
    Search clusters.
    """
    pass


###############################################################################


@router.get("/graph")
async def search_graph(
    q: str = Query(...),
):
    """
    Search graph entities.
    """
    pass


###############################################################################


@router.get("/autocomplete")
async def autocomplete(
    q: str = Query(...),
):
    """
    Autocomplete search.
    """
    pass


###############################################################################


@router.get("/recent")
async def recent_searches():
    """
    Recent searches.
    """
    pass


###############################################################################
# POST Endpoints
###############################################################################

@router.post("/advanced")
async def advanced_search(
    query: dict,
):
    """
    Advanced search.
    """
    pass


###############################################################################


@router.post("/save")
async def save_search(
    query: dict,
):
    """
    Save search.
    """
    pass


###############################################################################
# Runtime
###############################################################################

@router.get("/diagnostics")
async def diagnostics():
    """
    Router diagnostics.
    """

    return {
        "router": "search",
        "status": "healthy",
    }


###############################################################################


@router.get("/summary")
async def router_summary():
    """
    Router summary.
    """

    return {
        "router": "search",
        "version": "1.0.0",
        "endpoints": 11,
    }


###############################################################################
# Utilities
###############################################################################

def validate_query(
    query: str,
) -> bool:
    """
    Validate search query.
    """

    return (
        isinstance(query, str)
        and len(query.strip()) > 0
    )


###############################################################################


def build_search_response(
    data: Any,
) -> dict:
    """
    Standard search response.
    """

    return success(data)