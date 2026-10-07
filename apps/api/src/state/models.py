from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StateStatus(str, Enum):
    VERIFIED = "VERIFIED"
    DERIVED = "DERIVED"
    STALE = "STALE"
    CONFLICT = "CONFLICT"
    UNRESOLVED = "UNRESOLVED"
    UNAVAILABLE = "UNAVAILABLE"


class StateMeta(BaseModel):
    """
    Metadata attached to every canonical state object.

    This prevents SentinelAI from presenting a value without
    knowing where it came from or how fresh it is.
    """

    model_config = ConfigDict(extra="forbid")

    version: int = 1

    status: StateStatus = StateStatus.UNAVAILABLE

    source_id: str | None = None

    observed_at: datetime | None = None

    processed_at: datetime = Field(default_factory=utc_now)

    last_event_id: str | None = None

    parser: str | None = None

    parser_version: str | None = None

    age_ms: int | None = None


class TokenState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_type: str = "token"

    chain: str
    mint: str

    name: str | None = None
    symbol: str | None = None
    decimals: int | None = None

    price_usd: Decimal | None = None
    market_cap_usd: Decimal | None = None
    fdv_usd: Decimal | None = None

    total_supply: Decimal | None = None
    circulating_supply: Decimal | None = None

    holders: int | None = None

    liquidity_usd: Decimal | None = None

    volume_5m_usd: Decimal | None = None
    volume_1h_usd: Decimal | None = None
    volume_24h_usd: Decimal | None = None

    buy_volume_5m_usd: Decimal | None = None
    sell_volume_5m_usd: Decimal | None = None

    transaction_count_5m: int | None = None

    launchpad_id: str | None = None
    launchpad_name: str | None = None

    launchpad_rail: str | None = None

    launchpad_attribution_status: str = "UNRESOLVED"

    primary_pool_id: str | None = None
    pool_ids: list[str] = Field(default_factory=list)

    metadata_uri: str | None = None

    logo_uri: str | None = None

    creator_address: str | None = None

    mint_authority: str | None = None
    freeze_authority: str | None = None

    meta: StateMeta = Field(default_factory=StateMeta)


class PoolState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_type: str = "pool"

    chain: str
    pool_id: str

    dex_id: str

    base_token: str
    quote_token: str

    base_reserve: Decimal | None = None
    quote_reserve: Decimal | None = None

    price_usd: Decimal | None = None

    liquidity_usd: Decimal | None = None

    volume_5m_usd: Decimal | None = None
    volume_1h_usd: Decimal | None = None
    volume_24h_usd: Decimal | None = None

    buy_volume_5m_usd: Decimal | None = None
    sell_volume_5m_usd: Decimal | None = None

    fee_bps: int | None = None

    lp_supply: Decimal | None = None

    created_at: datetime | None = None

    last_swap_at: datetime | None = None

    last_liquidity_change_at: datetime | None = None

    meta: StateMeta = Field(default_factory=StateMeta)


class WalletState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_type: str = "wallet"

    chain: str
    address: str

    native_balance: Decimal | None = None

    token_count: int | None = None
    transaction_count: int | None = None

    total_volume_usd: Decimal | None = None

    realized_pnl_usd: Decimal | None = None
    unrealized_pnl_usd: Decimal | None = None

    win_rate: Decimal | None = None

    average_hold_seconds: int | None = None

    classification: str | None = None

    smart_money: bool = False
    sniper: bool = False
    insider: bool = False
    fresh_wallet: bool = False

    first_seen_at: datetime | None = None
    last_activity_at: datetime | None = None

    preferred_launchpads: list[str] = Field(
        default_factory=list
    )

    preferred_tokens: list[str] = Field(
        default_factory=list
    )

    meta: StateMeta = Field(default_factory=StateMeta)


class DeveloperState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_type: str = "developer"

    chain: str
    address: str

    first_seen_at: datetime | None = None
    last_activity_at: datetime | None = None

    tokens_created: int = 0

    successful_tokens: int = 0
    failed_tokens: int = 0

    rugged_tokens: int = 0

    total_deployed_liquidity_usd: Decimal = Decimal("0")

    average_initial_liquidity_usd: Decimal | None = None

    historical_volume_usd: Decimal = Decimal("0")

    wallet_addresses: list[str] = Field(
        default_factory=list
    )

    associated_launchpads: list[str] = Field(
        default_factory=list
    )

    risk_flags: list[str] = Field(
        default_factory=list
    )

    meta: StateMeta = Field(default_factory=StateMeta)


class LaunchpadState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_type: str = "launchpad"

    chain: str
    launchpad_id: str

    name: str

    detection_mode: str

    attribution_mode: str

    rail_id: str | None = None

    program_ids: list[str] = Field(
        default_factory=list
    )

    factory_addresses: list[str] = Field(
        default_factory=list
    )

    config_addresses: list[str] = Field(
        default_factory=list
    )

    created_token_count: int = 0

    volume_24h_usd: Decimal | None = None

    active: bool = True

    last_activity_at: datetime | None = None

    metadata_source: str | None = None

    meta: StateMeta = Field(default_factory=StateMeta)