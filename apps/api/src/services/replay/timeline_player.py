from __future__ import annotations

import asyncio
from typing import Callable, List, Optional

from .core.replay_engine import ReplayEngine
from .core.replay_event import ReplayEvent


class TimelinePlayer:

    """
    Controls replay playback for the frontend.

    Supports:

    • Play
    • Pause
    • Stop
    • Next
    • Previous
    • Seek
    • Playback Speed
    • Event Subscribers
    """

    def __init__(self, engine: ReplayEngine):

        self.engine = engine

        self.playing = False

        self.speed = 1.0

        self.subscribers: List[
            Callable[[ReplayEvent], None]
        ] = []

    # --------------------------------------------------

    async def play(self):

        self.playing = True

        self.engine.play()

        while self.playing:

            event = self.engine.next_event()

            if event is None:

                self.stop()

                break

            self.notify(event)

            await asyncio.sleep(

                1 / self.speed

            )

    # --------------------------------------------------

    def pause(self):

        self.playing = False

        self.engine.pause()

    # --------------------------------------------------

    def resume(self):

        if self.playing:

            return

        self.playing = True

        self.engine.resume()

    # --------------------------------------------------

    def stop(self):

        self.playing = False

        self.engine.stop()

    # --------------------------------------------------

    def next(self):

        event = self.engine.next_event()

        if event:

            self.notify(event)

        return event

    # --------------------------------------------------

    def previous(self):

        event = self.engine.previous_event()

        if event:

            self.notify(event)

        return event

    # --------------------------------------------------

    def seek(

        self,

        percentage: float

    ):

        event = self.engine.seek(

            percentage

        )

        if event:

            self.notify(event)

        return event

    # --------------------------------------------------

    def jump_to_slot(

        self,

        slot: int

    ):

        event = self.engine.jump_to_slot(

            slot

        )

        if event:

            self.notify(event)

        return event

    # --------------------------------------------------

    def jump_to_block(

        self,

        block: int

    ):

        event = self.engine.jump_to_block(

            block

        )

        if event:

            self.notify(event)

        return event

    # --------------------------------------------------

    def set_speed(

        self,

        speed: float

    ):

        self.speed = max(

            0.1,

            speed

        )

        self.engine.set_speed(

            self.speed

        )

    # --------------------------------------------------

    def subscribe(

        self,

        callback: Callable[[ReplayEvent], None]

    ):

        self.subscribers.append(

            callback

        )

    # --------------------------------------------------

    def unsubscribe(

        self,

        callback

    ):

        if callback in self.subscribers:

            self.subscribers.remove(

                callback

            )

    # --------------------------------------------------

    def notify(

        self,

        event: ReplayEvent

    ):

        for subscriber in self.subscribers:

            subscriber(event)

    # --------------------------------------------------

    def status(self):

        return {

            "playing": self.playing,

            "speed": self.speed,

            "engine": self.engine.state()

        }