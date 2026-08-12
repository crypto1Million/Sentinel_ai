"""
graph_storage.py

Production Graph Storage Layer

Responsible for:

- Wallet storage
- Token storage
- Node registry
- In-memory persistence
"""

from __future__ import annotations

# =============================================================================
# Standard Library
# =============================================================================

import copy
import logging
import sys

from typing import (
    Any,
    Dict,
    Iterable,
    Optional,
    Union,
)

# =============================================================================
# Internal Models
# =============================================================================

from .deployer_models import (
    WalletNode,
    TokenNode,
)

# =============================================================================
# Logger
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# GraphStorage
# =============================================================================

class GraphStorage:
    """
    Central storage backend for WalletDNA.

    Owns every node currently loaded into memory.

    Does NOT perform:

    • Graph Traversal
    • DFS
    • BFS
    • Indexing
    • Clustering

    Those are handled elsewhere.
    """

    # =======================================================================
    # Constructor
    # =======================================================================

    def __init__(self) -> None:

        logger.info("Initializing GraphStorage...")

        # -------------------------------------------------------------------
        # Wallet Storage
        # address -> WalletNode
        # -------------------------------------------------------------------

        self.wallets: Dict[str, WalletNode] = {}

        # -------------------------------------------------------------------
        # Token Storage
        # mint -> TokenNode
        # -------------------------------------------------------------------

        self.tokens: Dict[str, TokenNode] = {}

        # -------------------------------------------------------------------
        # Node Registry
        #
        # Every node regardless of type.
        #
        # wallet address -> WalletNode
        # token mint -> TokenNode
        # -------------------------------------------------------------------

        self.node_registry: Dict[
            str,
            Union[
                WalletNode,
                TokenNode,
            ],
        ] = {}

        # -------------------------------------------------------------------
        # Runtime Counters
        # -------------------------------------------------------------------

        self.wallet_count: int = 0

        self.token_count: int = 0

        self.node_count: int = 0

        logger.info("GraphStorage initialized successfully.")

    # =======================================================================
    # Wallet Storage
    # =======================================================================

    @property
    def wallets_view(self) -> Dict[str, WalletNode]:
        """
        Read-only wallet dictionary.
        """
        return self.wallets

    # -----------------------------------------------------------------------

    @property
    def total_wallets(self) -> int:
        return self.wallet_count

    # =======================================================================
    # Token Storage
    # =======================================================================

    @property
    def tokens_view(self) -> Dict[str, TokenNode]:
        """
        Read-only token dictionary.
        """
        return self.tokens

    # -----------------------------------------------------------------------

    @property
    def total_tokens(self) -> int:
        return self.token_count

    # =======================================================================
    # Node Registry
    # =======================================================================

    @property
    def nodes(self):
        """
        Complete registry.

        Wallets + Tokens.
        """
        return self.node_registry

    # -----------------------------------------------------------------------

    @property
    def total_nodes(self) -> int:
        return self.node_count

# =============================================================================
# CRUD Operations
# =============================================================================

# ============================================================================
# CREATE
# ============================================================================

def add_wallet(
    self,
    wallet: WalletNode,
) -> WalletNode:
    """
    Add a wallet to storage.

    If the wallet already exists it will be replaced.
    """

    if wallet is None:
        raise ValueError("Wallet cannot be None.")

    self.wallets[wallet.address] = wallet
    self.node_registry[wallet.address] = wallet

    self.wallet_count = len(self.wallets)
    self.node_count = len(self.node_registry)

    logger.debug(f"Wallet added: {wallet.address}")

    return wallet


# ---------------------------------------------------------------------------

def add_token(
    self,
    token: TokenNode,
) -> TokenNode:
    """
    Add a token to storage.
    """

    if token is None:
        raise ValueError("Token cannot be None.")

    self.tokens[token.mint] = token
    self.node_registry[token.mint] = token

    self.token_count = len(self.tokens)
    self.node_count = len(self.node_registry)

    logger.debug(f"Token added: {token.mint}")

    return token


# ============================================================================
# READ
# ============================================================================

def get_wallet(
    self,
    address: str,
) -> Optional[WalletNode]:
    """
    Retrieve wallet by address.
    """

    return self.wallets.get(address)


# ---------------------------------------------------------------------------

def get_token(
    self,
    mint: str,
) -> Optional[TokenNode]:
    """
    Retrieve token by mint.
    """

    return self.tokens.get(mint)


# ---------------------------------------------------------------------------

def get_node(
    self,
    node_id: str,
) -> Optional[Union[WalletNode, TokenNode]]:
    """
    Retrieve any node.
    """

    return self.node_registry.get(node_id)


# ---------------------------------------------------------------------------

def has_wallet(
    self,
    address: str,
) -> bool:

    return address in self.wallets


# ---------------------------------------------------------------------------

def has_token(
    self,
    mint: str,
) -> bool:

    return mint in self.tokens


# ---------------------------------------------------------------------------

def has_node(
    self,
    node_id: str,
) -> bool:

    return node_id in self.node_registry


# ============================================================================
# UPDATE
# ============================================================================

def update_wallet(
    self,
    wallet: WalletNode,
) -> WalletNode:
    """
    Replace wallet.
    """

    if wallet.address not in self.wallets:
        raise KeyError(wallet.address)

    self.wallets[wallet.address] = wallet
    self.node_registry[wallet.address] = wallet

    logger.debug(f"Wallet updated: {wallet.address}")

    return wallet


# ---------------------------------------------------------------------------

def update_token(
    self,
    token: TokenNode,
) -> TokenNode:
    """
    Replace token.
    """

    if token.mint not in self.tokens:
        raise KeyError(token.mint)

    self.tokens[token.mint] = token
    self.node_registry[token.mint] = token

    logger.debug(f"Token updated: {token.mint}")

    return token


# ============================================================================
# DELETE
# ============================================================================

def remove_wallet(
    self,
    address: str,
) -> bool:
    """
    Remove wallet from storage.
    """

    if address not in self.wallets:
        return False

    del self.wallets[address]
    self.node_registry.pop(address, None)

    self.wallet_count = len(self.wallets)
    self.node_count = len(self.node_registry)

    logger.debug(f"Wallet removed: {address}")

    return True


# ---------------------------------------------------------------------------

def remove_token(
    self,
    mint: str,
) -> bool:
    """
    Remove token from storage.
    """

    if mint not in self.tokens:
        return False

    del self.tokens[mint]
    self.node_registry.pop(mint, None)

    self.token_count = len(self.tokens)
    self.node_count = len(self.node_registry)

    logger.debug(f"Token removed: {mint}")

    return True


# ---------------------------------------------------------------------------

def clear(self) -> None:
    """
    Remove every stored node.
    """

    self.wallets.clear()
    self.tokens.clear()
    self.node_registry.clear()

    self.wallet_count = 0
    self.token_count = 0
    self.node_count = 0

    logger.info("GraphStorage cleared.")        

# =============================================================================
# Batch Operations
# =============================================================================

# ============================================================================
# Batch Create
# ============================================================================

def add_wallets(
    self,
    wallets: Iterable[WalletNode],
) -> int:
    """
    Add multiple wallets.

    Returns:
        Number of wallets inserted.
    """

    inserted = 0

    for wallet in wallets:
        self.add_wallet(wallet)
        inserted += 1

    logger.info(f"Added {inserted} wallets.")

    return inserted


# ---------------------------------------------------------------------------

def add_tokens(
    self,
    tokens: Iterable[TokenNode],
) -> int:
    """
    Add multiple tokens.

    Returns:
        Number of tokens inserted.
    """

    inserted = 0

    for token in tokens:
        self.add_token(token)
        inserted += 1

    logger.info(f"Added {inserted} tokens.")

    return inserted


# ============================================================================
# Batch Update
# ============================================================================

def update_wallets(
    self,
    wallets: Iterable[WalletNode],
) -> int:
    """
    Update multiple wallets.

    Returns:
        Number of updated wallets.
    """

    updated = 0

    for wallet in wallets:

        if self.has_wallet(wallet.address):

            self.update_wallet(wallet)

            updated += 1

    logger.info(f"Updated {updated} wallets.")

    return updated


# ---------------------------------------------------------------------------

def update_tokens(
    self,
    tokens: Iterable[TokenNode],
) -> int:
    """
    Update multiple tokens.

    Returns:
        Number of updated tokens.
    """

    updated = 0

    for token in tokens:

        if self.has_token(token.mint):

            self.update_token(token)

            updated += 1

    logger.info(f"Updated {updated} tokens.")

    return updated


# ============================================================================
# Batch Delete
# ============================================================================

def remove_wallets(
    self,
    addresses: Iterable[str],
) -> int:
    """
    Remove multiple wallets.

    Returns:
        Number removed.
    """

    removed = 0

    for address in addresses:

        if self.remove_wallet(address):

            removed += 1

    logger.info(f"Removed {removed} wallets.")

    return removed


# ---------------------------------------------------------------------------

def remove_tokens(
    self,
    mints: Iterable[str],
) -> int:
    """
    Remove multiple tokens.

    Returns:
        Number removed.
    """

    removed = 0

    for mint in mints:

        if self.remove_token(mint):

            removed += 1

    logger.info(f"Removed {removed} tokens.")

    return removed


# ============================================================================
# Batch Lookup
# ============================================================================

def get_wallets(
    self,
    addresses: Iterable[str],
) -> List[WalletNode]:
    """
    Fetch multiple wallets.
    """

    return [

        self.wallets[address]

        for address in addresses

        if address in self.wallets

    ]


# ---------------------------------------------------------------------------

def get_tokens(
    self,
    mints: Iterable[str],
) -> List[TokenNode]:
    """
    Fetch multiple tokens.
    """

    return [

        self.tokens[mint]

        for mint in mints

        if mint in self.tokens

    ]


# ============================================================================
# Batch Existence
# ============================================================================

def wallets_exist(
    self,
    addresses: Iterable[str],
) -> Dict[str, bool]:
    """
    Check existence of multiple wallets.
    """

    return {

        address: self.has_wallet(address)

        for address in addresses

    }


# ---------------------------------------------------------------------------

def tokens_exist(
    self,
    mints: Iterable[str],
) -> Dict[str, bool]:
    """
    Check existence of multiple tokens.
    """

    return {

        mint: self.has_token(mint)

        for mint in mints

    }


# ============================================================================
# Batch Snapshot
# ============================================================================

def snapshot_wallets(self) -> Dict[str, WalletNode]:
    """
    Deep-copy wallet storage.
    """

    return copy.deepcopy(self.wallets)


# ---------------------------------------------------------------------------

def snapshot_tokens(self) -> Dict[str, TokenNode]:
    """
    Deep-copy token storage.
    """

    return copy.deepcopy(self.tokens)    