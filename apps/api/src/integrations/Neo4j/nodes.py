"""
Neo4j Node Manager
==================
"""

from __future__ import annotations

from typing import Dict, Optional


class NodeManager:

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
        label: str,
        properties: Dict,
    ):

        query = f"""
        CREATE (n:{label})
        SET n = $properties
        RETURN n
        """

        return self.client.execute(
            query,
            {
                "properties": properties,
            },
        )

    ###########################################################################

    def merge(
        self,
        label: str,
        key: str,
        value,
        properties: Dict,
    ):

        query = f"""
        MERGE (n:{label} {{{key}:$value}})
        SET n += $properties
        RETURN n
        """

        return self.client.execute(
            query,
            {
                "value": value,
                "properties": properties,
            },
        )

    ###########################################################################

    def delete(
        self,
        label: str,
        key: str,
        value,
    ):

        query = f"""
        MATCH (n:{label} {{{key}:$value}})
        DETACH DELETE n
        """

        return self.client.execute(
            query,
            {
                "value": value,
            },
        )

    ###########################################################################
    # Wallet
    ###########################################################################

    def wallet(
        self,
        address: str,
        properties: Optional[Dict] = None,
    ):

        return self.merge(
            "Wallet",
            "address",
            address,
            properties or {},
        )

    ###########################################################################
    # Token
    ###########################################################################

    def token(
        self,
        mint: str,
        properties=None,
    ):

        return self.merge(
            "Token",
            "mint",
            mint,
            properties or {},
        )

    ###########################################################################
    # Bundle
    ###########################################################################

    def bundle(
        self,
        bundle_id: str,
        properties=None,
    ):

        return self.merge(
            "Bundle",
            "bundle_id",
            bundle_id,
            properties or {},
        )

    ###########################################################################
    # Deployer
    ###########################################################################

    def deployer(
        self,
        wallet: str,
        properties=None,
    ):

        return self.merge(
            "Deployer",
            "wallet",
            wallet,
            properties or {},
        )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "NodeManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "nodes": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def supported_nodes():

    return [
        "Wallet",
        "Token",
        "Bundle",
        "Deployer",
    ]