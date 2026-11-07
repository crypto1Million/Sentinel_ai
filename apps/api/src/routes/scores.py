from fastapi import APIRouter, HTTPException, Query

from intelligence.feature_store import (
    get_intelligence_feature_store,
)
from intelligence.sentinel_score import SentinelScoreEngine


router = APIRouter()
engine = SentinelScoreEngine()


async def _calculate(
    mint: str,
    chain: str,
) -> dict:

    if not mint.strip():
        raise HTTPException(
            status_code=400,
            detail="Token mint is required",
        )

    features = await get_intelligence_feature_store().get(
        chain,
        mint,
    )

    result = engine.calculate(features)

    return {
        "mint": mint,
        "chain": chain,
        **result,
    }


@router.get("/{mint}")
async def score(
    mint: str,
    chain: str = Query(
        default="solana",
        min_length=1,
        max_length=32,
    ),
):
    """Return current potential score and independent Rug Risk."""

    return await _calculate(
        mint,
        chain,
    )


@router.get("/{mint}/breakdown")
async def breakdown(
    mint: str,
    chain: str = Query(
        default="solana",
        min_length=1,
        max_length=32,
    ),
):
    """Return six-pillar breakdown and individual risk evidence."""

    result = await _calculate(
        mint,
        chain,
    )

    return {
        "mint": result["mint"],
        "chain": result["chain"],

        "model_name": result["model_name"],
        "model_version": result["model_version"],

        "potential_score": result["potential_score"],
        "potential_status": result["potential_status"],
        "potential_grade": result["potential_grade"],

        "rug_risk_score": result["rug_risk_score"],
        "rug_risk_status": result["rug_risk_status"],
        "rug_risk_coverage_pct": result["rug_risk_coverage_pct"],
        "rug_risk_confidence_pct": result["rug_risk_confidence_pct"],
        "rug_hard_veto": result["rug_hard_veto"],

        "data_coverage_pct": result["data_coverage_pct"],
        "confidence_pct": result["confidence_pct"],

        "pillars": result["pillars"],
        "risk_flags": result["risk_flags"],
        "risk_components": result["risk_components"],

        "scored_at": result["scored_at"],
    }