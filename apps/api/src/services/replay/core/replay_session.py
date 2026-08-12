from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from .replay_cursor import ReplayCursor
from .replay_event import ReplayEvent


class ReplayState(str, Enum):

    STOPPED = "STOPPED"

    PLAYING = "PLAYING"

    PAUSED = "PAUSED"

    COMPLETED = "COMPLETED"


class ReplaySession:

    """
    Represents one replay session.
    """

    def __init__(self):

        self.session_id = str(uuid4())

        self.cursor = ReplayCursor()

        self.state = ReplayState.STOPPED

        self.created_at = datetime.utcnow()

        self.started_at: Optional[datetime] = None

        self.finished_at: Optional[datetime] = None

        self.speed: float = 1.0

        self.bookmarks: List[int] = []

        self.filters: Dict = {}

    # -------------------------------------------------

    def load(

        self,

        events: List[ReplayEvent]

    ):

        self.cursor.load_events(events)

        self.state = ReplayState.STOPPED

    # -------------------------------------------------

    def play(self):

        self.started_at = datetime.utcnow()

        self.state = ReplayState.PLAYING

    # -------------------------------------------------

    def pause(self):

        self.state = ReplayState.PAUSED

    # -------------------------------------------------

    def resume(self):

        self.state = ReplayState.PLAYING

    # -------------------------------------------------

    def stop(self):

        self.state = ReplayState.STOPPED

        self.cursor.reset()

    # -------------------------------------------------

    def complete(self):

        self.finished_at = datetime.utcnow()

        self.state = ReplayState.COMPLETED

    # -------------------------------------------------

    def next(self):

        event = self.cursor.next()

        if event is None:

            self.complete()

        return event

    # -------------------------------------------------

    def previous(self):

        return self.cursor.previous()

    # -------------------------------------------------

    def current(self):

        return self.cursor.current()

    # -------------------------------------------------

    def jump_to_block(

        self,

        block: int

    ):

        return self.cursor.jump_to_block(block)

    # -------------------------------------------------

    def jump_to_slot(

        self,

        slot: int

    ):

        return self.cursor.jump_to_slot(slot)

    # -------------------------------------------------

    def jump_to_time(

        self,

        timestamp: datetime

    ):

        return self.cursor.jump_to_timestamp(timestamp)

    # -------------------------------------------------

    def seek(

        self,

        percent: float

    ):

        return self.cursor.seek(percent)

    # -------------------------------------------------

    def set_speed(

        self,

        speed: float

    ):

        if speed <= 0:

            raise ValueError(

                "Playback speed must be greater than zero."

            )

        self.speed = speed

    # -------------------------------------------------

    def bookmark(self):

        self.bookmarks.append(

            self.cursor.index

        )

    # -------------------------------------------------

    def goto_bookmark(

        self,

        bookmark_index: int

    ):

        if bookmark_index >= len(self.bookmarks):

            return None

        return self.cursor.jump_to_index(

            self.bookmarks[bookmark_index]

        )

    # -------------------------------------------------

    def clear_bookmarks(self):

        self.bookmarks.clear()

    # -------------------------------------------------

    def set_filter(

        self,

        key: str,

        value

    ):

        self.filters[key] = value

    # -------------------------------------------------

    def clear_filters(self):

        self.filters.clear()

    # -------------------------------------------------

    def status(self):

        return {

            "session_id": self.session_id,

            "state": self.state.value,

            "speed": self.speed,

            "progress":

                self.cursor.progress(),

            "current_event":

                self.current(),

            "bookmarks":

                len(self.bookmarks),

            "remaining":

                self.cursor.remaining()

        }