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
    MODEL_DERIVED = "MODEL_DERIVED"
    STALE = "STALE"
    CONFLICT = "CONFLICT"
    UNRESOLVED = "UNRESOLVED"
    UNAVAILABLE = "UNAVAILABLE"


class ChainId(str, Enum):
    SOLANA = "solana"
    BASE = "base"
    ETHEREUM = "ethereum"
    BNB = "bnb"
    ROBINHOOD = "robinhood"


class Provenance(BaseModel):
    """
    Provenance for an individual state value.

    This prevents SentinelAI from presenting an untraceable
    value as fact.
    """

    model_config = ConfigDict(extra="forbid")

    source: str
    source_type: str
    observed_at: datetime = Field(default_factory=utc_now)

    event_id: str | None = None

    transaction_hash: str | None = None
    transaction_signature: str | None = None

    block_number: int | None = None
    slot: int | None = None

    block_hash: str | None = None

    parser: str | None = None
    parser_version: str | None = None

    status: StateStatus = StateStatus.VERIFIED

    evidence_ids: list[str] = Field(default_factory=list)


class ChainPosition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    block_number: int | None = None
    slot: int | None = None
    block_hash: str | None = None

    transaction_hash: str | None = None
    transaction_signature: str | None = None

    instruction_index: int | None = None
    log_index: int | None = None

    commitment: str | None = None


class StateMeta(BaseModel):
    """
    Metadata shared by every canonical state object.
    """

    model_config = ConfigDict(extra="forbid")

    entity_id: str
    chain: ChainId

    version: int = 1

    status: StateStatus = StateStatus.VERIFIED

    observed_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    last_event_id: str | None = None

    source: str | None = None
    source_type: str | None = None

    chain_position: ChainPosition | None = None

    provenance: dict[str, Provenance] = Field(
        default_factory=dict
    )

    conflicts: dict[str, list[Any]] = Field(
        default_factory=dict
    )


class TokenState(BaseModel):
    """
    Current canonical state of a token.

    All values are nullable when the blockchain/provider has
    not established them. Zero must only mean an observed zero.
    """

    model_config = ConfigDict(extra="forbid")

    meta: StateMeta

    mint: str

    name: str | None = None
    symbol: str | None = None

    decimals: int | None = None

    total_supply: Decimal | None = None
    circulating_supply: Decimal | None = None

    price_usd: Decimal | None = None
    market_cap_usd: Decimal | None = None
    fdv_usd: Decimal | None = None

    liquidity_usd: Decimal | None = None

    volume_1m_usd: Decimal | None = None
    volume_5m_usd: Decimal | None = None
    volume_15m_usd: Decimal | None = None
    volume_1h_usd: Decimal | None = None
    volume_24h_usd: Decimal | None = None

    buys_1m: int | None = None
    sells_1m: int | None = None

    buys_5m: int | None = None
    sells_5m: int | None = None

    holders: int | None = None

    creator: str | None = None
    deployer: str | None = None

    launchpad_id: str | None = None
    launchpad_rail: str | None = None
    launchpad_status: StateStatus = StateStatus.UNAVAILABLE

    metadata_uri: str | None = None
    logo_uri: str | None = None

    mint_authority: str | None = None
    freeze_authority: str | None = None

    lp_locked: bool | None = None
    lp_burned: bool | None = None


class PoolState(BaseModel):
    """
    Current canonical state of a liquidity pool.
    """

    model_config = ConfigDict(extra="forbid")

    meta: StateMeta

    pool_address: str

    token_a: str
    token_b: str

    dex: str | None = None

    pool_type: str | None = None

    reserve_a: Decimal | None = None
    reserve_b: Decimal | None = None

    liquidity_usd: Decimal | None = None

    price_token_a: Decimal | None = None
    price_token_b: Decimal | None = None

    volume_1m_usd: Decimal | None = None
    volume_5m_usd: Decimal | None = None
    volume_1h_usd: Decimal | None = None
    volume_24h_usd: Decimal | None = None

    buys_5m: int | None = None
    sells_5m: int | None = None

    lp_supply: Decimal | None = None
    lp_burned: bool | None = None
    lp_locked: bool | None = None

    created_at: datetime | None = None

    last_swap_at: datetime | None = None


class WalletState(BaseModel):
    """
    Current canonical state of a wallet.
    """

    model_config = ConfigDict(extra="forbid")

    meta: StateMeta

    address: str

    wallet_type: str | None = None

    native_balance: Decimal | None = None

    total_trades: int | None = None

    winning_trades: int | None = None
    losing_trades: int | None = None

    win_rate: Decimal | None = None
    avg_roi: Decimal | None = None

    realized_pnl_usd: Decimal | None = None
    unrealized_pnl_usd: Decimal | None = None
    total_pnl_usd: Decimal | None = None

    first_seen: datetime | None = None
    last_active: datetime | None = None

    preferred_chains: list[str] = Field(
        default_factory=list
    )

    preferred_launchpads: list[str] = Field(
        default_factory=list
    )

    preferred_dexes: list[str] = Field(
        default_factory=list
    )


class DeveloperState(BaseModel):
    """
    Current canonical state of a token developer/deployer.
    """

    model_config = ConfigDict(extra="forbid")

    meta: StateMeta

    address: str

    tokens_created: int | None = None
    successful_tokens: int | None = None
    failed_tokens: int | None = None

    rug_count: int | None = None

    average_initial_liquidity_usd: Decimal | None = None

    average_token_lifetime_hours: Decimal | None = None

    historical_profit_usd: Decimal | None = None

    known_launchpads: list[str] = Field(
        default_factory=list
    )

    known_wallets: list[str] = Field(
        default_factory=list
    )

    first_seen: datetime | None = None
    last_activity: datetime | None = None


class LaunchpadState(BaseModel):
    """
    Canonical state for a launchpad / launch rail.

    A shared rail and a specific brand are deliberately separate.
    """

    model_config = ConfigDict(extra="forbid")

    meta: StateMeta

    launchpad_id: str
    name: str

    rail: str

    protocol_family: str | None = None

    chain_programs: list[str] = Field(
        default_factory=list
    )

    factory_addresses: list[str] = Field(
        default_factory=list
    )

    config_addresses: list[str] = Field(
        default_factory=list
    )

    attribution_mode: str = "direct"

    attribution_status: StateStatus = StateStatus.UNAVAILABLE

    authoritative_metadata_source: str | None = None

    last_metadata_refresh: datetime | None = None