from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    APP_NAME: str = "Sentinel AI"

    API_HOST: str = "0.0.0.0"

    API_PORT: int = 8000

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    POSTGRES_DB: str

    REDIS_HOST: str

    REDIS_PORT: int

    HELIUS_API_KEY: str = ""

    DEXSCREENER_API: str = ""

    JUPITER_API: str = ""

    RAYDIUM_API: str = ""

    ENVIRONMENT: str = "development"

    LOG_LEVEL: str = "INFO"

    class Config:

        env_file = ".env"


@lru_cache
def get_settings():

    return Settings()

BASE_RPC_URL: str = "https://mainnet.base.org"

BASE_WSS_URL: str = "wss://mainnet.base.org"

BASE_FLASHBLOCKS_RPC_URL: str = (
    "https://mainnet-preconf.base.org"
)

BASE_FLASHBLOCKS_WSS_URL: str = (
    "wss://mainnet-preconf.base.org"
)

BASE_CHAIN_ID: int = 8453

BASE_USDC_ADDRESS: str = (
    "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
)

BASE_WETH_ADDRESS: str = (
    "0x4200000000000000000000000000000000000006"
)

AERODROME_FACTORY_ADDRESS: str = (
    "0x420DD381b31aEf6683db6B902084cB0FFECe40Da"
)

AERODROME_ROUTER_ADDRESS: str = (
    "0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43"
)    

ROBINHOOD_RPC_URL: str = ""

JUPITER_API_KEY: str = ""

PLATFORM_FEE_BPS: int = 50

SOLANA_RPC_URL: str = ""
BASE_RPC_URL: str = "https://mainnet.base.org"
ETHEREUM_RPC_URL: str = ""
BNB_RPC_URL: str = ""
ROBINHOOD_RPC_URL: str = ""