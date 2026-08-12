###############################################################################
# Wallet Examples
###############################################################################

WALLET_EXAMPLES = {
    "wallet": {
        "address": "6m7Lk3ExampleWallet111111111111111111111111111",
    },
    "wallet_summary": {
        "address": "6m7Lk3ExampleWallet111111111111111111111111111",
        "score": 91.4,
        "risk": 12.3,
        "conviction": 95.1,
    },
}

###############################################################################
# Token Examples
###############################################################################

TOKEN_EXAMPLES = {
    "token": {
        "mint": "ExampleMint111111111111111111111111111111111111",
    },
    "token_summary": {
        "symbol": "DOGEAI",
        "market_cap": 145000,
        "liquidity": 25000,
    },
}

###############################################################################
# Funding Examples
###############################################################################

FUNDING_EXAMPLES = {
    "funding_chain": {
        "source": "WalletA",
        "destination": "WalletB",
        "amount_sol": 2.5,
    }
}

###############################################################################
# Bundle Examples
###############################################################################

BUNDLE_EXAMPLES = {
    "bundle": {
        "bundle_id": "bundle-001",
        "wallet_count": 12,
    }
}

###############################################################################
# Graph Examples
###############################################################################

GRAPH_EXAMPLES = {
    "graph": {
        "nodes": [],
        "edges": [],
    }
}

###############################################################################
# WalletDNA Examples
###############################################################################

WALLETDNA_EXAMPLES = {
    "wallet_dna": {
        "overall": 94.6,
        "conviction": 91.2,
        "risk": 8.4,
    }
}

###############################################################################
# Statistics Examples
###############################################################################

STATISTICS_EXAMPLES = {
    "statistics": {
        "wallets": 120394,
        "tokens": 51923,
        "graphs": 834,
    }
}

###############################################################################
# Search Examples
###############################################################################

SEARCH_EXAMPLES = {
    "search": {
        "query": "wallet",
        "limit": 20,
    }
}

###############################################################################
# Export Examples
###############################################################################

EXPORT_EXAMPLES = {
    "export": {
        "format": "json",
        "compressed": False,
    }
}

###############################################################################
# Utilities
###############################################################################


def load_examples():
    """
    Return every example.
    """

    return {
        "wallet": WALLET_EXAMPLES,
        "token": TOKEN_EXAMPLES,
        "funding": FUNDING_EXAMPLES,
        "bundle": BUNDLE_EXAMPLES,
        "graph": GRAPH_EXAMPLES,
        "wallet_dna": WALLETDNA_EXAMPLES,
        "statistics": STATISTICS_EXAMPLES,
        "search": SEARCH_EXAMPLES,
        "export": EXPORT_EXAMPLES,
    }


###############################################################################


def summary():
    """
    Examples summary.
    """

    return {
        "groups": len(load_examples()),
        "available": list(load_examples().keys()),
    }