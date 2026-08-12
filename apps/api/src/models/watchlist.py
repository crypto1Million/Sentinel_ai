from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from apps.api.src.database.connection import Base


class Watchlist(Base):

    __tablename__ = "watchlists"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    user_id = Column(
        String,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    items = relationship(
        "WatchlistItem",
        back_populates="watchlist",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<Watchlist("
            f"{self.name}"
            f")>"
        )