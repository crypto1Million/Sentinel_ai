from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Numeric
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from models.base import Base
from database.base import Base
from datetime import datetime


class Trade(Base):

    __tablename__ = "trades"

    id = Column(
        BigInteger,
        primary_key=True
    )

    wallet_address = Column(
        Text
    )

    mint_address = Column(
        Text
    )

    side = Column(
        Text
    )

    quantity = Column(
        Numeric
    )

    price = Column(
        Numeric
    )

    market_cap = Column(
        Numeric
    )

    pnl = Column(
        Numeric,
        default=0
    )

    executed_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )