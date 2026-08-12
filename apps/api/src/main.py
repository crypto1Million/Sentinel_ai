from fastapi import FastAPI

from routes.tokens import router as token_router

from routes.wallets import router as wallet_router

from routes.scores import router as score_router

from routes.narratives import router as narrative_router

from routes.trading import router as trading_router

from config.logging import setup_logging

from database.init_db import init_database

from websocket.token_stream import router as token_ws

from websocket.wallet_stream import router as wallet_ws

from websocket.score_stream import router as score_ws


logger = setup_logging()

app = FastAPI(

    title="Sentinel AI",

    version="1.0.0"
)


@app.on_event("startup")
async def startup():

    logger.info(
        "Starting Sentinel API..."
    )

    init_database()


@app.get("/")
async def root():

    return {

        "name": "Sentinel AI",

        "status": "running"
    }


app.include_router(

    token_router,

    prefix="/tokens",

    tags=["Tokens"]
)

app.include_router(

    wallet_router,

    prefix="/wallets",

    tags=["Wallets"]
)

app.include_router(

    score_router,

    prefix="/scores",

    tags=["Scores"]
)

app.include_router(

    narrative_router,

    prefix="/narratives",

    tags=["Narratives"]
)

app.include_router(

    trading_router,

    prefix="/trading",

    tags=["Trading"]
)

app.include_router(
    token_ws
)

app.include_router(
    wallet_ws
)

app.include_router(
    score_ws
)