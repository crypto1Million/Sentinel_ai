from fastapi import APIRouter

from app.chains.registry import CHAINS


router = APIRouter(
    prefix="/api/chains",
    tags=["chains"],
)


@router.get("")
async def list_chains():

    return [
        {
            "id": config.id.value,
            "name": config.name,
            "type": config.chain_type.value,
            "chain_id": config.chain_id,
            "native_symbol": config.native_symbol,
            "explorer_url": config.explorer_url,
        }
        for config in CHAINS.values()
    ]