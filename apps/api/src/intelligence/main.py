from __future__ import annotations

import asyncio

from fastapi import FastAPI

from config.logging import setup_logging
from database.init_db import init_database

from intelligence.worker import (
    get_intelligence_worker,
)

from routes.chains import router as chains_router
from routes.narratives import router as narrative_router
from routes.scores import router as score_router
from routes.tokens import router as token_router
from routes.trading import router as trading_router
from routes.wallets import router as wallet_router

from websocket.score_stream import router as score_ws
from websocket.token_stream import router as token_ws
from websocket.wallet_stream import router as wallet_ws


logger = setup_logging()

app = FastAPI(
    title="Sentinel AI",
    version="1.0.0",
)


_intelligence_task: asyncio.Task | None = None


@app.on_event("startup")
async def startup():

    global _intelligence_task

    logger.info(
        "Starting Sentinel API..."
    )

    init_database()

    worker = (
        get_intelligence_worker()
    )

    _intelligence_task = asyncio.create_task(
        worker.run(),
        name="sentinel-intelligence-worker",
    )


@app.on_event("shutdown")
async def shutdown():

    global _intelligence_task

    worker = (
        get_intelligence_worker()
    )

    await worker.stop()

    if _intelligence_task is not None:

        _intelligence_task.cancel()

        try:
            await _intelligence_task
        except asyncio.CancelledError:
            pass

        _intelligence_task = None


@app.get("/")
async def root():

    return {
        "name": "Sentinel AI",
        "status": "running",
        "realtime": True,
    }


app.include_router(
    token_router,
    prefix="/tokens",
    tags=["Tokens"],
)

app.include_router(
    wallet_router,
    prefix="/wallets",
    tags=["Wallets"],
)

app.include_router(
    score_router,
    prefix="/scores",
    tags=["Scores"],
)

app.include_router(
    narrative_router,
    prefix="/narratives",
    tags=["Narratives"],
)

app.include_router(
    trading_router,
    prefix="/trading",
    tags=["Trading"],
)

app.include_router(
    token_ws,
)

app.include_router(
    wallet_ws,
)

app.include_router(
    score_ws,
)

app.include_router(
    chains_router,
    prefix="/chains",
    tags=["chains"],
)