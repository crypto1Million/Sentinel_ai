from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Numeric
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from models.base import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(
        BigInteger,
        primary_key=True
    )

    address = Column(
        Text,
        unique=True,
        nullable=False
    )

    wallet_type = Column(
        Text
    )

    win_rate = Column(
        Numeric,
        default=0
    )

    avg_roi = Column(
        Numeric,
        default=0
    )

    total_trades = Column(
        Integer,
        default=0
    )

    total_profit = Column(
        Numeric,
        default=0
    )

    first_seen = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    last_active = Column(
        TIMESTAMP
    )