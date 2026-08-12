"""
Neo4j Graph Models
==================
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


###############################################################################
# Node Models
###############################################################################


class WalletNode(BaseModel):

    address: str

    score: Optional[float] = None

    balance: Optional[float] = None

    labels: List[str] = Field(default_factory=list)


###############################################################################


class TokenNode(BaseModel):

    mint: str

    symbol: Optional[str] = None

    name: Optional[str] = None

    score: Optional[float] = None


###############################################################################


class BundleNode(BaseModel):

    bundle_id: str

    score: Optional[float] = None


###############################################################################


class DeployerNode(BaseModel):

    wallet: str

    score: Optional[float] = None


###############################################################################


class FundingNode(BaseModel):

    funding_id: str

    amount: float


###############################################################################


class ClusterNode(BaseModel):

    cluster_id: str

    size: int = 0


###############################################################################


class GraphNode(BaseModel):

    node_id: str

    labels: List[str] = Field(default_factory=list)

    properties: Dict = Field(default_factory=dict)


###############################################################################
# Relationship Models
###############################################################################


class FundingRelationship(BaseModel):

    from_wallet: str

    to_wallet: str

    amount: float


###############################################################################


class TransferRelationship(BaseModel):

    from_wallet: str

    to_wallet: str

    amount: float


###############################################################################


class BundleRelationship(BaseModel):

    wallet: str

    bundle: str


###############################################################################


class HolderRelationship(BaseModel):

    wallet: str

    token: str

    balance: float


###############################################################################


class DeployRelationship(BaseModel):

    deployer: str

    token: str


###############################################################################


class SwapRelationship(BaseModel):

    wallet: str

    token: str

    volume: float


###############################################################################


class ConnectedRelationship(BaseModel):

    wallet_a: str

    wallet_b: str


###############################################################################
# Analytics Models
###############################################################################


class CentralityScore(BaseModel):

    node: str

    score: float


###############################################################################


class CommunityModel(BaseModel):

    community_id: int

    members: List[str] = Field(default_factory=list)


###############################################################################


class PathModel(BaseModel):

    source: str

    target: str

    hops: List[str] = Field(default_factory=list)


###############################################################################


class ClusterModel(BaseModel):

    cluster_id: str

    wallets: List[str] = Field(default_factory=list)


###############################################################################


class RiskModel(BaseModel):

    wallet: str

    risk: float

    reason: Optional[str] = None


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "node_models": 7,
        "relationship_models": 7,
        "analytics_models": 5,
    }


###############################################################################
# Utilities
###############################################################################


def validators():

    return {
        "wallet": "address",
        "mint": "token",
        "bundle": "bundle_id",
        "relationship": "valid",
    }