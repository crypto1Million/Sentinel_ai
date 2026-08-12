"""
Load Test Scenarios
===================

Reusable benchmark scenarios for Sentinel AI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


###############################################################################
# Scenario Model
###############################################################################


@dataclass(frozen=True)
class LoadScenario:

    name: str

    concurrent_users: int

    requests_per_second: int

    workers: int

    websocket_connections: int

    database_transactions: int

    duration_seconds: int


###############################################################################
# Small Load
###############################################################################

SMALL_LOAD = LoadScenario(

    name="Small Load",

    concurrent_users=50,

    requests_per_second=200,

    workers=4,

    websocket_connections=100,

    database_transactions=500,

    duration_seconds=60,

)

###############################################################################
# Medium Load
###############################################################################

MEDIUM_LOAD = LoadScenario(

    name="Medium Load",

    concurrent_users=250,

    requests_per_second=1000,

    workers=16,

    websocket_connections=1000,

    database_transactions=5000,

    duration_seconds=300,

)

###############################################################################
# Heavy Load
###############################################################################

HEAVY_LOAD = LoadScenario(

    name="Heavy Load",

    concurrent_users=1000,

    requests_per_second=5000,

    workers=32,

    websocket_connections=5000,

    database_transactions=25000,

    duration_seconds=600,

)

###############################################################################
# Extreme Load
###############################################################################

EXTREME_LOAD = LoadScenario(

    name="Extreme Load",

    concurrent_users=5000,

    requests_per_second=25000,

    workers=64,

    websocket_connections=25000,

    database_transactions=100000,

    duration_seconds=900,

)

###############################################################################
# Production Load
###############################################################################

PRODUCTION_LOAD = LoadScenario(

    name="Production Load",

    concurrent_users=10000,

    requests_per_second=50000,

    workers=128,

    websocket_connections=100000,

    database_transactions=250000,

    duration_seconds=1800,

)

###############################################################################
# Trading Session Load
###############################################################################

TRADING_SESSION_LOAD = LoadScenario(

    name="Trading Session",

    concurrent_users=3000,

    requests_per_second=20000,

    workers=64,

    websocket_connections=50000,

    database_transactions=100000,

    duration_seconds=7200,

)

###############################################################################
# Memecoin Launch Load
###############################################################################

MEMECOIN_LAUNCH_LOAD = LoadScenario(

    name="Memecoin Launch",

    concurrent_users=50000,

    requests_per_second=250000,

    workers=256,

    websocket_connections=500000,

    database_transactions=1000000,

    duration_seconds=3600,

)

###############################################################################
# Registry
###############################################################################

SCENARIOS: Dict[str, LoadScenario] = {

    "small": SMALL_LOAD,

    "medium": MEDIUM_LOAD,

    "heavy": HEAVY_LOAD,

    "extreme": EXTREME_LOAD,

    "production": PRODUCTION_LOAD,

    "trading": TRADING_SESSION_LOAD,

    "launch": MEMECOIN_LAUNCH_LOAD,

}

###############################################################################
# Helpers
###############################################################################


def get_scenario(

    name: str,

) -> LoadScenario:

    return SCENARIOS[name]


###############################################################################


def list_scenarios():

    return list(

        SCENARIOS.keys()

    )


###############################################################################


def summary():

    return {

        "available_scenarios": list_scenarios(),

        "total": len(

            SCENARIOS

        ),

    }