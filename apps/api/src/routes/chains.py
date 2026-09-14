from __future__ import annotations

from fastapi import APIRouter

from chains.registry import list_chains


router = APIRouter()


@router.get("")
async def chains():
    return {
        "chains": [
            {
                "id": config.id.value,
                "name": config.name,
                "chain_type": (
                    config.chain_type.value
                ),
                "chain_id": config.chain_id,
                "native_symbol": (
                    config.native_symbol
                ),
                "explorer_url": (
                    config.explorer_url
                ),
                "enabled": config.enabled,
            }
            for config in list_chains()
        ]
    }