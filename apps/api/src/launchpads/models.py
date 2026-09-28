from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from chains.models import Chain


class LaunchpadType(str, Enum):
    BONDING_CURVE = "bonding_curve"
    TOKEN_LAUNCH = "token_launch"
    FAIR_LAUNCH = "fair_launch"
    AUCTION = "auction"
    LIQUIDITY_LAUNCH = "liquidity_launch"
    AGENT_TOKEN = "agent_token"
    DAO_LAUNCH = "dao_launch"


class DiscoveryMethod(str, Enum):
    ONCHAIN_PROGRAM = "onchain_program"
    ONCHAIN_CONTRACT = "onchain_contract"
    INDEXER = "indexer"
    API = "api"
    WEBHOOK = "webhook"
    MANUAL = "manual"


@dataclass(frozen=True)
class LaunchpadConfig:
    slug: str
    name: str
    chain: Chain
    launchpad_type: LaunchpadType
    website: str
    discovery_method: DiscoveryMethod
    active: bool = True
    program_ids: tuple[str, ...] = ()
    contract_addresses: tuple[str, ...] = ()
    notes: str = ""