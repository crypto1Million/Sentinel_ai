from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from database.base import Base
from datetime import datetime


class WalletSnapshot(Base):
    __tablename__ = "wallet_snapshots"

    id = Column(Integer, primary_key=True)

    wallet_address = Column(
        String,
        index=True
    )

    total_value_usd = Column(
        Float,
        default=0
    )

    realized_pnl = Column(
        Float,
        default=0
    )

    unrealized_pnl = Column(
        Float,
        default=0
    )

    win_rate = Column(
        Float,
        default=0
    )

    token_count = Column(
        Integer,
        default=0
    )

    smart_money_score = Column(
        Float,
        default=0
    )

    whale_score = Column(
        Float,
        default=0
    )

    conviction_score = Column(
        Float,
        default=0
    )

    snapshot_time = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )