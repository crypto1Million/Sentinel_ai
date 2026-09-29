from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CanonicalEventModel(BaseModel):
    """
    Base class for normalized SentinelAI event payloads.

    Provider-specific fields should be converted into one of these
    canonical structures before entering the event bus.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )


# ============================================================
# TOKEN EVENTS
# ============================================================


class TokenCreatedEvent(CanonicalEventModel):
    chain: str
    token_address: str

    name: str | None = None
    symbol: str | None = None

    decimals: int | None = Field(
        default=None,
        ge=0,
        le=255,
    )

    creator_address: str | None = None

    metadata_uri: str | None = None
    image_uri: str | None = None

    created_at: str | None = None

    launchpad_id: str | None = None
    launchpad_status: str = "unresolved"

    launchpad_evidence: list[str] = Field(
        default_factory=list
    )


class TokenMetadataUpdatedEvent(CanonicalEventModel):
    chain: str
    token_address: str

    changed_fields: list[str] = Field(
        default_factory=list
    )

    name: str | None = None
    symbol: str | None = None

    decimals: int | None = Field(
        default=None,
        ge=0,
        le=255,
    )

    metadata_uri: str | None = None
    image_uri: str | None = None

    metadata_source: str | None = None


# ============================================================
# POOL / LIQUIDITY EVENTS
# ============================================================


class PoolCreatedEvent(CanonicalEventModel):
    chain: str

    pool_address: str

    token0: str
    token1: str

    dex_id: str | None = None
    launchpad_id: str | None = None

    creator_address: str | None = None

    initial_liquidity_usd: Decimal | None = None


class LiquidityChangedEvent(CanonicalEventModel):
    chain: str

    pool_address: str
    token_address: str | None = None

    previous_liquidity_usd: Decimal | None = None
    liquidity_usd: Decimal | None = None

    delta_usd: Decimal | None = None

    direction: str
    """
    add
    remove
    rebalance
    unknown
    """

    source: str | None = None


# ============================================================
# SWAP EVENTS
# ============================================================


class SwapEvent(CanonicalEventModel):
    chain: str

    transaction_id: str

    pool_address: str | None = None

    trader_address: str

    token_in: str
    token_out: str

    amount_in: Decimal
    amount_out: Decimal

    amount_in_usd: Decimal | None = None
    amount_out_usd: Decimal | None = None

    price_usd: Decimal | None = None

    side: str
    """
    buy
    sell
    unknown
    """

    dex_id: str | None = None

    is_mev_suspected: bool = False


# ============================================================
# TRANSFER EVENTS
# ============================================================


class TransferEvent(CanonicalEventModel):
    chain: str

    transaction_id: str

    token_address: str

    from_address: str
    to_address: str

    amount: Decimal

    amount_usd: Decimal | None = None

    token_standard: str
    """
    spl
    spl-token-2022
    erc20
    native
    other
    """

    from_balance_after: Decimal | None = None
    to_balance_after: Decimal | None = None


# ============================================================
# WALLET EVENTS
# ============================================================


class WalletFundedEvent(CanonicalEventModel):
    chain: str

    wallet_address: str

    funder_address: str

    asset: str
    amount: Decimal

    amount_usd: Decimal | None = None

    funding_method: str | None = None


class WalletInteractionEvent(CanonicalEventModel):
    chain: str

    wallet_address: str

    interaction_type: str
    """
    swap
    transfer
    liquidity_add
    liquidity_remove
    deploy
    approval
    bridge
    launchpad
    other
    """

    target_address: str | None = None
    token_address: str | None = None
    pool_address: str | None = None

    amount_usd: Decimal | None = None

    success: bool = True


# ============================================================
# AUTHORITY / RISK EVENTS
# ============================================================


class TokenAuthorityChangedEvent(CanonicalEventModel):
    chain: str

    token_address: str

    authority_type: str
    """
    mint
    freeze
    owner
    upgrade
    admin
    """

    previous_authority: str | None = None
    new_authority: str | None = None

    revoked: bool | None = None


class HolderDistributionChangedEvent(CanonicalEventModel):
    chain: str

    token_address: str

    holder_count: int | None = Field(
        default=None,
        ge=0,
    )

    top10_percent: Decimal | None = None
    top25_percent: Decimal | None = None
    top50_percent: Decimal | None = None

    largest_holder_percent: Decimal | None = None


# ============================================================
# LAUNCHPAD EVENTS
# ============================================================


class LaunchpadAttributionEvent(CanonicalEventModel):
    chain: str

    token_address: str

    rail_id: str | None = None

    launchpad_id: str | None = None

    attribution_status: str
    """
    verified
    unresolved
    conflict
    unavailable
    """

    attribution_method: str
    """
    exact_program
    exact_factory
    config_account
    event_signature
    authoritative_partner_mapping
    none
    """

    evidence_event_ids: list[str] = Field(
        default_factory=list
    )

    evidence_values: dict[str, Any] = Field(
        default_factory=dict
    )

    reason: str | None = None


# ============================================================
# MARKET SNAPSHOT EVENTS
# ============================================================


class MarketSnapshotEvent(CanonicalEventModel):
    chain: str

    token_address: str

    price_usd: Decimal | None = None

    market_cap_usd: Decimal | None = None
    fdv_usd: Decimal | None = None

    liquidity_usd: Decimal | None = None

    volume_5m_usd: Decimal | None = None
    volume_1h_usd: Decimal | None = None
    volume_24h_usd: Decimal | None = None

    buys_5m: int | None = Field(
        default=None,
        ge=0,
    )

    sells_5m: int | None = Field(
        default=None,
        ge=0,
    )

    holders: int | None = Field(
        default=None,
        ge=0,
    )

    circulating_supply: Decimal | None = None

    data_source: str


# ============================================================
# SCORE EVENTS
# ============================================================


class ScoreUpdatedEvent(CanonicalEventModel):
    chain: str

    token_address: str

    score_name: str
    """
    sentinel
    dev
    wallet
    volume
    social
    narrative
    rug
    opportunity
    """

    score: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    previous_score: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    model_name: str | None = None
    model_version: str | None = None

    feature_version: str | None = None

    input_event_ids: list[str] = Field(
        default_factory=list
    )

    explanation: str | None = None


# ============================================================
# ALERT EVENTS
# ============================================================


class AlertTriggeredEvent(CanonicalEventModel):
    chain: str

    token_address: str | None = None
    wallet_address: str | None = None

    alert_type: str

    severity: str
    """
    info
    low
    medium
    high
    critical
    """

    title: str
    message: str

    trigger_event_ids: list[str] = Field(
        default_factory=list
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# REPLAY / SYSTEM EVENTS
# ============================================================


class ReconciliationEvent(CanonicalEventModel):
    chain: str

    entity_type: str
    entity_id: str

    reconciliation_status: str
    """
    matched
    repaired
    conflict
    failed
    """

    expected_state: dict[str, Any] = Field(
        default_factory=dict
    )

    observed_state: dict[str, Any] = Field(
        default_factory=dict
    )

    repaired_fields: list[str] = Field(
        default_factory=list
    )

    source_event_ids: list[str] = Field(
        default_factory=list
    )


class BackfillEvent(CanonicalEventModel):
    chain: str

    start_position: int
    end_position: int

    provider: str

    events_recovered: int = Field(
        default=0,
        ge=0,
    )

    events_deduplicated: int = Field(
        default=0,
        ge=0,
    )