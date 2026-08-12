from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from .core.replay_engine import ReplayEngine
from .core.replay_event import ReplayEvent


class BlockReplay:

    """
    Replays blockchain activity
    block-by-block.
    """

    def __init__(self, engine: ReplayEngine):

        self.engine = engine

    # ----------------------------------------------------

    def replay_block(
        self,
        block: int
    ) -> List[ReplayEvent]:

        events = self.engine.session.cursor.events

        return [

            event

            for event in events

            if event.block == block

        ]

    # ----------------------------------------------------

    def replay_slot(
        self,
        slot: int
    ) -> List[ReplayEvent]:

        events = self.engine.session.cursor.events

        return [

            event

            for event in events

            if event.slot == slot

        ]

    # ----------------------------------------------------

    def replay_range(
        self,
        start_block: int,
        end_block: int
    ) -> List[ReplayEvent]:

        events = self.engine.session.cursor.events

        return [

            event

            for event in events

            if start_block
            <= event.block
            <= end_block

        ]

    # ----------------------------------------------------

    def replay_transaction(
        self,
        signature: str
    ) -> Optional[ReplayEvent]:

        events = self.engine.session.cursor.events

        for event in events:

            if event.signature == signature:

                return event

        return None

    # ----------------------------------------------------

    def replay_swaps(
        self,
        block: int
    ) -> List[ReplayEvent]:

        swaps = []

        for event in self.replay_block(block):

            if event.event_type.value in {

                "TRADE_EXECUTED",

                "SMART_MONEY_BUY",

                "SMART_MONEY_SELL",

                "WHALE_BUY",

                "WHALE_SELL"

            }:

                swaps.append(event)

        return swaps

    # ----------------------------------------------------

    def replay_liquidity(
        self,
        block: int
    ) -> List[ReplayEvent]:

        liquidity = []

        for event in self.replay_block(block):

            if event.event_type.value in {

                "LIQUIDITY_ADDED",

                "LIQUIDITY_REMOVED"

            }:

                liquidity.append(event)

        return liquidity

    # ----------------------------------------------------

    def replay_bundles(
        self,
        block: int
    ) -> List[ReplayEvent]:

        bundles = []

        for event in self.replay_block(block):

            if event.event_type.value in {

                "BUNDLE_DETECTED",

                "JITO_BUNDLE"

            }:

                bundles.append(event)

        return bundles

    # ----------------------------------------------------

    def replay_holders(
        self,
        block: int
    ) -> List[ReplayEvent]:

        holders = []

        for event in self.replay_block(block):

            if event.event_type.value in {

                "HOLDER_UPDATE",

                "TOP10_CHANGED",

                "TOP25_CHANGED"

            }:

                holders.append(event)

        return holders

    # ----------------------------------------------------

    def statistics(
        self,
        block: int
    ) -> Dict:

        events = self.replay_block(block)

        grouped = defaultdict(int)

        for event in events:

            grouped[event.event_type.value] += 1

        return {

            "block": block,

            "events": len(events),

            "breakdown": dict(grouped)

        }