from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Numeric
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

from models.base import Base
from database.base import Base
from datetime import datetime


class Narrative(Base):

    __tablename__ = "narratives"

    id = Column(
        BigInteger,
        primary_key=True
    )

    narrative_name = Column(
        Text
    )

    category = Column(
        Text
    )

    sentiment_score = Column(
        Numeric,
        default=0
    )

    momentum_score = Column(
        Numeric,
        default=0
    )

    token_count = Column(
        Integer,
        default=0
    )

    volume = Column(
        Numeric,
        default=0
    )

    tracked_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )