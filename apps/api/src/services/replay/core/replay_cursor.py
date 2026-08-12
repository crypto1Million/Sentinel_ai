from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .replay_event import ReplayEvent


class ReplayCursor:

    """
    Controls navigation through replay events.

    Supports:

    • Next event
    • Previous event
    • Jump to block
    • Jump to slot
    • Jump to timestamp
    • Seek
    """

    def __init__(self):

        self.events: List[ReplayEvent] = []

        self.index: int = 0

    # ---------------------------------------------

    def load_events(

        self,

        events: List[ReplayEvent]

    ):

        self.events = sorted(

            events,

            key=lambda x: (

                x.slot,

                x.timestamp

            )

        )

        self.index = 0

    # ---------------------------------------------

    def current(self) -> Optional[ReplayEvent]:

        if not self.events:

            return None

        return self.events[self.index]

    # ---------------------------------------------

    def next(self) -> Optional[ReplayEvent]:

        if self.index >= len(self.events) - 1:

            return None

        self.index += 1

        return self.current()

    # ---------------------------------------------

    def previous(self) -> Optional[ReplayEvent]:

        if self.index == 0:

            return None

        self.index -= 1

        return self.current()

    # ---------------------------------------------

    def reset(self):

        self.index = 0

    # ---------------------------------------------

    def jump_to_index(

        self,

        index: int

    ) -> Optional[ReplayEvent]:

        if index < 0:

            return None

        if index >= len(self.events):

            return None

        self.index = index

        return self.current()

    # ---------------------------------------------

    def jump_to_slot(

        self,

        slot: int

    ) -> Optional[ReplayEvent]:

        for i, event in enumerate(self.events):

            if event.slot >= slot:

                self.index = i

                return event

        return None

    # ---------------------------------------------

    def jump_to_block(

        self,

        block: int

    ) -> Optional[ReplayEvent]:

        for i, event in enumerate(self.events):

            if event.block >= block:

                self.index = i

                return event

        return None

    # ---------------------------------------------

    def jump_to_timestamp(

        self,

        timestamp: datetime

    ) -> Optional[ReplayEvent]:

        for i, event in enumerate(self.events):

            if event.timestamp >= timestamp:

                self.index = i

                return event

        return None

    # ---------------------------------------------

    def seek(

        self,

        percentage: float

    ) -> Optional[ReplayEvent]:

        if not self.events:

            return None

        percentage = max(

            0,

            min(

                percentage,

                100

            )

        )

        position = int(

            (

                percentage / 100

            )

            *

            (

                len(self.events) - 1

            )

        )

        self.index = position

        return self.current()

    # ---------------------------------------------

    def remaining(self) -> int:

        return max(

            0,

            len(self.events)

            - self.index

            - 1

        )

    # ---------------------------------------------

    def progress(self) -> float:

        if not self.events:

            return 0

        return round(

            (

                self.index

                /

                (

                    len(self.events)

                    - 1

                )

            )

            * 100,

            2

        )

    # ---------------------------------------------

    def has_next(self):

        return self.index < len(self.events) - 1

    # ---------------------------------------------

    def has_previous(self):

        return self.index > 0

    # ---------------------------------------------

    def size(self):

        return len(self.events)