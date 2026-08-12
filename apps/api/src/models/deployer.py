from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from database.base import Base


class Deployer(Base):
    __tablename__ = "deployers"

    id = Column(Integer, primary_key=True)

    wallet_address = Column(
        String,
        unique=True
    )

    total_tokens = Column(Integer, default=0)

    successful_tokens = Column(
        Integer,
        default=0
    )

    rugged_tokens = Column(
        Integer,
        default=0
    )

    best_market_cap = Column(
        Float,
        default=0
    )

    trust_score = Column(
        Float,
        default=0
    )