from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from database.base import Base


class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True)

    cluster_id = Column(String, index=True)

    cluster_type = Column(String)

    wallet_count = Column(Integer)

    total_holdings = Column(Float)

    confidence = Column(Float)

    risk_score = Column(Float)