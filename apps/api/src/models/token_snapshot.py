from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime
)

from database.base import Base
from datetime import datetime


class TokenSnapshot(Base):
    __tablename__ = "token_snapshots"

    id = Column(Integer, primary_key=True)

    token_address = Column(
        String,
        index=True
    )

    market_cap = Column(
        Float,
        default=0
    )

    liquidity = Column(
        Float,
        default=0
    )

    volume_1m = Column(
        Float,
        default=0
    )

    volume_5m = Column(
        Float,
        default=0
    )

    volume_1h = Column(
        Float,
        default=0
    )

    holders = Column(
        Integer,
        default=0
    )

    buy_count = Column(
        Integer,
        default=0
    )

    sell_count = Column(
        Integer,
        default=0
    )

    smart_money_percentage = Column(
        Float,
        default=0
    )

    whale_percentage = Column(
        Float,
        default=0
    )

    insider_percentage = Column(
        Float,
        default=0
    )

    fresh_wallet_percentage = Column(
        Float,
        default=0
    )

    bundled_percentage = Column(
        Float,
        default=0
    )

    sniper_percentage = Column(
        Float,
        default=0
    )

    lp_burned = Column(
        Boolean,
        default=False
    )

    lp_locked = Column(
        Boolean,
        default=False
    )

    snapshot_time = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )