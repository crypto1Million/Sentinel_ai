from fastapi import APIRouter
from fastapi import Query

router = APIRouter()


@router.get("/")
async def get_tokens():

    return {
        "status": "success",
        "message": "Token list endpoint"
    }


@router.get("/{mint}")
async def get_token(
    mint: str
):

    return {

        "mint": mint,

        "symbol": "UNKNOWN",

        "name": "Unknown Token",

        "market_cap": 0,

        "holders": 0
    }


@router.get("/{mint}/holders")
async def get_holders(
    mint: str
):

    return {

        "mint": mint,

        "holders": []
    }


@router.get("/{mint}/rug-analysis")
async def rug_analysis(
    mint: str
):

    return {

        "mint": mint,

        "bundle_percent": 0,

        "sniper_percent": 0,

        "insider_percent": 0
    }