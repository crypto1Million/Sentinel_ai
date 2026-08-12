from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from models.base import Base
from database.base import Base
from datetime import datetime


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)

    address = Column(String, unique=True, index=True)

    symbol = Column(String)
    name = Column(String)

    chain = Column(String, default="solana")

    market_cap = Column(Float, default=0)
    liquidity = Column(Float, default=0)
    volume_24h = Column(Float, default=0)

    holders = Column(Integer, default=0)

    mint_authority = Column(Boolean, default=False)
    freeze_authority = Column(Boolean, default=False)

    lp_burned = Column(Boolean, default=False)
    lp_locked = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    scores = relationship("Score", back_populates="token")