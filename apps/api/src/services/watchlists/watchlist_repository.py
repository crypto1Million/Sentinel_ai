from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from apps.api.src.models.watchlist import Watchlist
from apps.api.src.models.watchlist_item import WatchlistItem


class WatchlistRepository:

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------
    # WATCHLIST CRUD
    # ------------------------------------

    def create_watchlist(
        self,
        user_id: str,
        name: str,
        description: str = ""
    ) -> Watchlist:

        watchlist = Watchlist(

            id=str(uuid4()),

            user_id=user_id,

            name=name,

            description=description,

            created_at=datetime.utcnow()

        )

        self.db.add(watchlist)

        self.db.commit()

        self.db.refresh(watchlist)

        return watchlist

    def get_watchlist(
        self,
        watchlist_id: str
    ) -> Optional[Watchlist]:

        return (

            self.db.query(Watchlist)

            .filter(

                Watchlist.id == watchlist_id

            )

            .first()

        )

    def get_user_watchlists(
        self,
        user_id: str
    ) -> List[Watchlist]:

        return (

            self.db.query(Watchlist)

            .filter(

                Watchlist.user_id == user_id

            )

            .all()

        )

    def delete_watchlist(
        self,
        watchlist_id: str
    ) -> bool:

        watchlist = self.get_watchlist(

            watchlist_id

        )

        if not watchlist:

            return False

        self.db.delete(watchlist)

        self.db.commit()

        return True

    # ------------------------------------
    # TOKENS
    # ------------------------------------

    def add_token(

        self,

        watchlist_id: str,

        mint: str

    ) -> WatchlistItem:

        existing = (

            self.db.query(WatchlistItem)

            .filter(

                WatchlistItem.watchlist_id == watchlist_id,

                WatchlistItem.mint == mint

            )

            .first()

        )

        if existing:

            return existing

        item = WatchlistItem(

            id=str(uuid4()),

            watchlist_id=watchlist_id,

            mint=mint,

            created_at=datetime.utcnow()

        )

        self.db.add(item)

        self.db.commit()

        self.db.refresh(item)

        return item

    def remove_token(

        self,

        watchlist_id: str,

        mint: str

    ) -> bool:

        item = (

            self.db.query(WatchlistItem)

            .filter(

                WatchlistItem.watchlist_id == watchlist_id,

                WatchlistItem.mint == mint

            )

            .first()

        )

        if not item:

            return False

        self.db.delete(item)

        self.db.commit()

        return True

    def get_tokens(

        self,

        watchlist_id: str

    ) -> List[WatchlistItem]:

        return (

            self.db.query(

                WatchlistItem

            )

            .filter(

                WatchlistItem.watchlist_id == watchlist_id

            )

            .all()

        )

    # ------------------------------------
    # SEARCH
    # ------------------------------------

    def search(

        self,

        user_id: str,

        query: str

    ) -> List[Watchlist]:

        return (

            self.db.query(Watchlist)

            .filter(

                Watchlist.user_id == user_id,

                Watchlist.name.ilike(

                    f"%{query}%"

                )

            )

            .all()

        )

    # ------------------------------------
    # RENAME
    # ------------------------------------

    def rename(

        self,

        watchlist_id: str,

        new_name: str

    ) -> Optional[Watchlist]:

        watchlist = self.get_watchlist(

            watchlist_id

        )

        if not watchlist:

            return None

        watchlist.name = new_name

        self.db.commit()

        self.db.refresh(watchlist)

        return watchlist

    # ------------------------------------
    # UPDATE DESCRIPTION
    # ------------------------------------

    def update_description(

        self,

        watchlist_id: str,

        description: str

    ) -> Optional[Watchlist]:

        watchlist = self.get_watchlist(

            watchlist_id

        )

        if not watchlist:

            return None

        watchlist.description = description

        self.db.commit()

        self.db.refresh(watchlist)

        return watchlist