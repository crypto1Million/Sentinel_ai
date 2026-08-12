from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict
from uuid import uuid4


class ReplayEventType(str, Enum):

    TOKEN_CREATED = "TOKEN_CREATED"

    TOKEN_UPDATED = "TOKEN_UPDATED"

    PRICE_UPDATE = "PRICE_UPDATE"

    MARKET_CAP_UPDATE = "MARKET_CAP_UPDATE"

    LIQUIDITY_ADDED = "LIQUIDITY_ADDED"

    LIQUIDITY_REMOVED = "LIQUIDITY_REMOVED"

    HOLDER_UPDATE = "HOLDER_UPDATE"

    HOLDER_CHURN = "HOLDER_CHURN"

    SMART_MONEY_BUY = "SMART_MONEY_BUY"

    SMART_MONEY_SELL = "SMART_MONEY_SELL"

    WHALE_BUY = "WHALE_BUY"

    WHALE_SELL = "WHALE_SELL"

    FRESH_WALLET_BUY = "FRESH_WALLET_BUY"

    DEPLOYER_BUY = "DEPLOYER_BUY"

    DEPLOYER_SELL = "DEPLOYER_SELL"

    TOP10_CHANGED = "TOP10_CHANGED"

    TOP25_CHANGED = "TOP25_CHANGED"

    SNIPER_UPDATE = "SNIPER_UPDATE"

    INSIDER_UPDATE = "INSIDER_UPDATE"

    BUNDLE_DETECTED = "BUNDLE_DETECTED"

    JITO_BUNDLE = "JITO_BUNDLE"

    SANDWICH_ATTACK = "SANDWICH_ATTACK"

    ARBITRAGE = "ARBITRAGE"

    FRONT_RUN = "FRONT_RUN"

    MEV_ACTIVITY = "MEV_ACTIVITY"

    NARRATIVE_CHANGED = "NARRATIVE_CHANGED"

    SENTINEL_SCORE = "SENTINEL_SCORE"

    OPPORTUNITY_SCORE = "OPPORTUNITY_SCORE"

    RUG_SCORE = "RUG_SCORE"

    AI_VERDICT = "AI_VERDICT"

    ALERT = "ALERT"

    TRADE_EXECUTED = "TRADE_EXECUTED"

    CUSTOM = "CUSTOM"


@dataclass(slots=True)
class ReplayEvent:

    event_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    event_type: ReplayEventType = ReplayEventType.CUSTOM

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    slot: int = 0

    block: int = 0

    token: str = ""

    wallet: str = ""

    signature: str = ""

    source: str = ""

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:

        return {

            "event_id": self.event_id,

            "event_type": self.event_type.value,

            "timestamp": self.timestamp.isoformat(),

            "slot": self.slot,

            "block": self.block,

            "token": self.token,

            "wallet": self.wallet,

            "signature": self.signature,

            "source": self.source,

            "payload": self.payload,

            "metadata": self.metadata,

        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):

        return cls(

            event_id=data["event_id"],

            event_type=ReplayEventType(
                data["event_type"]
            ),

            timestamp=datetime.fromisoformat(
                data["timestamp"]
            ),

            slot=data.get("slot", 0),

            block=data.get("block", 0),

            token=data.get("token", ""),

            wallet=data.get("wallet", ""),

            signature=data.get(
                "signature",
                ""
            ),

            source=data.get(
                "source",
                ""
            ),

            payload=data.get(
                "payload",
                {}
            ),

            metadata=data.get(
                "metadata",
                {}
            ),
        )

    def add_metadata(
        self,
        key: str,
        value: Any
    ):

        self.metadata[key] = value

    def update_payload(
        self,
        key: str,
        value: Any
    ):

        self.payload[key] = value

    def is_market_event(self):

        return self.event_type in {

            ReplayEventType.PRICE_UPDATE,

            ReplayEventType.MARKET_CAP_UPDATE,

            ReplayEventType.LIQUIDITY_ADDED,

            ReplayEventType.LIQUIDITY_REMOVED,

        }

    def is_wallet_event(self):

        return self.event_type in {

            ReplayEventType.WHALE_BUY,

            ReplayEventType.WHALE_SELL,

            ReplayEventType.SMART_MONEY_BUY,

            ReplayEventType.SMART_MONEY_SELL,

            ReplayEventType.FRESH_WALLET_BUY,

            ReplayEventType.DEPLOYER_BUY,

            ReplayEventType.DEPLOYER_SELL,

        }

    def is_mev_event(self):

        return self.event_type in {

            ReplayEventType.BUNDLE_DETECTED,

            ReplayEventType.JITO_BUNDLE,

            ReplayEventType.SANDWICH_ATTACK,

            ReplayEventType.ARBITRAGE,

            ReplayEventType.FRONT_RUN,

            ReplayEventType.MEV_ACTIVITY,

        }

    def is_score_event(self):

        return self.event_type in {

            ReplayEventType.SENTINEL_SCORE,

            ReplayEventType.OPPORTUNITY_SCORE,

            ReplayEventType.RUG_SCORE,

        }

    def is_alert(self):

        return self.event_type == ReplayEventType.ALERT