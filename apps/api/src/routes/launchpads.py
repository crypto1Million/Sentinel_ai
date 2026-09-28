from __future__ import annotations

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
)

from chains.models import Chain
from launchpads.service import LaunchpadService


router = APIRouter()

service = LaunchpadService()


@router.get("")
async def list_launchpads(
    chain: Chain | None = Query(
        default=None
    ),
):
    launchpads = service.list(
        chain=chain
    )

    return {
        "chain": (
            chain.value
            if chain
            else "all"
        ),
        "count": len(launchpads),
        "launchpads": [
            service.serialize(item)
            for item in launchpads
        ],
    }


@router.get("/{chain}/{slug}")
async def launchpad(
    chain: Chain,
    slug: str,
):
    try:
        item = service.resolve(
            chain=chain,
            slug=slug,
        )

        return service.serialize(item)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error