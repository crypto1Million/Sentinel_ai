from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from database.base import Base


class Holder(Base):
    __tablename__ = "holders"

    id = Column(Integer, primary_key=True)

    token_address = Column(String, index=True)

    wallet_address = Column(String)

    balance = Column(Float)

    ownership_percentage = Column(Float)

    wallet_type = Column(String)