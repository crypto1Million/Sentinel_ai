from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from models.base import Base


class Score(Base):

    __tablename__ = "scores"

    id = Column(
        BigInteger,
        primary_key=True
    )

    mint_address = Column(
        Text,
        unique=True
    )

    sentinel_score = Column(
        Numeric
    )

    dev_quality = Column(
        Numeric
    )

    wallet_quality = Column(
        Numeric
    )

    volume_quality = Column(
        Numeric
    )

    social_strength = Column(
        Numeric
    )

    narrative_momentum = Column(
        Numeric
    )

    rug_risk = Column(
        Numeric
    )

    opportunity_score = Column(
        Numeric
    )

    calculated_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )