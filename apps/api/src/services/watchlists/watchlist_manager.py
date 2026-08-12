from typing import Dict, List
from datetime import datetime


class WatchlistManager:

    def __init__(self):

        self.watchlists = {}

    def create_watchlist(
        self,
        user_id: str,
        name: str
    ) -> Dict:

        watchlist_id = (
            f"{user_id}_{name}"
        )

        self.watchlists[
            watchlist_id
        ] = {

            "id": watchlist_id,

            "user_id": user_id,

            "name": name,

            "tokens": [],

            "created_at":
            datetime.utcnow()
        }

        return self.watchlists[
            watchlist_id
        ]

    def add_token(
        self,
        watchlist_id: str,
        token: str
    ) -> bool:

        if watchlist_id not in self.watchlists:

            return False

        if token not in self.watchlists[
            watchlist_id
        ]["tokens"]:

            self.watchlists[
                watchlist_id
            ]["tokens"].append(
                token
            )

        return True

    def remove_token(
        self,
        watchlist_id: str,
        token: str
    ) -> bool:

        if watchlist_id not in self.watchlists:

            return False

        if token in self.watchlists[
            watchlist_id
        ]["tokens"]:

            self.watchlists[
                watchlist_id
            ]["tokens"].remove(
                token
            )

        return True

    def get_watchlist(
        self,
        watchlist_id: str
    ):

        return self.watchlists.get(
            watchlist_id
        )

    def get_all(
        self,
        user_id: str
    ):

        return [

            watchlist

            for watchlist in
            self.watchlists.values()

            if watchlist["user_id"]
            == user_id

        ]