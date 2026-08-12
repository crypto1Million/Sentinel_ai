from fastapi import APIRouter

router = APIRouter()


@router.get("/{wallet}")
async def get_wallet(
    wallet: str
):

    return {

        "wallet": wallet,

        "classification": "UNKNOWN",

        "win_rate": 0,

        "avg_roi": 0
    }


@router.get("/{wallet}/trades")
async def get_trades(
    wallet: str
):

    return {

        "wallet": wallet,

        "trades": []
    }


@router.get("/{wallet}/dna")
async def wallet_dna(
    wallet: str
):

    return {

        "wallet": wallet,

        "specialization": [],

        "copy_score": 0
    }