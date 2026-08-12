from __future__ import annotations

from typing import List, Optional

from .replay_event import ReplayEvent
from .replay_session import ReplaySession
from .replay_storage import ReplayStorage


class ReplayEngine:
    """
    Core replay engine.

    Responsible for:

    • Loading events
    • Managing replay sessions
    • Playback
    • Seeking
    • Exporting
    """

    def __init__(
        self,
        storage: ReplayStorage
    ):

        self.storage = storage

        self.session = ReplaySession()

    # --------------------------------------------------

    def load_events(
        self,
        events: List[ReplayEvent]
    ):

        self.session.load(events)

    # --------------------------------------------------

    def load_archive(
        self,
        replay_id: str
    ):

        events = self.storage.load_events(
            replay_id
        )

        self.load_events(events)

    # --------------------------------------------------

    def play(self):

        self.session.play()

    # --------------------------------------------------

    def pause(self):

        self.session.pause()

    # --------------------------------------------------

    def resume(self):

        self.session.resume()

    # --------------------------------------------------

    def stop(self):

        self.session.stop()

    # --------------------------------------------------

    def next_event(
        self
    ) -> Optional[ReplayEvent]:

        return self.session.next()

    # --------------------------------------------------

    def previous_event(
        self
    ) -> Optional[ReplayEvent]:

        return self.session.previous()

    # --------------------------------------------------

    def current_event(
        self
    ) -> Optional[ReplayEvent]:

        return self.session.current()

    # --------------------------------------------------

    def jump_to_slot(
        self,
        slot: int
    ):

        return self.session.jump_to_slot(
            slot
        )

    # --------------------------------------------------

    def jump_to_block(
        self,
        block: int
    ):

        return self.session.jump_to_block(
            block
        )

    # --------------------------------------------------

    def jump_to_time(
        self,
        timestamp
    ):

        return self.session.jump_to_time(
            timestamp
        )

    # --------------------------------------------------

    def seek(
        self,
        percentage: float
    ):

        return self.session.seek(
            percentage
        )

    # --------------------------------------------------

    def set_speed(
        self,
        speed: float
    ):

        self.session.set_speed(speed)

    # --------------------------------------------------

    def bookmark(self):

        self.session.bookmark()

    # --------------------------------------------------

    def goto_bookmark(
        self,
        index: int
    ):

        return self.session.goto_bookmark(
            index
        )

    # --------------------------------------------------

    def export(
        self,
        replay_id: str,
        output_file: str
    ):

        self.storage.export(

            replay_id,

            output_file

        )

    # --------------------------------------------------

    def statistics(self):

        return self.storage.statistics(

            self.session.cursor.events

        )

    # --------------------------------------------------

    def state(self):

        return self.session.status()