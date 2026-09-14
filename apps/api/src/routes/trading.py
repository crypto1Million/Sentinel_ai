from __future__ import annotations

from enum import Enum
from typing import Any

from fastapi import (
    APIRouter,
    HTTPException,
)
from pydantic import (
    BaseModel,
    Field,
)

from chains.models import Chain
from trading.execution_options import (
    ExecutionMode,
)
from trading.trade_executor import (
    TradeExecutor,
)


router = APIRouter()

executor = TradeExecutor()


class QuoteRequest(BaseModel):
    chain: Chain
    input_token: str
    output_token: str
    amount: str

    wallet: str | None = None

    slippage_bps: int = Field(
        default=50,
        ge=1,
        le=10_000,
    )


class SwapRequest(BaseModel):
    chain: Chain

    input_token: str
    output_token: str
    amount: str

    wallet: str

    slippage_bps: int = Field(
        default=50,
        ge=1,
        le=10_000,
    )

    execution_mode: ExecutionMode = (
        ExecutionMode.AUTO
    )

    priority_fee: int | None = Field(
        default=None,
        ge=0,
    )

    jito_tip: int | None = Field(
        default=None,
        ge=0,
    )

    notional_usd: str


class ExecuteRequest(BaseModel):
    chain: Chain

    signed_transaction: str

    request_id: str


@router.post("/quote")
async def quote(
    request: QuoteRequest,
) -> dict[str, Any]:
    try:
        result = await executor.quote(
            chain=request.chain,
            input_token=request.input_token,
            output_token=request.output_token,
            amount=request.amount,
            wallet=request.wallet,
            slippage_bps=request.slippage_bps,
        )

        return {
            "status": "ok",
            **result,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error


@router.post("/swap")
async def swap(
    request: SwapRequest,
) -> dict[str, Any]:
    try:
        result = await executor.build_swap(
            chain=request.chain,
            input_token=request.input_token,
            output_token=request.output_token,
            amount=request.amount,
            wallet=request.wallet,
            slippage_bps=request.slippage_bps,
            priority_fee=request.priority_fee,
            jito_tip=request.jito_tip,
            execution_mode=request.execution_mode,
            notional_usd=request.notional_usd,
        )

        return {
            "status": "awaiting_signature",
            **result,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except NotImplementedError as error:
        raise HTTPException(
            status_code=501,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error


@router.post("/execute")
async def execute(
    request: ExecuteRequest,
) -> dict[str, Any]:
    try:
        result = await executor.execute_signed(
            chain=request.chain,
            signed_transaction=(
                request.signed_transaction
            ),
            request_id=request.request_id,
        )

        return {
            "status": "submitted",
            "chain": request.chain.value,
            "result": result,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except NotImplementedError as error:
        raise HTTPException(
            status_code=501,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error