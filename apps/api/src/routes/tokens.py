from enum import Enum

from fastapi import APIRouter, HTTPException, Query

from chains.base_client import BaseClient
from services.base_token_ingestion import BaseTokenIngestion
from services.base_dex import BaseDexDiscovery
from services.base_holder_intelligence import (
    BaseHolderIntelligence,
)
from services.base_rug_radar import BaseRugRadar


router = APIRouter()


class ChainQuery(str, Enum):
    SOLANA = "solana"
    BASE = "base"


base_client = BaseClient()
base_ingestion = BaseTokenIngestion(
    base_client
)
base_dex = BaseDexDiscovery(
    base_client
)
base_holders = BaseHolderIntelligence(
    base_client
)
base_rug = BaseRugRadar(
    base_client
)


@router.get("/")
async def get_tokens(
    chain: ChainQuery = Query(
        ChainQuery.SOLANA
    ),
):
    return {
        "status": "success",
        "chain": chain.value,
        "tokens": [],
    }


@router.get("/{address}")
async def get_token(
    address: str,
    chain: ChainQuery = Query(
        ChainQuery.SOLANA
    ),
):
    if chain == ChainQuery.SOLANA:
        return {
            "chain": "solana",
            "mint": address,
            "symbol": "UNKNOWN",
            "name": "Unknown Token",
            "market_cap": 0,
            "holders": 0,
        }

    try:
        return base_ingestion.ingest(
            address
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/{address}/holders")
async def get_holders(
    address: str,
    chain: ChainQuery = Query(
        ChainQuery.SOLANA
    ),
):
    if chain == ChainQuery.SOLANA:
        return {
            "chain": "solana",
            "mint": address,
            "holders": [],
        }

    try:
        return base_holders.analyze(
            address
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/{address}/rug-analysis")
async def rug_analysis(
    address: str,
    chain: ChainQuery = Query(
        ChainQuery.SOLANA
    ),
):
    if chain == ChainQuery.SOLANA:
        return {
            "chain": "solana",
            "mint": address,
            "bundle_percent": 0,
            "sniper_percent": 0,
            "insider_percent": 0,
        }

    try:
        pools = base_dex.discover(
            address
        )

        holders = base_holders.analyze(
            address
        )

        return base_rug.analyze(
            address,
            top10_percent=holders[
                "top10_percent"
            ],
            pool_count=len(pools),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc