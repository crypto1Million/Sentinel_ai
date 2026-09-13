from enum import Enum

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()


class Chain(str, Enum):
    SOLANA = "solana"
    BASE = "base"


class QuoteRequest(BaseModel):
    chain: Chain
    input_token: str
    output_token: str
    amount: str


class SwapRequest(BaseModel):
    chain: Chain
    input_token: str
    output_token: str
    amount: str
    wallet: str
    slippage_bps: int = 50


@router.post("/quote")
async def quote(
    request: QuoteRequest,
):
    if request.chain == Chain.SOLANA:
        return {
            "status": "ok",
            "chain": "solana",
            "input_token": request.input_token,
            "output_token": request.output_token,
            "amount": request.amount,
        }

    if request.chain == Chain.BASE:
        return {
            "status": "ready",
            "chain": "base",
            "input_token": request.input_token,
            "output_token": request.output_token,
            "amount": request.amount,
            "execution": "aerodrome",
        }

    raise HTTPException(
        status_code=400,
        detail="Unsupported chain",
    )


@router.post("/swap")
async def swap(
    request: SwapRequest,
):
    if request.chain == Chain.BASE:
        return {
            "status": "awaiting_signature",
            "chain": "base",
            "wallet": request.wallet,
            "message": (
                "Unsigned Base transaction "
                "must be built and signed by "
                "the user's wallet."
            ),
        }

    return {
        "status": "pending",
        "chain": "solana",
    }