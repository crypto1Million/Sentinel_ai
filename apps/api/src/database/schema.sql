CREATE TABLE tokens (

    id BIGSERIAL PRIMARY KEY,

    mint_address TEXT UNIQUE NOT NULL,

    symbol TEXT,

    name TEXT,

    decimals INTEGER,

    supply NUMERIC,

    creator_wallet TEXT,

    market_cap NUMERIC DEFAULT 0,

    volume_24h NUMERIC DEFAULT 0,

    holders INTEGER DEFAULT 0,

    created_at TIMESTAMP,

    inserted_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_token_symbol
ON tokens(symbol);

CREATE INDEX idx_token_created
ON tokens(created_at);

-- =====================================================
-- WALLET RELATIONSHIPS
-- =====================================================

CREATE TABLE IF NOT EXISTS wallet_relationships (
    id SERIAL PRIMARY KEY,

    wallet_a VARCHAR(255),
    wallet_b VARCHAR(255),

    relationship_type VARCHAR(100),

    confidence FLOAT DEFAULT 0,

    interaction_count INTEGER DEFAULT 0,

    shared_tokens INTEGER DEFAULT 0,
    shared_trades INTEGER DEFAULT 0,

    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- WALLET SNAPSHOTS
-- =====================================================

CREATE TABLE IF NOT EXISTS wallet_snapshots (
    id SERIAL PRIMARY KEY,

    wallet_address VARCHAR(255),

    total_value_usd FLOAT DEFAULT 0,

    realized_pnl FLOAT DEFAULT 0,
    unrealized_pnl FLOAT DEFAULT 0,

    win_rate FLOAT DEFAULT 0,

    token_count INTEGER DEFAULT 0,

    smart_money_score FLOAT DEFAULT 0,
    whale_score FLOAT DEFAULT 0,
    conviction_score FLOAT DEFAULT 0,

    snapshot_time TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- TOKEN SNAPSHOTS
-- =====================================================

CREATE TABLE IF NOT EXISTS token_snapshots (
    id SERIAL PRIMARY KEY,

    token_address VARCHAR(255),

    market_cap FLOAT DEFAULT 0,

    liquidity FLOAT DEFAULT 0,

    volume_1m FLOAT DEFAULT 0,
    volume_5m FLOAT DEFAULT 0,
    volume_1h FLOAT DEFAULT 0,

    holders INTEGER DEFAULT 0,

    buy_count INTEGER DEFAULT 0,
    sell_count INTEGER DEFAULT 0,

    smart_money_percentage FLOAT DEFAULT 0,
    whale_percentage FLOAT DEFAULT 0,
    insider_percentage FLOAT DEFAULT 0,

    fresh_wallet_percentage FLOAT DEFAULT 0,

    bundled_percentage FLOAT DEFAULT 0,
    sniper_percentage FLOAT DEFAULT 0,

    lp_burned BOOLEAN DEFAULT FALSE,
    lp_locked BOOLEAN DEFAULT FALSE,

    snapshot_time TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- PERFORMANCE INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_wallet_relationship_a
ON wallet_relationships(wallet_a);

CREATE INDEX IF NOT EXISTS idx_wallet_relationship_b
ON wallet_relationships(wallet_b);

CREATE INDEX IF NOT EXISTS idx_wallet_snapshot_wallet
ON wallet_snapshots(wallet_address);

CREATE INDEX IF NOT EXISTS idx_wallet_snapshot_time
ON wallet_snapshots(snapshot_time);

CREATE INDEX IF NOT EXISTS idx_token_snapshot_token
ON token_snapshots(token_address);

CREATE INDEX IF NOT EXISTS idx_token_snapshot_time
ON token_snapshots(snapshot_time);

-- =====================================================
-- FUTURE ANALYTICS TABLES
-- =====================================================

-- capital_flows
-- liquidity_migrations
-- smart_money_entries
-- smart_money_exits
-- whale_entries
-- whale_exits
-- holder_churn
-- wallet_cluster_events

CREATE TABLE watchlists (

    id TEXT PRIMARY KEY,

    user_id TEXT NOT NULL,

    name VARCHAR(100) NOT NULL,

    description TEXT,

    created_at TIMESTAMP,

    updated_at TIMESTAMP

);

CREATE INDEX idx_watchlists_user
ON watchlists(user_id);



CREATE TABLE watchlist_items (

    id TEXT PRIMARY KEY,

    watchlist_id TEXT NOT NULL,

    mint TEXT NOT NULL,

    created_at TIMESTAMP,

    FOREIGN KEY (watchlist_id)

        REFERENCES watchlists(id)

        ON DELETE CASCADE

);

CREATE INDEX idx_watchlist_items_watchlist
ON watchlist_items(watchlist_id);

CREATE INDEX idx_watchlist_items_mint
ON watchlist_items(mint);