from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from config.logging import setup_logging

from routes.tokens import router as token_router
from routes.wallets import router as wallet_router
from routes.scores import router as score_router
from routes.narratives import router as narrative_router
from routes.trading import router as trading_router
from routes.chains import router as chains_router

from routes.launchpads import (
    router as launchpad_router,
)

from routes.realtime import (
    router as realtime_router,
)

from realtime.bus import get_realtime_bus

from database.init_db import init_database

from websocket.token_stream import router as token_ws
from websocket.wallet_stream import router as wallet_ws
from websocket.score_stream import router as score_ws
from websocket.events_stream import router as events_ws


logger = setup_logging()

settings = get_settings()


app = FastAPI(
    title="Sentinel AI",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.CORS_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
async def startup():

    logger.info(
        "Starting Sentinel API..."
    )

    init_database()

    realtime_bus = get_realtime_bus()

    if await realtime_bus.ping():

        logger.info(
            "Realtime bus connected."
        )

    else:

        logger.error(
            "Realtime bus unavailable."
        )


# =========================================================
# SHUTDOWN
# =========================================================

@app.on_event("shutdown")
async def shutdown():

    logger.info(
        "Shutting down Sentinel API..."
    )

    try:

        await get_realtime_bus().close()

    except Exception:

        logger.exception(
            "Realtime bus shutdown failed."
        )


# =========================================================
# ROOT
# =========================================================

@app.get("/")
async def root():

    return {
        "name": "Sentinel AI",
        "status": "running",
    }


# =========================================================
# REST API ROUTES
# =========================================================

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
    chains_router,
    prefix="/chains",
    tags=["Chains"],
)

app.include_router(
    launchpad_router,
    prefix="/launchpads",
    tags=["Launchpads"],
)


# =========================================================
# EXISTING WEBSOCKET ROUTES
# =========================================================

app.include_router(
    token_ws,
)

app.include_router(
    wallet_ws,
)

app.include_router(
    score_ws,
)


# =========================================================
# NEW REALTIME GATEWAY
# =========================================================

app.include_router(
    realtime_router,
    prefix="/realtime",
    tags=["Realtime"],
)

app.include_router(
    events_ws,
)