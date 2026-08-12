# ==========================================================
# Part 1
# Imports
# Constants
# Enums
# Type Aliases
# DatabaseConfig
# WalletRecord
# TransactionRecord
# CacheRecord
# DatabaseStats
# ==========================================================

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import time

from dataclasses import (
    dataclass,
    field,
)

from datetime import datetime

from enum import Enum

from pathlib import Path

from typing import (
    Any,
    Dict,
    List,
    Optional,
    TypeAlias,
)

# ==========================================================
# Constants
# ==========================================================

DEFAULT_DATABASE_NAME = (
    "sentinel_wallets.db"
)

DEFAULT_CACHE_TTL = 600

DEFAULT_BATCH_SIZE = 100

DEFAULT_TIMEOUT = 30

DEFAULT_PAGE_SIZE = 1000

DEFAULT_MAX_CACHE_ITEMS = 50000

DATABASE_VERSION = "1.0.0"

# ==========================================================
# Enums
# ==========================================================

class DatabaseBackend(Enum):
    """
    Supported storage backends.
    """

    SQLITE = "sqlite"

    POSTGRES = "postgres"

    CLICKHOUSE = "clickhouse"

    REDIS = "redis"

    MEMORY = "memory"


class WalletLabel(Enum):
    """
    Known wallet classifications.
    """

    UNKNOWN = "unknown"

    USER = "user"

    WHALE = "whale"

    SMART_MONEY = "smart_money"

    EXCHANGE = "exchange"

    BRIDGE = "bridge"

    DEPLOYER = "deployer"

    MARKET_MAKER = "market_maker"

    TEAM = "team"

    SNIPER = "sniper"

    INSIDER = "insider"


class CacheState(Enum):
    """
    Cache lifecycle.
    """

    VALID = "valid"

    EXPIRED = "expired"

    MISSING = "missing"


# ==========================================================
# Type Aliases
# ==========================================================

WalletAddress: TypeAlias = str

Signature: TypeAlias = str

TokenMint: TypeAlias = str

ProgramID: TypeAlias = str

JSONDict: TypeAlias = Dict[str, Any]

# ==========================================================
# Database Configuration
# ==========================================================

@dataclass(slots=True)
class DatabaseConfig:
    """
    Wallet database configuration.
    """

    backend: DatabaseBackend = (
        DatabaseBackend.SQLITE
    )

    database_path: Path = Path(
        DEFAULT_DATABASE_NAME
    )

    cache_ttl: int = (
        DEFAULT_CACHE_TTL
    )

    timeout: int = (
        DEFAULT_TIMEOUT
    )

    batch_size: int = (
        DEFAULT_BATCH_SIZE
    )

    page_size: int = (
        DEFAULT_PAGE_SIZE
    )

    max_cache_items: int = (
        DEFAULT_MAX_CACHE_ITEMS
    )

    enable_cache: bool = True

    enable_wal_mode: bool = True

    auto_commit: bool = True

    backup_enabled: bool = True


# ==========================================================
# Wallet Record
# ==========================================================

@dataclass(slots=True)
class WalletRecord:
    """
    Persistent wallet metadata.
    """

    address: WalletAddress

    label: WalletLabel = (
        WalletLabel.UNKNOWN
    )

    risk_score: float = 0.0

    confidence: float = 1.0

    balance_sol: float = 0.0

    first_seen: Optional[
        datetime
    ] = None

    last_seen: Optional[
        datetime
    ] = None

    tags: List[str] = field(
        default_factory=list
    )

    metadata: JSONDict = field(
        default_factory=dict
    )


# ==========================================================
# Transaction Record
# ==========================================================

@dataclass(slots=True)
class TransactionRecord:
    """
    Persistent transaction record.
    """

    signature: Signature

    slot: int

    timestamp: int

    sender: WalletAddress

    receiver: WalletAddress

    amount: float

    token_mint: Optional[
        TokenMint
    ] = None

    program_id: Optional[
        ProgramID
    ] = None

    fee: float = 0.0

    success: bool = True

    metadata: JSONDict = field(
        default_factory=dict
    )


# ==========================================================
# Cache Record
# ==========================================================

@dataclass(slots=True)
class CacheRecord:
    """
    Generic cache entry.
    """

    key: str

    value: Any

    created_at: float

    expires_at: float

    hash: str = ""

    metadata: JSONDict = field(
        default_factory=dict
    )


# ==========================================================
# Database Statistics
# ==========================================================

@dataclass(slots=True)
class DatabaseStats:
    """
    Runtime database metrics.
    """

    start_time: float = field(
        default_factory=time.time
    )

    wallets: int = 0

    transactions: int = 0

    cache_entries: int = 0

    cache_hits: int = 0

    cache_misses: int = 0

    reads: int = 0

    writes: int = 0

    updates: int = 0

    deletes: int = 0

    commits: int = 0

    last_backup: Optional[
        datetime
    ] = None

    last_vacuum: Optional[
        datetime
    ] = None

    database_size: int = 0

    uptime_seconds: float = 0.0

# ==========================================================
# Part 2
# Initialization
# Database Connection
# Cache
# Statistics
# ==========================================================

class WalletDatabase:
    """
    Central persistence layer for Sentinel AI.

    Every engine should access persistent
    wallet information through this class
    instead of talking directly to SQLite,
    PostgreSQL, Redis or ClickHouse.
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        *,
        config: Optional[
            DatabaseConfig
        ] = None,
    ) -> None:

        self.config = (
            config
            or DatabaseConfig()
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        # ==================================================
        # Database Connection
        # ==================================================

        self.connection: Optional[
            sqlite3.Connection
        ] = None

        self.cursor: Optional[
            sqlite3.Cursor
        ] = None

        if (

            self.config.backend

            ==

            DatabaseBackend.SQLITE

        ):

            self.connection = sqlite3.connect(

                self.config.database_path,

                timeout=self.config.timeout,

                check_same_thread=False,

            )

            self.connection.row_factory = (
                sqlite3.Row
            )

            self.cursor = (
                self.connection.cursor()
            )

            if self.config.enable_wal_mode:

                self.cursor.execute(

                    "PRAGMA journal_mode=WAL;"

                )

                self.cursor.execute(

                    "PRAGMA synchronous=NORMAL;"

                )

                self.connection.commit()

        # ==================================================
        # Cache
        # ==================================================

        self.wallet_cache: Dict[
            WalletAddress,
            WalletRecord,
        ] = {}

        self.transaction_cache: Dict[
            Signature,
            TransactionRecord,
        ] = {}

        self.similarity_cache: Dict[
            str,
            Any,
        ] = {}

        self.cluster_cache: Dict[
            str,
            Any,
        ] = {}

        self.funding_cache: Dict[
            str,
            Any,
        ] = {}

        self.generic_cache: Dict[
            str,
            CacheRecord,
        ] = {}

        self.cache_expiry: Dict[
            str,
            float,
        ] = {}

        # ==================================================
        # Statistics
        # ==================================================

        self.stats = DatabaseStats()

        self.statistics: Dict[
            str,
            Any,
        ] = {

            "database_version":
                DATABASE_VERSION,

            "backend":
                self.config.backend.value,

            "database_path":
                str(
                    self.config.database_path
                ),

            "connected":
                self.connection is not None,

            "wallets":
                0,

            "transactions":
                0,

            "cache_entries":
                0,

            "cache_hits":
                0,

            "cache_misses":
                0,

            "reads":
                0,

            "writes":
                0,

            "updates":
                0,

            "deletes":
                0,

            "commits":
                0,

            "uptime":
                0.0,

            "last_commit":
                None,

            "last_backup":
                None,

        }

        self.logger.info(

            "WalletDatabase initialized "

            "(backend=%s)",

            self.config.backend.value,

        )

# ==========================================================
# Part 3
# Wallet Storage
# ==========================================================

def save_wallet(
    self,
    wallet: WalletRecord,
) -> WalletRecord:
    """
    Save a wallet record.

    Existing records are replaced.
    """

    if self.connection is None:

        raise RuntimeError(
            "Database is not connected."
        )

    tags = json.dumps(wallet.tags)

    metadata = json.dumps(
        wallet.metadata
    )

    self.cursor.execute(
        """
        INSERT OR REPLACE INTO wallets (

            address,
            label,
            risk_score,
            confidence,
            balance_sol,
            first_seen,
            last_seen,
            tags,
            metadata

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            wallet.address,
            wallet.label.value,
            wallet.risk_score,
            wallet.confidence,
            wallet.balance_sol,
            wallet.first_seen,
            wallet.last_seen,
            tags,
            metadata,
        ),
    )

    if self.config.auto_commit:

        self.connection.commit()

        self.statistics[
            "commits"
        ] += 1

    self.wallet_cache[
        wallet.address
    ] = wallet

    self.statistics[
        "writes"
    ] += 1

    self.statistics[
        "wallets"
    ] += 1

    return wallet


# ==========================================================


def load_wallet(
    self,
    address: WalletAddress,
) -> Optional[
    WalletRecord
]:
    """
    Load a wallet by address.
    """

    cached = self.wallet_cache.get(
        address
    )

    if cached is not None:

        self.statistics[
            "cache_hits"
        ] += 1

        return cached

    self.statistics[
        "cache_misses"
    ] += 1

    row = self.cursor.execute(
        """
        SELECT *
        FROM wallets
        WHERE address = ?
        """,
        (
            address,
        ),
    ).fetchone()

    if row is None:

        return None

    wallet = WalletRecord(

        address=row["address"],

        label=WalletLabel(
            row["label"]
        ),

        risk_score=row[
            "risk_score"
        ],

        confidence=row[
            "confidence"
        ],

        balance_sol=row[
            "balance_sol"
        ],

        first_seen=row[
            "first_seen"
        ],

        last_seen=row[
            "last_seen"
        ],

        tags=json.loads(
            row["tags"]
        ),

        metadata=json.loads(
            row["metadata"]
        ),

    )

    self.wallet_cache[
        address
    ] = wallet

    self.statistics[
        "reads"
    ] += 1

    return wallet


# ==========================================================


def wallet_exists(
    self,
    address: WalletAddress,
) -> bool:
    """
    Determine whether a wallet exists.
    """

    if address in self.wallet_cache:

        return True

    row = self.cursor.execute(
        """
        SELECT 1
        FROM wallets
        WHERE address = ?
        LIMIT 1
        """,
        (
            address,
        ),
    ).fetchone()

    return row is not None


# ==========================================================


def delete_wallet(
    self,
    address: WalletAddress,
) -> bool:
    """
    Delete a wallet record.
    """

    if not self.wallet_exists(
        address
    ):

        return False

    self.cursor.execute(
        """
        DELETE
        FROM wallets
        WHERE address = ?
        """,
        (
            address,
        ),
    )

    if self.config.auto_commit:

        self.connection.commit()

        self.statistics[
            "commits"
        ] += 1

    self.wallet_cache.pop(
        address,
        None,
    )

    self.statistics[
        "deletes"
    ] += 1

    return True


# ==========================================================


def update_wallet(
    self,
    address: WalletAddress,
    **updates: Any,
) -> Optional[
    WalletRecord
]:
    """
    Update wallet fields.

    Only supplied attributes
    are modified.
    """

    wallet = self.load_wallet(
        address
    )

    if wallet is None:

        return None

    for key, value in updates.items():

        if hasattr(
            wallet,
            key,
        ):

            setattr(
                wallet,
                key,
                value,
            )

    wallet.last_seen = (
        datetime.utcnow()
    )

    self.save_wallet(
        wallet
    )

    self.statistics[
        "updates"
    ] += 1

    return wallet

# ==========================================================
# save_wallet()
# ==========================================================

def save_wallet(
    self,
    wallet: WalletRecord,
    *,
    validate: bool = True,
    overwrite: bool = True,
    commit: Optional[bool] = None,
) -> WalletRecord:
    """
    Persist a wallet into the database.

    Features
    --------
    • Validation
    • Cache synchronization
    • UPSERT support
    • Automatic timestamps
    • Statistics update
    • Transaction safety

    Parameters
    ----------
    wallet:
        WalletRecord to store.

    validate:
        Validate wallet before saving.

    overwrite:
        If False, existing wallet is returned.

    commit:
        Override auto_commit configuration.

    Returns
    -------
    WalletRecord
    """

    if self.connection is None:

        raise RuntimeError(
            "Database is not connected."
        )

    if validate:

        self.validate_wallet(
            wallet.address
        )

    if commit is None:

        commit = (
            self.config.auto_commit
        )

    existing = self.wallet_cache.get(
        wallet.address
    )

    if existing is None:

        existing = self.load_wallet(
            wallet.address
        )

    if (

        existing is not None

        and

        not overwrite

    ):

        return existing

    now = datetime.utcnow()

    if wallet.first_seen is None:

        wallet.first_seen = now

    wallet.last_seen = now

    tags_json = json.dumps(
        wallet.tags,
        ensure_ascii=False,
    )

    metadata_json = json.dumps(
        wallet.metadata,
        ensure_ascii=False,
        default=str,
    )

    try:

        self.cursor.execute(
            """
            INSERT INTO wallets (

                address,

                label,

                risk_score,

                confidence,

                balance_sol,

                first_seen,

                last_seen,

                tags,

                metadata

            )

            VALUES (

                ?,?,?,?,?,?,?,?,?

            )

            ON CONFLICT(address)

            DO UPDATE SET

                label=excluded.label,

                risk_score=excluded.risk_score,

                confidence=excluded.confidence,

                balance_sol=excluded.balance_sol,

                last_seen=excluded.last_seen,

                tags=excluded.tags,

                metadata=excluded.metadata

            """,
            (
                wallet.address,

                wallet.label.value,

                wallet.risk_score,

                wallet.confidence,

                wallet.balance_sol,

                wallet.first_seen,

                wallet.last_seen,

                tags_json,

                metadata_json,
            ),
        )

        if commit:

            self.connection.commit()

            self.statistics[
                "commits"
            ] += 1


# ==========================================================
# save_wallets()
# ==========================================================

def save_wallets(
    self,
    wallets: List[WalletRecord],
    *,
    validate: bool = True,
    overwrite: bool = True,
    batch_size: Optional[int] = None,
    commit: bool = True,
) -> int:
    """
    Persist multiple wallets using bulk UPSERT.

    Features
    --------
    • Transaction batching
    • executemany() bulk insert
    • Validation
    • Cache synchronization
    • Automatic timestamps
    • Statistics update
    • Rollback on failure

    Parameters
    ----------
    wallets
        Wallets to save.

    validate
        Validate every wallet.

    overwrite
        Ignore existing wallets if False.

    batch_size
        Number of rows per transaction.

    commit
        Commit after all batches.

    Returns
    -------
    int
        Number of wallets written.
    """

    if self.connection is None:

        raise RuntimeError(
            "Database not connected."
        )

    if not wallets:

        return 0

    if batch_size is None:

        batch_size = (
            self.config.batch_size
        )

    written = 0

    now = datetime.utcnow()

    sql = """
    INSERT INTO wallets (

        address,

        label,

        risk_score,

        confidence,

        balance_sol,

        first_seen,

        last_seen,

        tags,

        metadata

    )

    VALUES (

        ?,?,?,?,?,?,?,?,?

    )

    ON CONFLICT(address)

    DO UPDATE SET

        label=excluded.label,

        risk_score=excluded.risk_score,

        confidence=excluded.confidence,

        balance_sol=excluded.balance_sol,

        last_seen=excluded.last_seen,

        tags=excluded.tags,

        metadata=excluded.metadata
    """

    try:

        self.cursor.execute(
            "BEGIN TRANSACTION"
        )

        # =====================================
        # Process batches
        # =====================================

        for i in range(
            0,
            len(wallets),
            batch_size,
        ):

            batch = wallets[
                i:i + batch_size
            ]

            rows = []

            for wallet in batch:

                if validate:

                    self.validate_wallet(
                        wallet.address
                    )

                if (

                    not overwrite

                    and

                    self.wallet_exists(
                        wallet.address
                    )

                ):

                    continue

                if wallet.first_seen is None:

                    wallet.first_seen = now

                wallet.last_seen = now

                rows.append(

                    (

                        wallet.address,

                        wallet.label.value,

                        wallet.risk_score,

                        wallet.confidence,

                        wallet.balance_sol,

                        wallet.first_seen,

                        wallet.last_seen,

                        json.dumps(
                            wallet.tags,
                            ensure_ascii=False,
                        ),

                        json.dumps(
                            wallet.metadata,
                            ensure_ascii=False,
                            default=str,
                        ),

                    )

                )

            if not rows:

                continue

            self.cursor.executemany(
                sql,
                rows,
            )

            written += len(rows)

            # ----------------------------
            # Cache synchronization
            # ----------------------------

            for wallet in batch:

                self.wallet_cache[
                    wallet.address
                ] = wallet

                if (

                    self.config.enable_cache

                ):

                    self.cache_expiry[
                        wallet.address
                    ] = (

                        time.time()

                        +

                        self.config.cache_ttl

                    )

        # =====================================

        if commit:

            self.connection.commit()

            self.statistics[
                "commits"
            ] += 1

        self.statistics[
            "writes"
        ] += written

        self.statistics[
            "wallets"
        ] = max(

            self.statistics[
                "wallets"
            ],

            len(
                self.wallet_cache
            ),

        )

        self.statistics[
            "cache_entries"
        ] = len(
            self.wallet_cache
        )

        self.statistics[
            "last_commit"
        ] = datetime.utcnow()

        self.logger.info(

            "Saved %d wallets.",

            written,

        )

        return written

    except Exception as exc:

        self.connection.rollback()

        self.logger.exception(

            "Bulk wallet save failed."

        )

        raise RuntimeError(

            "save_wallets() failed"

        ) from exc

# ==========================================================
# load_wallet()
# ==========================================================

def load_wallet(
    self,
    address: WalletAddress,
    *,
    use_cache: bool = True,
    refresh_cache: bool = True,
) -> Optional[WalletRecord]:
    """
    Load a wallet from the database.

    Features
    --------
    • Cache-first lookup
    • Automatic cache expiration
    • SQLite row -> WalletRecord conversion
    • Statistics tracking
    • Safe deserialization

    Parameters
    ----------
    address
        Solana wallet address.

    use_cache
        Check in-memory cache first.

    refresh_cache
        Cache the wallet after DB lookup.

    Returns
    -------
    WalletRecord | None
    """

    if self.connection is None:

        raise RuntimeError(
            "Database is not connected."
        )

    # --------------------------------------------------
    # Validate address
    # --------------------------------------------------

    self.validate_wallet(
        address
    )

    now = time.time()

    # --------------------------------------------------
    # Cache Lookup
    # --------------------------------------------------

    if (

        use_cache

        and

        self.config.enable_cache

    ):

        cached = self.wallet_cache.get(
            address
        )

        expiry = self.cache_expiry.get(
            address,
            0,
        )

        if (

            cached is not None

            and

            expiry > now

        ):

            self.statistics[
                "cache_hits"
            ] += 1

            self.statistics[
                "reads"
            ] += 1

            return cached

        if cached is not None:

            self.wallet_cache.pop(
                address,
                None,
            )

            self.cache_expiry.pop(
                address,
                None,
            )

    self.statistics[
        "cache_misses"
    ] += 1

    # --------------------------------------------------
    # Database Query
    # --------------------------------------------------

    row = self.cursor.execute(
        """
        SELECT *

        FROM wallets

        WHERE address = ?

        LIMIT 1
        """,
        (
            address,
        ),
    ).fetchone()

    if row is None:

        self.statistics[
            "reads"
        ] += 1

        return None

    # --------------------------------------------------
    # Deserialize
    # --------------------------------------------------

    wallet = WalletRecord(

        address=row["address"],

        label=WalletLabel(
            row["label"]
        ),

        risk_score=float(
            row["risk_score"]
        ),

        confidence=float(
            row["confidence"]
        ),

        balance_sol=float(
            row["balance_sol"]
        ),

        first_seen=(

            datetime.fromisoformat(
                row["first_seen"]
            )

            if row["first_seen"]

            else None

        ),

        last_seen=(

            datetime.fromisoformat(
                row["last_seen"]
            )

            if row["last_seen"]

            else None

        ),

        tags=(

            json.loads(
                row["tags"]
            )

            if row["tags"]

            else []

        ),

        metadata=(

            json.loads(
                row["metadata"]
            )

            if row["metadata"]

            else {}

        ),

    )

    # --------------------------------------------------
    # Refresh Cache
    # --------------------------------------------------

    if (

        refresh_cache

        and

        self.config.enable_cache

    ):

        self.wallet_cache[
            address
        ] = wallet

        self.cache_expiry[
            address
        ] = (

            now

            +

            self.config.cache_ttl

        )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    self.statistics[
        "reads"
    ] += 1

    self.statistics[
        "cache_entries"
    ] = len(
        self.wallet_cache
    )

    self.logger.debug(

        "Loaded wallet %s",

        address,

    )

    return wallet

# ==========================================================
# load_wallets()
# ==========================================================

def load_wallets(
    self,
    addresses: List[WalletAddress],
    *,
    use_cache: bool = True,
    refresh_cache: bool = True,
    batch_size: Optional[int] = None,
) -> Dict[
    WalletAddress,
    WalletRecord,
]:
    """
    Bulk load wallets.

    Features
    --------
    • Cache-first loading
    • Automatic batching
    • Single SQL query per batch
    • Automatic cache update
    • Statistics tracking

    Parameters
    ----------
    addresses
        Wallet addresses.

    use_cache
        Use in-memory cache.

    refresh_cache
        Refresh cache after DB lookup.

    batch_size
        Number of addresses per SQL query.

    Returns
    -------
    Dict[address, WalletRecord]
    """

    if self.connection is None:

        raise RuntimeError(
            "Database not connected."
        )

    if not addresses:

        return {}

    if batch_size is None:

        batch_size = (
            self.config.batch_size
        )

    result: Dict[
        WalletAddress,
        WalletRecord,
    ] = {}

    missing: List[
        WalletAddress
    ] = []

    now = time.time()

    # ======================================================
    # Cache Lookup
    # ======================================================

    if (

        use_cache

        and

        self.config.enable_cache

    ):

        for address in addresses:

            cached = self.wallet_cache.get(
                address
            )

            expiry = self.cache_expiry.get(
                address,
                0,
            )

            if (

                cached is not None

                and

                expiry > now

            ):

                result[
                    address
                ] = cached

                self.statistics[
                    "cache_hits"
                ] += 1

            else:

                missing.append(
                    address
                )

                if cached is not None:

                    self.wallet_cache.pop(
                        address,
                        None,
                    )

                    self.cache_expiry.pop(
                        address,
                        None,
                    )

    else:

        missing = list(
            addresses
        )

    self.statistics[
        "cache_misses"
    ] += len(
        missing
    )

    # ======================================================
    # Database Lookup
    # ======================================================

    for start in range(
        0,
        len(missing),
        batch_size,
    ):

        batch = missing[
            start:start + batch_size
        ]

        if not batch:

            continue

        placeholders = ",".join(

            "?"

            for _ in batch

        )

        sql = f"""
        SELECT *

        FROM wallets

        WHERE address IN (
            {placeholders}
        )
        """

        rows = self.cursor.execute(
            sql,
            tuple(batch),
        ).fetchall()

        for row in rows:

            wallet = WalletRecord(

                address=row["address"],

                label=WalletLabel(
                    row["label"]
                ),

                risk_score=float(
                    row["risk_score"]
                ),

                confidence=float(
                    row["confidence"]
                ),

                balance_sol=float(
                    row["balance_sol"]
                ),

                first_seen=(

                    datetime.fromisoformat(
                        row["first_seen"]
                    )

                    if row["first_seen"]

                    else None

                ),

                last_seen=(

                    datetime.fromisoformat(
                        row["last_seen"]
                    )

                    if row["last_seen"]

                    else None

                ),

                tags=(

                    json.loads(
                        row["tags"]
                    )

                    if row["tags"]

                    else []

                ),

                metadata=(

                    json.loads(
                        row["metadata"]
                    )

                    if row["metadata"]

                    else {}

                ),

            )

            result[
                wallet.address
            ] = wallet

            # ------------------------------------------
            # Cache Refresh
            # ------------------------------------------

            if (

                refresh_cache

                and

                self.config.enable_cache

            ):

                self.wallet_cache[
                    wallet.address
                ] = wallet

                self.cache_expiry[
                    wallet.address
                ] = (

                    now

                    +

                    self.config.cache_ttl

                )

    # ======================================================
    # Statistics
    # ======================================================

    self.statistics[
        "reads"
    ] += len(
        addresses
    )

    self.statistics[
        "cache_entries"
    ] = len(
        self.wallet_cache
    )

    self.logger.debug(

        "Loaded %d/%d wallets.",

        len(result),

        len(addresses),

    )

    return result

# ==========================================================
# load_or_create_wallet()
# ==========================================================

def load_or_create_wallet(
    self,
    address: WalletAddress,
    *,
    label: WalletLabel = WalletLabel.UNKNOWN,
    balance_sol: float = 0.0,
    metadata: Optional[JSONDict] = None,
    tags: Optional[List[str]] = None,
    validate: bool = True,
    touch: bool = True,
) -> WalletRecord:
    """
    Load a wallet if it exists, otherwise create it.

    This is one of the most frequently used helpers
    throughout Sentinel AI because almost every engine
    encounters wallets that may or may not already
    exist in persistent storage.

    Features
    --------
    • Cache-first lookup
    • Optional validation
    • Automatic wallet creation
    • Cache synchronization
    • Optional touch(last_seen)
    • Statistics updates

    Parameters
    ----------
    address
        Solana wallet address.

    label
        Initial wallet label if created.

    balance_sol
        Initial balance.

    metadata
        Initial metadata.

    tags
        Initial tags.

    validate
        Validate Solana address.

    touch
        Update last_seen if wallet already exists.

    Returns
    -------
    WalletRecord
    """

    if validate:

        self.validate_wallet(
            address
        )

    # --------------------------------------------------
    # Existing wallet?
    # --------------------------------------------------

    wallet = self.load_wallet(
        address
    )

    if wallet is not None:

        if touch:

            self.touch_wallet(
                address
            )

            wallet.last_seen = (
                datetime.utcnow()
            )

        return wallet

    # --------------------------------------------------
    # Create new wallet
    # --------------------------------------------------

    now = datetime.utcnow()

    wallet = WalletRecord(

        address=address,

        label=label,

        risk_score=0.0,

        confidence=1.0,

        balance_sol=balance_sol,

        first_seen=now,

        last_seen=now,

        tags=tags or [],

        metadata=metadata or {},

    )

    self.save_wallet(
        wallet
    )

    self.logger.debug(

        "Created wallet %s",

        address,

    )

    return wallet

# ==========================================================
# wallet_exists()
# ==========================================================

def wallet_exists(
    self,
    address: WalletAddress,
    *,
    use_cache: bool = True,
    validate: bool = True,
) -> bool:
    """
    Determine whether a wallet exists.

    Features
    --------
    • Optional Solana address validation
    • Cache-first lookup
    • Fast SQL EXISTS query
    • Statistics tracking

    Parameters
    ----------
    address
        Solana wallet address.

    use_cache
        Check memory cache first.

    validate
        Validate address before lookup.

    Returns
    -------
    bool
    """

    if self.connection is None:

        raise RuntimeError(
            "Database is not connected."
        )

    # --------------------------------------------------
    # Validate address
    # --------------------------------------------------

    if validate:

        self.validate_wallet(
            address
        )

    # --------------------------------------------------
    # Cache Lookup
    # --------------------------------------------------

    if (

        use_cache

        and

        self.config.enable_cache

    ):

        if address in self.wallet_cache:

            expiry = self.cache_expiry.get(
                address,
                0,
            )

            if expiry > time.time():

                self.statistics[
                    "cache_hits"
                ] += 1

                return True

            # Cache expired

            self.wallet_cache.pop(
                address,
                None,
            )

            self.cache_expiry.pop(
                address,
                None,
            )

        self.statistics[
            "cache_misses"
        ] += 1

    # --------------------------------------------------
    # Database Lookup
    # --------------------------------------------------

    row = self.cursor.execute(
        """
        SELECT EXISTS(

            SELECT 1

            FROM wallets

            WHERE address = ?

        )
        """,
        (
            address,
        ),
    ).fetchone()

    exists = bool(

        row[0]

        if row is not None

        else False

    )

    self.statistics[
        "reads"
    ] += 1

    self.logger.debug(

        "Wallet exists (%s): %s",

        address,

        exists,

    )

    return exists            

# ==========================================================
# wallet_count()
# ==========================================================

def wallet_count(
    self,
    *,
    label: Optional[
        WalletLabel
    ] = None,
    min_risk: Optional[
        float
    ] = None,
    max_risk: Optional[
        float
    ] = None,
    active_since: Optional[
        datetime
    ] = None,
    use_cache: bool = True,
) -> int:
    """
    Count wallets matching optional filters.

    Features
    --------
    • Count all wallets
    • Count by label
    • Count by risk score
    • Count by activity
    • Cached results
    • Statistics tracking

    Parameters
    ----------
    label
        Wallet label filter.

    min_risk
        Minimum risk score.

    max_risk
        Maximum risk score.

    active_since
        Count wallets active after this time.

    use_cache
        Use cached counts.

    Returns
    -------
    int
    """

    if self.connection is None:

        raise RuntimeError(
            "Database not connected."
        )

    # --------------------------------------------------
    # Cache Key
    # --------------------------------------------------

    cache_key = hashlib.sha256(

        json.dumps(

            {

                "label":
                    label.value
                    if label
                    else None,

                "min":
                    min_risk,

                "max":
                    max_risk,

                "active":
                    active_since.isoformat()
                    if active_since
                    else None,

            },

            sort_keys=True,

        ).encode()

    ).hexdigest()

    if (

        use_cache

        and

        self.config.enable_cache

    ):

        cached = self.generic_cache.get(
            cache_key
        )

        if (

            cached

            and

            cached.expires_at

            >

            time.time()

        ):

            self.statistics[
                "cache_hits"
            ] += 1

            return int(
                cached.value
            )

        self.statistics[
            "cache_misses"
        ] += 1

    # --------------------------------------------------
    # Build SQL
    # --------------------------------------------------

    sql = """
    SELECT COUNT(*)

    FROM wallets

    WHERE 1=1
    """

    params = []

    if label is not None:

        sql += """
        AND label = ?
        """

        params.append(
            label.value
        )

    if min_risk is not None:

        sql += """
        AND risk_score >= ?
        """

        params.append(
            min_risk
        )

    if max_risk is not None:

        sql += """
        AND risk_score <= ?
        """

        params.append(
            max_risk
        )

    if active_since is not None:

        sql += """
        AND last_seen >= ?
        """

        params.append(
            active_since.isoformat()
        )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    row = self.cursor.execute(

        sql,

        tuple(params),

    ).fetchone()

    count = int(
        row[0]
    )

    # --------------------------------------------------
    # Cache Result
    # --------------------------------------------------

    if self.config.enable_cache:

        self.generic_cache[
            cache_key
        ] = CacheRecord(

            key=cache_key,

            value=count,

            created_at=time.time(),

            expires_at=(

                time.time()

                +

                self.config.cache_ttl

            ),

        )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    self.statistics[
        "reads"
    ] += 1

    self.logger.debug(

        "Wallet count = %d",

        count,

    )

    return count            
