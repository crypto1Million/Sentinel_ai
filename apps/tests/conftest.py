"""
Shared pytest fixtures for Sentinel AI tests.
"""

import pytest

from tests.mocks.helius import mock_helius
from tests.mocks.pumpfun import mock_pumpfun
from tests.mocks.dexscreener import mock_dexscreener
from tests.mocks.raydium import mock_raydium
from tests.mocks.jupiter import mock_jupiter
from tests.mocks.redis import mock_redis
from tests.mocks.postgres import mock_postgres
from tests.mocks.neo4j import mock_neo4j


# ---------------------------------------------------------------------------
# External Services
# ---------------------------------------------------------------------------

@pytest.fixture
def helius():
    return mock_helius()


@pytest.fixture
def pumpfun():
    return mock_pumpfun()


@pytest.fixture
def dexscreener():
    return mock_dexscreener()


@pytest.fixture
def raydium():
    return mock_raydium()


@pytest.fixture
def jupiter():
    return mock_jupiter()


@pytest.fixture
def redis():
    return mock_redis()


@pytest.fixture
def postgres():
    return mock_postgres()


@pytest.fixture
def neo4j():
    return mock_neo4j()


# ---------------------------------------------------------------------------
# Common Test Data
# ---------------------------------------------------------------------------

@pytest.fixture
def wallet_data():
    return {
        "address": "Wallet001",
        "balance": 25.4,
        "tokens": ["TOKEN001"],
    }


@pytest.fixture
def token_data():
    return {
        "mint": "TOKEN001",
        "name": "Test Meme",
        "symbol": "TMEME",
        "liquidity": 125_000,
        "market_cap": 1_200_000,
    }


@pytest.fixture
def bundle_data():
    return {
        "bundle_id": "BUNDLE001",
        "percentage": 8.4,
        "wallets": [
            "Wallet001",
            "Wallet002",
        ],
    }


@pytest.fixture
def score_data():
    return {
        "narrative": "AI Narrative",
        "narrative_type": "ai",
        "narrative_strength": 91,
        "wallet_quality": 87,
        "token_quality": 92,
        "volume_quality": 89,
        "smart_money": 82,
        "rug_risk": 7,
        "sentinel_score": 91,
        "confidence": 95,
    }