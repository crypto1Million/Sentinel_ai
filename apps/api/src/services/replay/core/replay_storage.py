from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from .replay_event import ReplayEvent


class ReplayStorage:
    """
    Production-ready storage abstraction.

    Supports:

    • PostgreSQL
    • JSON archives
    • Redis Streams (future)
    • Kafka (future)
    """

    def __init__(

        self,

        db: Optional[Session] = None,

        archive_directory: str = "replays"

    ):

        self.db = db

        self.archive_directory = Path(
            archive_directory
        )

        self.archive_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # -------------------------------------------------

    # JSON STORAGE

    # -------------------------------------------------

    def save_events(

        self,

        replay_id: str,

        events: List[ReplayEvent]

    ) -> Path:

        file = self.archive_directory / f"{replay_id}.json"

        with open(file, "w") as f:

            json.dump(

                [

                    event.to_dict()

                    for event in events

                ],

                f,

                indent=4

            )

        return file

    # -------------------------------------------------

    def load_events(

        self,

        replay_id: str

    ) -> List[ReplayEvent]:

        file = self.archive_directory / f"{replay_id}.json"

        if not file.exists():

            return []

        with open(file) as f:

            raw = json.load(f)

        return [

            ReplayEvent.from_dict(x)

            for x in raw

        ]

    # -------------------------------------------------

    def delete_archive(

        self,

        replay_id: str

    ) -> bool:

        file = self.archive_directory / f"{replay_id}.json"

        if not file.exists():

            return False

        file.unlink()

        return True

    # -------------------------------------------------

    def archive_exists(

        self,

        replay_id: str

    ) -> bool:

        return (

            self.archive_directory

            / f"{replay_id}.json"

        ).exists()

    # -------------------------------------------------

    # DATABASE

    # -------------------------------------------------

    def save_to_database(

        self,

        events: List[ReplayEvent]

    ):

        """
        Save replay events into PostgreSQL.

        Replace with ReplayEventModel later.
        """

        if self.db is None:

            return

        for event in events:

            self.db.add(event)

        self.db.commit()

    # -------------------------------------------------

    def load_from_database(

        self,

        token: str = "",

        wallet: str = "",

        start_slot: int = 0,

        end_slot: int = 0

    ) -> List[ReplayEvent]:

        """
        Replace with SQLAlchemy queries.
        """

        return []

    # -------------------------------------------------

    # SEARCH

    # -------------------------------------------------

    def filter_by_token(

        self,

        events: List[ReplayEvent],

        token: str

    ):

        return [

            event

            for event in events

            if event.token == token

        ]

    # -------------------------------------------------

    def filter_by_wallet(

        self,

        events: List[ReplayEvent],

        wallet: str

    ):

        return [

            event

            for event in events

            if event.wallet == wallet

        ]

    # -------------------------------------------------

    def filter_by_slot(

        self,

        events: List[ReplayEvent],

        start_slot: int,

        end_slot: int

    ):

        return [

            event

            for event in events

            if

            start_slot

            <= event.slot

            <= end_slot

        ]

    # -------------------------------------------------

    def statistics(

        self,

        events: List[ReplayEvent]

    ) -> Dict:

        if not events:

            return {}

        return {

            "events":

                len(events),

            "first_slot":

                events[0].slot,

            "last_slot":

                events[-1].slot,

            "first_timestamp":

                events[0].timestamp,

            "last_timestamp":

                events[-1].timestamp,

            "tokens":

                len(

                    set(

                        e.token

                        for e in events

                    )

                ),

            "wallets":

                len(

                    set(

                        e.wallet

                        for e in events

                    )

                )

        }

    # -------------------------------------------------

    def export(

        self,

        replay_id: str,

        output_path: str

    ):

        events = self.load_events(
            replay_id
        )

        with open(output_path, "w") as f:

            json.dump(

                [

                    x.to_dict()

                    for x in events

                ],

                f,

                indent=4

            )