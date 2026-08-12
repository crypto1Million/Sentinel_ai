from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from apps.api.src.database.connection import Base


class WatchlistItem(Base):

    __tablename__ = "watchlist_items"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    watchlist_id = Column(
        String,
        ForeignKey("watchlists.id"),
        nullable=False,
        index=True
    )

    mint = Column(
        String,
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    watchlist = relationship(
        "Watchlist",
        back_populates="items"
    )

    def __repr__(self):

        return (
            f"<WatchlistItem("
            f"{self.mint}"
            f")>"
        )