###############################################################################
# Imports
###############################################################################

from __future__ import annotations

###############################################################################
# API Tags
###############################################################################

Wallet = {
    "name": "Wallet",
    "description": "Wallet analysis endpoints.",
}

Token = {
    "name": "Token",
    "description": "Token intelligence endpoints.",
}

Funding = {
    "name": "Funding",
    "description": "Funding chain analysis.",
}

Bundle = {
    "name": "Bundle",
    "description": "Bundle detection endpoints.",
}

Deployer = {
    "name": "Deployer",
    "description": "Deployer intelligence.",
}

Cluster = {
    "name": "Cluster",
    "description": "Wallet clustering.",
}

Graph = {
    "name": "Graph",
    "description": "Graph engine endpoints.",
}

WalletDNA = {
    "name": "WalletDNA",
    "description": "AI Wallet DNA analysis.",
}

Statistics = {
    "name": "Statistics",
    "description": "Analytics and metrics.",
}

Search = {
    "name": "Search",
    "description": "Global search endpoints.",
}

Health = {
    "name": "Health",
    "description": "Health and readiness checks.",
}

Admin = {
    "name": "Admin",
    "description": "Administrative endpoints.",
}

###############################################################################
# OpenAPI Tags
###############################################################################


def get_tags() -> list[dict]:
    """
    Return OpenAPI tag definitions.
    """

    return [
        Wallet,
        Token,
        Funding,
        Bundle,
        Deployer,
        Cluster,
        Graph,
        WalletDNA,
        Statistics,
        Search,
        Health,
        Admin,
    ]


###############################################################################


def register_tags(app):
    """
    Register tags into FastAPI app.
    """

    app.openapi_tags = get_tags()


###############################################################################
# Runtime
###############################################################################


def summary():
    """
    Tags summary.
    """

    return {
        "total_tags": len(get_tags()),
        "names": [
            tag["name"]
            for tag in get_tags()
        ],
    }