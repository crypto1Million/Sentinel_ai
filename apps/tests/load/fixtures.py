"""
Shared Load Test Fixtures
=========================

Reusable benchmark datasets for Sentinel AI load tests.
"""

from __future__ import annotations

from typing import Dict, List


###############################################################################
# Wallet Fixtures
###############################################################################

WALLETS: List[Dict] = [

    {
        "address": "Wallet001",
        "balance": 25.4,
        "score": 94,
    },

    {
        "address": "Wallet002",
        "balance": 12.7,
        "score": 87,
    },

    {
        "address": "Wallet003",
        "balance": 3.9,
        "score": 72,
    },

]

###############################################################################
# Token Fixtures
###############################################################################

TOKENS: List[Dict] = [

    {
        "mint": "TOKEN111",
        "symbol": "DOGEAI",
        "price": 0.00123,
        "liquidity": 240000,
    },

    {
        "mint": "TOKEN222",
        "symbol": "MEMEX",
        "price": 0.00457,
        "liquidity": 540000,
    },

]

###############################################################################
# Bundle Fixtures
###############################################################################

BUNDLES: List[Dict] = [

    {
        "bundle_id": "bundle001",
        "wallets": 5,
        "percentage": 12.3,
    },

    {
        "bundle_id": "bundle002",
        "wallets": 11,
        "percentage": 26.7,
    },

]

###############################################################################
# Graph Fixtures
###############################################################################

GRAPHS: List[Dict] = [

    {

        "nodes": 100,

        "relationships": 250,

    },

    {

        "nodes": 1000,

        "relationships": 3400,

    },

]

###############################################################################
# AI Score Fixtures
###############################################################################

AI_SCORES: List[Dict] = [

    {

        "wallet_score": 91,

        "token_score": 95,

        "rug_score": 8,

        "sentinel_score": 93,

        "confidence": 97,

    },

    {

        "wallet_score": 64,

        "token_score": 58,

        "rug_score": 74,

        "sentinel_score": 41,

        "confidence": 55,

    },

]

###############################################################################
# WebSocket Event Fixtures
###############################################################################

WEBSOCKET_EVENTS: List[Dict] = [

    {

        "event": "NEW_TOKEN",

        "mint": "TOKEN111",

    },

    {

        "event": "NEW_SWAP",

        "wallet": "Wallet001",

    },

    {

        "event": "NEW_BUNDLE",

        "bundle": "bundle001",

    },

    {

        "event": "RUG_ALERT",

        "mint": "TOKEN222",

    },

]

###############################################################################
# Helper Functions
###############################################################################

def wallet():

    return WALLETS[0]


###############################################################################

def token():

    return TOKENS[0]


###############################################################################

def bundle():

    return BUNDLES[0]


###############################################################################

def graph():

    return GRAPHS[0]


###############################################################################

def ai_score():

    return AI_SCORES[0]


###############################################################################

def websocket_event():

    return WEBSOCKET_EVENTS[0]


###############################################################################

def all_fixtures():

    return {

        "wallets": WALLETS,

        "tokens": TOKENS,

        "bundles": BUNDLES,

        "graphs": GRAPHS,

        "ai_scores": AI_SCORES,

        "websocket_events": WEBSOCKET_EVENTS,

    }


###############################################################################

def summary():

    return {

        "wallets": len(WALLETS),

        "tokens": len(TOKENS),

        "bundles": len(BUNDLES),

        "graphs": len(GRAPHS),

        "ai_scores": len(AI_SCORES),

        "websocket_events": len(WEBSOCKET_EVENTS),

    }