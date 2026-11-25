from __future__ import annotations

from fastapi import APIRouter, HTTPException

from chains.models import Chain
from chains.registry import list_chains
from chains.router import get_chain_adapter


router = APIRouter()


@router.get("")
async def chains():
    return {
        "chains": [
            {
                "id": config.id.value,
                "name": config.name,
                "chain_type": config.chain_type.value,
                "chain_id": config.chain_id,
                "native_symbol": config.native_symbol,
                "explorer_url": config.explorer_url,
                "enabled": config.enabled,
            }
            for config in list_chains()
        ]
    }


@router.get("/{chain_name}/health")
async def chain_health(chain_name: str):
    try:
        chain = Chain(chain_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Unsupported chain: {chain_name}",
        ) from exc

    try:
        adapter = get_chain_adapter(chain)
        return await adapter.health()

    except (RuntimeError, ValueError) as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc