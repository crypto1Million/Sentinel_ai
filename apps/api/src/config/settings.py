from __future__ import annotations

from functools import lru_cache
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central, typed configuration for SentinelAI."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "Sentinel AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "sentinel"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "sentinel"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    REDIS_STREAM_PREFIX: str = "sentinel"
    REDIS_EVENT_STREAM: str = "events"
    REDIS_TOKEN_STREAM: str = "token-events"
    REDIS_WALLET_STREAM: str = "wallet-events"
    REDIS_MARKET_STREAM: str = "market-events"
    REDIS_ALERT_STREAM: str = "alert-events"
    REDIS_SCORE_STREAM: str = "score-events"
    REDIS_STREAM_MAXLEN: int = 1_000_000
    REDIS_STREAM_BLOCK_MS: int = 5_000
    REDIS_STREAM_READ_COUNT: int = 100

    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    REALTIME_ENABLED: bool = True
    REALTIME_RECONNECT_DELAY_SECONDS: float = 2.0
    REALTIME_MAX_RECONNECT_DELAY_SECONDS: float = 30.0
    REALTIME_HEARTBEAT_SECONDS: int = 15
    REALTIME_PROVIDER_TIMEOUT_SECONDS: float = 15.0
    REALTIME_BACKFILL_ENABLED: bool = True
    REALTIME_DEDUP_ENABLED: bool = True
    REALTIME_RECONCILIATION_ENABLED: bool = True
    REALTIME_STALE_AFTER_SECONDS: float = 10.0

    HTTP_TIMEOUT_SECONDS: float = 15.0
    HTTP_CONNECT_TIMEOUT_SECONDS: float = 5.0
    HTTP_MAX_RETRIES: int = 3

    SOLANA_CHAIN_ID: str = "solana"
    SOLANA_NATIVE_SYMBOL: str = "SOL"
    SOLANA_RPC_URL: str = ""
    SOLANA_WSS_URL: str = ""
    HELIUS_API_KEY: str = ""
    HELIUS_WSS_URL: str = ""
    HELIUS_HTTP_URL: str = "https://mainnet.helius-rpc.com"
    HELIUS_WEBHOOK_URL: str = ""
    JUPITER_API_URL: str = "https://api.jup.ag"
    JUPITER_API_KEY: str = ""
    RAYDIUM_API_URL: str = "https://api-v3.raydium.io"

    ALCHEMY_API_KEY: str = ""
    BASE_CHAIN_ID: int = 8453
    BASE_NATIVE_SYMBOL: str = "ETH"
    BASE_RPC_URL: str = ""
    BASE_WSS_URL: str = ""
    BASE_FLASHBLOCKS_RPC_URL: str = "https://mainnet-preconf.base.org"
    BASE_FLASHBLOCKS_WSS_URL: str = ""
    BASE_USDC_ADDRESS: str = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    BASE_WETH_ADDRESS: str = "0x4200000000000000000000000000000000000006"
    AERODROME_FACTORY_ADDRESS: str = "0x420DD381b31aEf6683db6B902084cB0FFECe40Da"
    AERODROME_ROUTER_ADDRESS: str = "0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43"

    ETHEREUM_CHAIN_ID: int = 1
    ETHEREUM_NATIVE_SYMBOL: str = "ETH"
    ETHEREUM_RPC_URL: str = ""
    ETHEREUM_WSS_URL: str = ""

    BNB_CHAIN_ID: int = 56
    BNB_NATIVE_SYMBOL: str = "BNB"
    BNB_RPC_URL: str = ""
    BNB_WSS_URL: str = ""

    ROBINHOOD_CHAIN_ID: int = 4663
    ROBINHOOD_NATIVE_SYMBOL: str = "ETH"
    ROBINHOOD_RPC_URL: str = "https://rpc.mainnet.chain.robinhood.com"
    ROBINHOOD_WSS_URL: str = ""
    ROBINHOOD_SEQUENCER_FEED_URL: str = "wss://feed.mainnet.chain.robinhood.com"
    ROBINHOOD_SEQUENCER_URL: str = "https://sequencer.mainnet.chain.robinhood.com"

    ELYSIUM_CHAIN_ID: int = 99901
    ELYSIUM_NATIVE_SYMBOL: str = "HYPE"
    ELYSIUM_RPC_URL: str = ""
    ELYSIUM_WSS_URL: str = ""

    DEXSCREENER_API_URL: str = "https://api.dexscreener.com/latest"
    LAUNCHPAD_METADATA_REFRESH_SECONDS: int = 300
    LAUNCHPAD_ATTRIBUTION_REQUIRE_EVIDENCE: bool = True
    LAUNCHPAD_ALLOW_UNRESOLVED: bool = True
    REQUIRE_PROVENANCE: bool = True
    REQUIRE_OBSERVED_AT: bool = True
    REQUIRE_SOURCE_ID: bool = True
    REQUIRE_CHAIN_POSITION: bool = True
    EXTERNAL_DATA_STALE_AFTER_SECONDS: int = 60
    RECONCILIATION_INTERVAL_SECONDS: int = 60
    RECONCILIATION_BLOCK_LOOKBACK: int = 100
    RECONCILIATION_MAX_DRIFT_SECONDS: float = 5.0
    RAW_EVENT_RETENTION_DAYS: int = 90

    SCORE_ENGINE_ENABLED: bool = True
    SCORE_RECOMPUTE_ON_EVENT: bool = True
    SCORE_MODEL_VERSION: str = "1.0.0"
    SCORE_FEATURE_VERSION: str = "1.0.0"
    RUG_RADAR_ENABLED: bool = True
    RUG_RECOMPUTE_ON_AUTHORITY_CHANGE: bool = True
    RUG_RECOMPUTE_ON_LIQUIDITY_CHANGE: bool = True
    RUG_RECOMPUTE_ON_HOLDER_CHANGE: bool = True
    RUG_RECOMPUTE_ON_DEV_ACTIVITY: bool = True
    WALLET_DNA_ENABLED: bool = True
    WALLET_RECOMPUTE_ON_TRANSFER: bool = True
    WALLET_RECOMPUTE_ON_SWAP: bool = True
    WALLET_RECOMPUTE_ON_LP_EVENT: bool = True
    J7TRACKER_ENABLED: bool = True
    J7_POLL_INTERVAL_SECONDS: int = 15
    ALERTS_ENABLED: bool = True
    ALERT_DEDUP_WINDOW_SECONDS: int = 30
    TRADING_ENABLED: bool = False
    JITO_ENABLED: bool = True
    PRIORITY_FEES_ENABLED: bool = True
    PLATFORM_FEE_BPS: int = 50
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

    @model_validator(mode="after")
    def validate_production_configuration(self) -> "Settings":
        if self.ENVIRONMENT.lower() != "production":
            return self
        required = {
            "POSTGRES_PASSWORD": self.POSTGRES_PASSWORD,
            "JWT_SECRET": self.JWT_SECRET,
            "SOLANA_RPC_URL": self.SOLANA_RPC_URL,
            "HELIUS_API_KEY": self.HELIUS_API_KEY,
            "HELIUS_WSS_URL": self.HELIUS_WSS_URL,
            "BASE_RPC_URL": self.BASE_RPC_URL,
            "BASE_WSS_URL": self.BASE_WSS_URL,
            "ETHEREUM_RPC_URL": self.ETHEREUM_RPC_URL,
            "ETHEREUM_WSS_URL": self.ETHEREUM_WSS_URL,
            "BNB_RPC_URL": self.BNB_RPC_URL,
            "BNB_WSS_URL": self.BNB_WSS_URL,
            "ROBINHOOD_RPC_URL": self.ROBINHOOD_RPC_URL,
            "ROBINHOOD_WSS_URL": self.ROBINHOOD_WSS_URL,
        }
        missing = [key for key, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError("Missing required production configuration: " + ", ".join(missing))
        return self

    @property
    def environment(self) -> str:
        return self.ENVIRONMENT


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide cached settings object."""
    return Settings()


# Backward-compatible import for older modules. New code should use get_settings().
settings = get_settings()

# Backwards-compatible instance for modules that import `settings` directly.
settings = get_settings()
