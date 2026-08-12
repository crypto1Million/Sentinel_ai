"""
Neo4j Relationship Manager
==========================

Creates, updates and removes graph relationships.
"""

from __future__ import annotations

from typing import Dict, Optional


###############################################################################
# RelationshipManager
###############################################################################


class RelationshipManager:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, client):

        self.client = client

    ###########################################################################
    # Generic
    ###########################################################################

    def create(
        self,
        source_label: str,
        source_key: str,
        source_value: str,
        relationship: str,
        target_label: str,
        target_key: str,
        target_value: str,
        properties: Optional[Dict] = None,
    ):

        query = f"""
        MATCH (a:{source_label} {{{source_key}:$source}})
        MATCH (b:{target_label} {{{target_key}:$target}})
        MERGE (a)-[r:{relationship}]->(b)
        SET r += $properties
        RETURN r
        """

        return self.client.execute(
            query,
            {
                "source": source_value,
                "target": target_value,
                "properties": properties or {},
            },
        )

    ###########################################################################

    def delete(
        self,
        relationship: str,
        source: str,
        target: str,
    ):

        query = f"""
        MATCH (a)-[r:{relationship}]->(b)
        WHERE id(a)=$source AND id(b)=$target
        DELETE r
        """

        return self.client.execute(
            query,
            {
                "source": int(source),
                "target": int(target),
            },
        )

    ###########################################################################
    # Wallet Relationships
    ###########################################################################

    def funding(
        self,
        from_wallet: str,
        to_wallet: str,
        amount: float,
    ):

        return self.create(
            "Wallet",
            "address",
            from_wallet,
            "FUNDED",
            "Wallet",
            "address",
            to_wallet,
            {"amount": amount},
        )

    ###########################################################################

    def transfer(
        self,
        from_wallet: str,
        to_wallet: str,
        amount: float,
    ):

        return self.create(
            "Wallet",
            "address",
            from_wallet,
            "TRANSFERRED",
            "Wallet",
            "address",
            to_wallet,
            {"amount": amount},
        )

    ###########################################################################
    # Token Relationships
    ###########################################################################

    def owns(
        self,
        wallet: str,
        token: str,
        amount: float,
    ):

        return self.create(
            "Wallet",
            "address",
            wallet,
            "OWNS",
            "Token",
            "mint",
            token,
            {"balance": amount},
        )

    ###########################################################################

    def traded(
        self,
        wallet: str,
        token: str,
    ):

        return self.create(
            "Wallet",
            "address",
            wallet,
            "TRADED",
            "Token",
            "mint",
            token,
        )

    ###########################################################################
    # Deployer
    ###########################################################################

    def deployed(
        self,
        deployer: str,
        token: str,
    ):

        return self.create(
            "Deployer",
            "wallet",
            deployer,
            "DEPLOYED",
            "Token",
            "mint",
            token,
        )

    ###########################################################################
    # Bundle
    ###########################################################################

    def bundled(
        self,
        wallet: str,
        bundle: str,
    ):

        return self.create(
            "Wallet",
            "address",
            wallet,
            "BUNDLED",
            "Bundle",
            "bundle_id",
            bundle,
        )

    ###########################################################################
    # Graph
    ###########################################################################

    def connected(
        self,
        wallet_a: str,
        wallet_b: str,
    ):

        return self.create(
            "Wallet",
            "address",
            wallet_a,
            "CONNECTED",
            "Wallet",
            "address",
            wallet_b,
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "RelationshipManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "relationship_manager": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def relationship_metadata():

    return {
        "supported": [
            "FUNDED",
            "TRANSFERRED",
            "OWNS",
            "TRADED",
            "DEPLOYED",
            "BUNDLED",
            "CONNECTED",
        ]
    }