from fastapi import APIRouter

router = APIRouter()


@router.get("/{mint}")
async def score(
    mint: str
):

    return {

        "mint": mint,

        "sentinel_score": 0,

        "grade": "D",

        "recommendation": "AVOID"
    }


@router.get("/{mint}/breakdown")
async def breakdown(
    mint: str
):

    return {

        "dev_quality": 0,

        "wallet_quality": 0,

        "volume_quality": 0,

        "social_strength": 0,

        "narrative_momentum": 0,

        "rug_risk": 0,

        "opportunity_score": 0
    }