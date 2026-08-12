from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from database.base import Base
from datetime import datetime


class WalletRelationship(Base):
    __tablename__ = "wallet_relationships"

    id = Column(Integer, primary_key=True)

    wallet_a = Column(
        String,
        index=True
    )

    wallet_b = Column(
        String,
        index=True
    )

    relationship_type = Column(
        String
    )

    confidence = Column(
        Float,
        default=0
    )

    interaction_count = Column(
        Integer,
        default=0
    )

    shared_tokens = Column(
        Integer,
        default=0
    )

    shared_trades = Column(
        Integer,
        default=0
    )

    first_seen = Column(
        DateTime,
        default=datetime.utcnow
    )

    last_seen = Column(
        DateTime,
        default=datetime.utcnow
    )