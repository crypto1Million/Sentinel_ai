# ==========================================================
# Part 1
# Imports
# Constants
# Enums
# Type Aliases
# FetchMode
# TransactionRecord
# FetchResult
# FetchConfig
# ==========================================================

from __future__ import annotations

import asyncio
import hashlib
import logging
import statistics
import time

from dataclasses import (
    dataclass,
    field,
)

from datetime import datetime

from enum import Enum

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    TypeAlias,
)

from collections import defaultdict

# ==========================================================
# Internal Imports
# ==========================================================

from sentinel.blockchain.helius_client import (
    HeliusClient,
    HeliusResponse,
)

# ==========================================================
# Constants
# ==========================================================

DEFAULT_HISTORY_LIMIT = 1000

DEFAULT_BATCH_SIZE = 100

DEFAULT_PARALLEL_DOWNLOADS = 20

DEFAULT_CACHE_TTL = 600

DEFAULT_MAX_DEPTH = 5

DEFAULT_TIMEOUT = 30

DEFAULT_RETRY_COUNT = 5

DEFAULT_CHUNK_SIZE = 250

DEFAULT_SAVE_INTERVAL = 500

# ==========================================================
# Enums
# ==========================================================

class FetchMode(Enum):
    """
    Transaction fetching mode.
    """

    RECENT = "recent"

    FULL = "full"

    INCREMENTAL = "incremental"

    RECURSIVE = "recursive"

    TOKEN = "token"

    SOL = "sol"


class TransactionType(Enum):

    UNKNOWN = "unknown"

    SOL_TRANSFER = "sol_transfer"

    TOKEN_TRANSFER = "token_transfer"

    NFT_TRANSFER = "nft_transfer"

    SWAP = "swap"

    LIQUIDITY = "liquidity"

    STAKE = "stake"

    UNSTAKE = "unstake"

    MINT = "mint"

    BURN = "burn"


class FetchStatus(Enum):

    SUCCESS = "success"

    PARTIAL = "partial"

    FAILED = "failed"


# ==========================================================
# Type Aliases
# ==========================================================

WalletAddress: TypeAlias = str

Signature: TypeAlias = str

Slot: TypeAlias = int

Timestamp: TypeAlias = int

ProgramID: TypeAlias = str

TokenMint: TypeAlias = str

JSONDict: TypeAlias = Dict[str, Any]

# ==========================================================
# Transaction Record
# ==========================================================

@dataclass(slots=True)
class TransactionRecord:
    """
    Canonical transaction model used
    throughout Sentinel AI.
    """

    signature: Signature

    slot: Slot

    block_time: Optional[
        Timestamp
    ] = None

    transaction_type: TransactionType = (
        TransactionType.UNKNOWN
    )

    success: bool = True

    fee: int = 0

    wallets: List[
        WalletAddress
    ] = field(
        default_factory=list
    )

    signers: List[
        WalletAddress
    ] = field(
        default_factory=list
    )

    programs: List[
        ProgramID
    ] = field(
        default_factory=list
    )

    token_transfers: List[
        JSONDict
    ] = field(
        default_factory=list
    )

    sol_transfers: List[
        JSONDict
    ] = field(
        default_factory=list
    )

    instructions: List[
        JSONDict
    ] = field(
        default_factory=list
    )

    logs: List[
        str
    ] = field(
        default_factory=list
    )

    risk_flags: List[
        str
    ] = field(
        default_factory=list
    )

    metadata: JSONDict = field(
        default_factory=dict
    )

    raw: Optional[
        JSONDict
    ] = None


# ==========================================================
# Fetch Result
# ==========================================================

@dataclass(slots=True)
class FetchResult:
    """
    Result returned after a fetch job.
    """

    wallet: WalletAddress

    mode: FetchMode

    status: FetchStatus

    transactions: List[
        TransactionRecord
    ] = field(
        default_factory=list
    )

    signatures_downloaded: int = 0

    transactions_downloaded: int = 0

    failed_downloads: int = 0

    cache_hits: int = 0

    cache_misses: int = 0

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    finished_at: Optional[
        datetime
    ] = None

    metadata: JSONDict = field(
        default_factory=dict
    )

    @property
    def duration(self) -> float:

        if self.finished_at is None:

            return 0.0

        return (

            self.finished_at

            -

            self.started_at

        ).total_seconds()


# ==========================================================
# Fetch Configuration
# ==========================================================

@dataclass(slots=True)
class FetchConfig:
    """
    TransactionFetcher configuration.
    """

    mode: FetchMode = (
        FetchMode.FULL
    )

    history_limit: int = (
        DEFAULT_HISTORY_LIMIT
    )

    batch_size: int = (
        DEFAULT_BATCH_SIZE
    )

    chunk_size: int = (
        DEFAULT_CHUNK_SIZE
    )

    parallel_downloads: int = (
        DEFAULT_PARALLEL_DOWNLOADS
    )

    cache_ttl: int = (
        DEFAULT_CACHE_TTL
    )

    timeout: int = (
        DEFAULT_TIMEOUT
    )

    retry_count: int = (
        DEFAULT_RETRY_COUNT
    )

    recursive_depth: int = (
        DEFAULT_MAX_DEPTH
    )

    save_interval: int = (
        DEFAULT_SAVE_INTERVAL
    )

    normalize: bool = True

    enrich: bool = True

    deduplicate: bool = True

    save_to_database: bool = True

    update_cache: bool = True  

# ==========================================================
# Part 2
# Initialization
# Cache
# Statistics
# Internal Storage
# ==========================================================

class TransactionFetcher:
    """
    Downloads, normalizes and caches
    Solana transaction history.

    This class sits directly above
    HeliusClient and provides a unified
    history source for every Sentinel AI
    analytics engine.
    """

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------

    def __init__(
        self,
        helius: HeliusClient,
        config: Optional[
            FetchConfig
        ] = None,
    ) -> None:

        self.helius = helius

        self.config = (
            config
            or FetchConfig()
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        # --------------------------------------------------
        # Transaction Cache
        # signature -> TransactionRecord
        # --------------------------------------------------

        self.transaction_cache: Dict[
            Signature,
            TransactionRecord,
        ] = {}

        # --------------------------------------------------
        # Wallet History Cache
        # wallet -> List[Signature]
        # --------------------------------------------------

        self.wallet_cache: Dict[
            WalletAddress,
            List[Signature],
        ] = {}

        # --------------------------------------------------
        # Cache Expiration
        # --------------------------------------------------

        self.cache_expiry: Dict[
            str,
            float,
        ] = {}

        # --------------------------------------------------
        # Recently Downloaded Signatures
        # --------------------------------------------------

        self.downloaded_signatures: Set[
            Signature
        ] = set()

        # --------------------------------------------------
        # Internal Storage
        # --------------------------------------------------

        self.transactions: Dict[
            Signature,
            TransactionRecord,
        ] = {}

        self.wallet_histories: Dict[
            WalletAddress,
            List[TransactionRecord],
        ] = defaultdict(list)

        self.failed_transactions: Dict[
            Signature,
            str,
        ] = {}

        self.pending_downloads: Set[
            Signature
        ] = set()

        self.program_index: Dict[
            ProgramID,
            Set[Signature],
        ] = defaultdict(set)

        self.token_index: Dict[
            TokenMint,
            Set[Signature],
        ] = defaultdict(set)

        self.wallet_index: Dict[
            WalletAddress,
            Set[Signature],
        ] = defaultdict(set)

        # --------------------------------------------------
        # Performance Statistics
        # --------------------------------------------------

        self.statistics: Dict[
            str,
            Any,
        ] = {

            # download

            "wallet_fetches": 0,

            "history_fetches": 0,

            "transactions_downloaded": 0,

            "failed_downloads": 0,

            "retry_count": 0,

            # cache

            "cache_hits": 0,

            "cache_misses": 0,

            "cache_writes": 0,

            "cache_evictions": 0,

            # normalization

            "normalized": 0,

            "enriched": 0,

            "duplicates_removed": 0,

            # storage

            "wallets_cached": 0,

            "transactions_cached": 0,

            # timing

            "start_time": time.time(),

            "last_fetch": None,

            "last_refresh": None,

        }

        # --------------------------------------------------
        # Runtime Metrics
        # --------------------------------------------------

        self._request_times: List[
            float
        ] = []

        self._download_times: List[
            float
        ] = []

        self._normalization_times: List[
            float
        ] = []

        self._cache_access_times: List[
            float
        ] = []

        self.logger.info(
            "TransactionFetcher initialized."
        )

    # ======================================================
    # Internal Helpers
    # ======================================================

    def _cache_key(
        self,
        *parts: Any,
    ) -> str:
        """
        Generate deterministic cache key.
        """

        raw = "|".join(
            map(str, parts)
        )

        return hashlib.sha256(
            raw.encode()
        ).hexdigest()

    # ------------------------------------------------------

    def _cache_valid(
        self,
        key: str,
    ) -> bool:
        """
        Returns True if cache entry
        is still valid.
        """

        expiry = self.cache_expiry.get(
            key
        )

        if expiry is None:

            return False

        return expiry > time.time()

    # ------------------------------------------------------

    def _touch_cache(
        self,
        key: str,
    ) -> None:
        """
        Refresh cache expiry.
        """

        self.cache_expiry[key] = (

            time.time()

            +

            self.config.cache_ttl

        )

    # ------------------------------------------------------

    def _record_download_time(
        self,
        elapsed: float,
    ) -> None:

        self._download_times.append(
            elapsed
        )

    # ------------------------------------------------------

    def _record_normalization_time(
        self,
        elapsed: float,
    ) -> None:

        self._normalization_times.append(
            elapsed
        )

# ==========================================================
# Part 3
# Wallet History
# ==========================================================

def fetch_wallet_history(
    self,
    wallet: WalletAddress,
    *,
    mode: Optional[
        FetchMode
    ] = None,
    limit: Optional[int] = None,
) -> FetchResult:
    """
    Primary wallet history entry point.

    Dispatches to the appropriate
    fetching strategy.
    """

    mode = mode or self.config.mode

    if mode == FetchMode.RECENT:

        return self.fetch_recent_history(
            wallet,
            limit=limit,
        )

    if mode == FetchMode.FULL:

        return self.fetch_full_history(
            wallet,
            limit=limit,
        )

    if mode == FetchMode.INCREMENTAL:

        return self.fetch_recent_history(
            wallet,
            limit=limit,
        )

    raise ValueError(
        f"Unsupported fetch mode: {mode}"
    )


# ==========================================================


def fetch_recent_history(
    self,
    wallet: WalletAddress,
    *,
    limit: Optional[int] = None,
) -> FetchResult:
    """
    Download only the newest transactions.
    """

    start = time.perf_counter()

    limit = (
        limit
        or self.config.history_limit
    )

    history = self.helius.get_wallet_history(

        wallet,

        limit=limit,

    )

    result = FetchResult(

        wallet=wallet,

        mode=FetchMode.RECENT,

        status=FetchStatus.SUCCESS,

    )

    for tx in history:

        normalized = self.normalize_transaction(
            tx
        )

        result.transactions.append(
            normalized
        )

        self.transactions[
            normalized.signature
        ] = normalized

        self.wallet_histories[
            wallet
        ].append(
            normalized
        )

    result.transactions_downloaded = (
        len(result.transactions)
    )

    result.signatures_downloaded = (
        len(result.transactions)
    )

    result.finished_at = (
        datetime.utcnow()
    )

    self.statistics[
        "wallet_fetches"
    ] += 1

    self.statistics[
        "history_fetches"
    ] += 1

    self.statistics[
        "transactions_downloaded"
    ] += len(
        result.transactions
    )

    self.statistics[
        "last_fetch"
    ] = datetime.utcnow()

    self._record_download_time(

        time.perf_counter()
        - start

    )

    return result


# ==========================================================


def fetch_full_history(
    self,
    wallet: WalletAddress,
    *,
    limit: Optional[int] = None,
) -> FetchResult:
    """
    Download the complete transaction
    history using pagination.
    """

    limit = (
        limit
        or self.config.history_limit
    )

    result = FetchResult(

        wallet=wallet,

        mode=FetchMode.FULL,

        status=FetchStatus.SUCCESS,

    )

    before = None

    while True:

        signatures = self.helius.get_signatures(

            wallet,

            limit=min(
                limit,
                self.config.batch_size,
            ),

            before=before,

        )

        if (

            not signatures.success

            or

            not signatures.result

        ):

            break

        for item in signatures.result:

            signature = item.get(
                "signature"
            )

            if not signature:
                continue

            tx = self.helius.get_enriched_transaction(
                signature
            )

            normalized = self.normalize_transaction(
                tx
            )

            result.transactions.append(
                normalized
            )

            self.transactions[
                normalized.signature
            ] = normalized

            self.wallet_histories[
                wallet
            ].append(
                normalized
            )

        before = signatures.result[-1][
            "signature"
        ]

        if (

            len(result.transactions)

            >= limit

        ):

            break

        if (

            len(signatures.result)

            < self.config.batch_size

        ):

            break

    result.transactions_downloaded = (
        len(result.transactions)
    )

    result.signatures_downloaded = (
        len(result.transactions)
    )

    result.finished_at = (
        datetime.utcnow()
    )

    return result


# ==========================================================


def fetch_history_until(
    self,
    wallet: WalletAddress,
    until_signature: Signature,
    *,
    batch_size: Optional[int] = None,
) -> FetchResult:
    """
    Download history until reaching
    a known transaction signature.

    Used for incremental syncing.
    """

    batch_size = (

        batch_size

        or

        self.config.batch_size

    )

    result = FetchResult(

        wallet=wallet,

        mode=FetchMode.INCREMENTAL,

        status=FetchStatus.SUCCESS,

    )

    before = None

    stop = False

    while not stop:

        response = self.helius.get_signatures(

            wallet,

            limit=batch_size,

            before=before,

        )

        if (

            not response.success

            or

            not response.result

        ):

            break

        for item in response.result:

            signature = item.get(
                "signature"
            )

            if signature == until_signature:

                stop = True

                break

            tx = self.helius.get_enriched_transaction(
                signature
            )

            normalized = self.normalize_transaction(
                tx
            )

            result.transactions.append(
                normalized
            )

            self.transactions[
                normalized.signature
            ] = normalized

            self.wallet_histories[
                wallet
            ].append(
                normalized
            )

        if stop:

            break

        before = response.result[-1][
            "signature"
        ]

    result.transactions_downloaded = (
        len(result.transactions)
    )

    result.signatures_downloaded = (
        len(result.transactions)
    )

    result.finished_at = (
        datetime.utcnow()
    )

    return result

# ==========================================================
# Part 4
# Transaction Download
# ==========================================================

def fetch_transaction(
    self,
    signature: Signature,
    *,
    use_cache: bool = True,
) -> TransactionRecord:
    """
    Download a single transaction.

    Automatically uses cache when enabled.
    """

    cache_key = self._cache_key(
        "tx",
        signature,
    )

    # --------------------------------------------------
    # Cache
    # --------------------------------------------------

    if (

        use_cache

        and

        self._cache_valid(cache_key)

        and

        signature in self.transaction_cache

    ):

        self.statistics[
            "cache_hits"
        ] += 1

        return self.transaction_cache[
            signature
        ]

    self.statistics[
        "cache_misses"
    ] += 1

    start = time.perf_counter()

    tx = self.helius.get_enriched_transaction(
        signature
    )

    record = self.normalize_transaction(
        tx
    )

    if self.config.enrich:

        record = self.enrich_transaction(
            record
        )

    self.transaction_cache[
        signature
    ] = record

    self.transactions[
        signature
    ] = record

    self._touch_cache(
        cache_key
    )

    self.statistics[
        "transactions_downloaded"
    ] += 1

    self.statistics[
        "cache_writes"
    ] += 1

    self._record_download_time(

        time.perf_counter()

        - start

    )

    return record


# ==========================================================


def fetch_transactions(
    self,
    signatures: List[
        Signature
    ],
    *,
    use_cache: bool = True,
) -> List[
    TransactionRecord
]:
    """
    Download multiple transactions.
    """

    records: List[
        TransactionRecord
    ] = []

    for signature in signatures:

        try:

            records.append(

                self.fetch_transaction(

                    signature,

                    use_cache=use_cache,

                )

            )

        except Exception as exc:

            self.failed_transactions[
                signature
            ] = str(exc)

            self.statistics[
                "failed_downloads"
            ] += 1

    return records


# ==========================================================


def batch_download(
    self,
    signatures: List[
        Signature
    ],
    *,
    batch_size: Optional[
        int
    ] = None,
) -> List[
    TransactionRecord
]:
    """
    Download transactions using
    batched Helius RPC requests.
    """

    batch_size = (

        batch_size

        or

        self.config.batch_size

    )

    records: List[
        TransactionRecord
    ] = []

    for i in range(

        0,

        len(signatures),

        batch_size,

    ):

        chunk = signatures[
            i:i + batch_size
        ]

        responses = (

            self.helius.get_transactions(
                chunk
            )

        )

        for response in responses:

            try:

                if not response.success:

                    self.statistics[
                        "failed_downloads"
                    ] += 1

                    continue

                normalized = (

                    self.normalize_transaction(

                        response.result

                    )

                )

                if self.config.enrich:

                    normalized = (

                        self.enrich_transaction(

                            normalized

                        )

                    )

                records.append(
                    normalized
                )

                self.transactions[
                    normalized.signature
                ] = normalized

            except Exception:

                self.statistics[
                    "failed_downloads"
                ] += 1

    return records


# ==========================================================


async def parallel_download(
    self,
    signatures: List[
        Signature
    ],
    *,
    workers: Optional[
        int
    ] = None,
) -> List[
    TransactionRecord
]:
    """
    Download many transactions
    concurrently.

    Used for very large wallets.
    """

    workers = (

        workers

        or

        self.config.parallel_downloads

    )

    semaphore = asyncio.Semaphore(
        workers
    )

    async def worker(
        signature: Signature,
    ) -> Optional[
        TransactionRecord
    ]:

        async with semaphore:

            try:

                tx = await asyncio.to_thread(

                    self.fetch_transaction,

                    signature,

                )

                return tx

            except Exception as exc:

                self.failed_transactions[
                    signature
                ] = str(exc)

                self.statistics[
                    "failed_downloads"
                ] += 1

                return None

    results = await asyncio.gather(

        *(

            worker(sig)

            for sig in signatures

        )

    )

    return [

        tx

        for tx in results

        if tx is not None

    ]

# ==========================================================
# Part 5
# Normalization
# ==========================================================

def normalize_transaction(
    self,
    tx: Dict[str, Any],
) -> TransactionRecord:
    """
    Convert an enriched Helius transaction into the
    canonical TransactionRecord used throughout
    Sentinel AI.
    """

    start = time.perf_counter()

    programs = []

    for instruction in tx.get(
        "instructions",
        [],
    ):

        program = instruction.get(
            "programId"
        )

        if program:

            programs.append(
                program
            )

    accounts = self.normalize_accounts(
        tx
    )

    record = TransactionRecord(

        signature=tx.get(
            "signature",
            "",
        ),

        slot=tx.get(
            "slot",
            0,
        ),

        block_time=tx.get(
            "block_time"
        ),

        success=(
            tx.get(
                "status",
                "success",
            )
            == "success"
        ),

        fee=tx.get(
            "fee",
            0,
        ),

        wallets=accounts,

        signers=[

            signer.get("pubkey")

            if isinstance(
                signer,
                dict,
            )

            else signer

            for signer in tx.get(
                "signers",
                [],
            )

        ],

        programs=programs,

        token_transfers=[

            self.normalize_token_transfer(
                transfer
            )

            for transfer

            in tx.get(
                "token_transfers",
                [],
            )

        ],

        sol_transfers=[

            self.normalize_sol_transfer(
                transfer
            )

            for transfer

            in tx.get(
                "sol_transfers",
                [],
            )

        ],

        instructions=[

            self.normalize_instruction(
                instruction
            )

            for instruction

            in tx.get(
                "instructions",
                [],
            )

        ],

        logs=tx.get(
            "log_messages",
            [],
        ),

        metadata={

            "compute_units":

                tx.get(
                    "compute_units"
                ),

            "version":

                tx.get(
                    "version"
                ),

        },

        raw=tx,

    )

    self.statistics[
        "normalized"
    ] += 1

    self._record_normalization_time(

        time.perf_counter()

        - start

    )

    return record


# ==========================================================


def normalize_instruction(
    self,
    instruction: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize a transaction instruction.
    """

    return {

        "program":

            instruction.get(
                "program"
            ),

        "program_id":

            instruction.get(
                "programId"
            ),

        "accounts":

            instruction.get(
                "accounts",
                [],
            ),

        "data":

            instruction.get(
                "data"
            ),

        "parsed":

            instruction.get(
                "parsed"
            ),

        "stack_height":

            instruction.get(
                "stackHeight"
            ),

    }


# ==========================================================


def normalize_token_transfer(
    self,
    transfer: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize an SPL token transfer.
    """

    return {

        "mint":

            transfer.get(
                "mint"
            ),

        "from":

            transfer.get(
                "fromUserAccount"
            ),

        "to":

            transfer.get(
                "toUserAccount"
            ),

        "authority":

            transfer.get(
                "authority"
            ),

        "amount":

            transfer.get(
                "tokenAmount"
            ),

        "decimals":

            transfer.get(
                "decimals"
            ),

        "token_standard":

            transfer.get(
                "tokenStandard"
            ),

    }


# ==========================================================


def normalize_sol_transfer(
    self,
    transfer: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize a native SOL transfer.
    """

    return {

        "from":

            transfer.get(
                "fromUserAccount"
            ),

        "to":

            transfer.get(
                "toUserAccount"
            ),

        "lamports":

            transfer.get(
                "amount",
                0,
            ),

        "sol":

            transfer.get(
                "amount",
                0,
            ) / 1_000_000_000,

    }


# ==========================================================


def normalize_accounts(
    self,
    tx: Dict[str, Any],
) -> List[WalletAddress]:
    """
    Normalize account list.

    Removes duplicates while preserving order.
    """

    normalized: List[
        WalletAddress
    ] = []

    seen: Set[
        WalletAddress
    ] = set()

    for account in tx.get(
        "accounts",
        [],
    ):

        if isinstance(
            account,
            dict,
        ):

            address = account.get(
                "pubkey"
            )

        else:

            address = account

        if (

            address

            and

            address not in seen

        ):

            normalized.append(
                address
            )

            seen.add(
                address
            )

    return normalized                    

# ==========================================================
# Part 6
# Enrichment
# ==========================================================

def enrich_transaction(
    self,
    record: TransactionRecord,
) -> TransactionRecord:
    """
    Enrich a normalized transaction with
    wallet labels, program names, token
    metadata and risk flags.
    """

    start = time.perf_counter()

    record.metadata["wallet_labels"] = (
        self.enrich_wallet_labels(record)
    )

    record.metadata["program_names"] = (
        self.enrich_program_names(record)
    )

    record.metadata["token_metadata"] = (
        self.enrich_token_metadata(record)
    )

    record.risk_flags = (
        self.enrich_risk_flags(record)
    )

    self.statistics["enriched"] += 1

    self._record_normalization_time(
        time.perf_counter() - start
    )

    return record


# ==========================================================


def enrich_wallet_labels(
    self,
    record: TransactionRecord,
) -> Dict[
    WalletAddress,
    str,
]:
    """
    Attach known wallet labels.

    Labels are resolved using the local
    wallet label database and Helius data.
    """

    labels = {}

    resolver = getattr(
        self,
        "wallet_label_resolver",
        None,
    )

    for wallet in record.wallets:

        label = "Unknown"

        if resolver:

            try:

                label = resolver.label(
                    wallet
                )

            except Exception:

                pass

        labels[wallet] = label

    return labels


# ==========================================================


def enrich_program_names(
    self,
    record: TransactionRecord,
) -> Dict[
    ProgramID,
    str,
]:
    """
    Convert program IDs into readable names.
    """

    names = {}

    resolver = getattr(
        self,
        "program_registry",
        None,
    )

    for program in record.programs:

        program_name = program

        if resolver:

            try:

                program_name = (
                    resolver.name(
                        program
                    )
                )

            except Exception:

                pass

        names[program] = program_name

    return names


# ==========================================================


def enrich_token_metadata(
    self,
    record: TransactionRecord,
) -> Dict[
    TokenMint,
    Dict[str, Any],
]:
    """
    Attach token metadata.

    Uses Helius DAS when metadata is
    not already cached.
    """

    metadata = {}

    for transfer in record.token_transfers:

        mint = transfer.get(
            "mint"
        )

        if not mint:
            continue

        if hasattr(
            self,
            "token_metadata_cache",
        ):

            cached = (
                self.token_metadata_cache.get(
                    mint
                )
            )

            if cached:

                metadata[mint] = cached

                continue

        try:

            asset = self.helius.get_asset(
                mint
            )

            if asset.success:

                result = asset.result

                info = {

                    "name":
                        result.get(
                            "content",
                            {}
                        )
                        .get(
                            "metadata",
                            {}
                        )
                        .get(
                            "name"
                        ),

                    "symbol":
                        result.get(
                            "content",
                            {}
                        )
                        .get(
                            "metadata",
                            {}
                        )
                        .get(
                            "symbol"
                        ),

                    "decimals":
                        result.get(
                            "token_info",
                            {}
                        )
                        .get(
                            "decimals"
                        ),

                }

                metadata[mint] = info

                if hasattr(
                    self,
                    "token_metadata_cache",
                ):

                    self.token_metadata_cache[
                        mint
                    ] = info

        except Exception:

            continue

    return metadata


# ==========================================================


def enrich_risk_flags(
    self,
    record: TransactionRecord,
) -> List[str]:
    """
    Generate transaction-level
    heuristic risk flags.
    """

    flags: List[str] = []

    # --------------------------------------

    if not record.success:

        flags.append(
            "FAILED_TRANSACTION"
        )

    # --------------------------------------

    if record.fee > 10_000_000:

        flags.append(
            "HIGH_FEE"
        )

    # --------------------------------------

    if len(
        record.token_transfers
    ) > 25:

        flags.append(
            "MASS_TOKEN_TRANSFER"
        )

    # --------------------------------------

    if len(
        record.sol_transfers
    ) > 25:

        flags.append(
            "MASS_SOL_TRANSFER"
        )

    # --------------------------------------

    if (

        len(record.programs)

        > 15

    ):

        flags.append(
            "HIGH_PROGRAM_COMPLEXITY"
        )

    # --------------------------------------

    if any(

        transfer.get(
            "amount",
            0,
        ) == 0

        for transfer

        in record.token_transfers

    ):

        flags.append(
            "ZERO_TOKEN_TRANSFER"
        )

    # --------------------------------------

    if (

        len(record.wallets)

        > 100

    ):

        flags.append(
            "VERY_LARGE_TRANSACTION"
        )

    # --------------------------------------

    return sorted(
        set(flags)
    )

# ==========================================================
# Part 8
# Deduplication
# ==========================================================

def remove_duplicates(
    self,
    transactions: List[
        TransactionRecord
    ],
) -> List[
    TransactionRecord
]:
    """
    Remove duplicate transactions.

    Signature is treated as the
    canonical unique identifier.
    """

    unique: Dict[
        Signature,
        TransactionRecord,
    ] = {}

    duplicates = 0

    for tx in transactions:

        if tx.signature in unique:

            duplicates += 1

            continue

        unique[
            tx.signature
        ] = tx

    self.statistics[
        "duplicates_removed"
    ] += duplicates

    return list(
        unique.values()
    )


# ==========================================================


def unique_signatures(
    self,
    transactions: List[
        TransactionRecord
    ],
) -> List[
    Signature
]:
    """
    Return unique transaction signatures
    while preserving order.
    """

    seen: Set[
        Signature
    ] = set()

    signatures: List[
        Signature
    ] = []

    for tx in transactions:

        if tx.signature in seen:

            continue

        seen.add(
            tx.signature
        )

        signatures.append(
            tx.signature
        )

    return signatures


# ==========================================================


def merge_histories(
    self,
    *histories: List[
        TransactionRecord
    ],
) -> List[
    TransactionRecord
]:
    """
    Merge multiple histories into
    one chronologically sorted history.

    Duplicate signatures are removed.
    """

    merged: List[
        TransactionRecord
    ] = []

    for history in histories:

        merged.extend(
            history
        )

    merged = self.remove_duplicates(
        merged
    )

    merged.sort(

        key=lambda tx: (

            tx.block_time

            if tx.block_time
            is not None

            else 0,

            tx.slot,

        ),

        reverse=True,

    )

    return merged


# ==========================================================


def validate_history(
    self,
    history: List[
        TransactionRecord
    ],
) -> Tuple[
    bool,
    List[str],
]:
    """
    Validate a wallet history.

    Checks:

        • duplicate signatures
        • missing signatures
        • missing slots
        • malformed timestamps
    """

    errors: List[
        str
    ] = []

    seen: Set[
        Signature
    ] = set()

    for tx in history:

        # ------------------------

        if not tx.signature:

            errors.append(
                "Missing transaction signature."
            )

        elif tx.signature in seen:

            errors.append(

                f"Duplicate signature: "

                f"{tx.signature}"

            )

        else:

            seen.add(
                tx.signature
            )

        # ------------------------

        if tx.slot <= 0:

            errors.append(

                f"{tx.signature}: "

                "Invalid slot."

            )

        # ------------------------

        if (

            tx.block_time

            is not None

            and

            tx.block_time < 1_500_000_000

        ):

            errors.append(

                f"{tx.signature}: "

                "Suspicious timestamp."

            )

        # ------------------------

        if not tx.wallets:

            errors.append(

                f"{tx.signature}: "

                "No participating wallets."

            )

    return (

        len(errors) == 0,

        errors,

    )

# ==========================================================
# Part 9
# Storage
# ==========================================================

import json
from pathlib import Path

# ==========================================================


def save_transactions(
    self,
    filepath: Union[
        str,
        Path,
    ],
    *,
    pretty: bool = True,
) -> Path:
    """
    Save all downloaded transactions
    to disk as JSON.
    """

    filepath = Path(filepath)

    data = [

        {

            "signature": tx.signature,

            "slot": tx.slot,

            "block_time": tx.block_time,

            "transaction_type":
                tx.transaction_type.value,

            "success": tx.success,

            "fee": tx.fee,

            "wallets": tx.wallets,

            "signers": tx.signers,

            "programs": tx.programs,

            "token_transfers":
                tx.token_transfers,

            "sol_transfers":
                tx.sol_transfers,

            "instructions":
                tx.instructions,

            "logs":
                tx.logs,

            "risk_flags":
                tx.risk_flags,

            "metadata":
                tx.metadata,

        }

        for tx

        in self.transactions.values()

    ]

    with filepath.open(
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(

            data,

            fp,

            indent=4 if pretty else None,

            ensure_ascii=False,

        )

    return filepath


# ==========================================================


def load_transactions(
    self,
    filepath: Union[
        str,
        Path,
    ],
) -> int:
    """
    Load transactions from JSON.
    """

    filepath = Path(filepath)

    with filepath.open(

        "r",

        encoding="utf-8",

    ) as fp:

        data = json.load(fp)

    loaded = 0

    for item in data:

        tx = TransactionRecord(

            signature=item["signature"],

            slot=item["slot"],

            block_time=item.get(
                "block_time"
            ),

            transaction_type=TransactionType(

                item.get(

                    "transaction_type",

                    "unknown",

                )

            ),

            success=item.get(
                "success",
                True,
            ),

            fee=item.get(
                "fee",
                0,
            ),

            wallets=item.get(
                "wallets",
                [],
            ),

            signers=item.get(
                "signers",
                [],
            ),

            programs=item.get(
                "programs",
                [],
            ),

            token_transfers=item.get(
                "token_transfers",
                [],
            ),

            sol_transfers=item.get(
                "sol_transfers",
                [],
            ),

            instructions=item.get(
                "instructions",
                [],
            ),

            logs=item.get(
                "logs",
                [],
            ),

            risk_flags=item.get(
                "risk_flags",
                [],
            ),

            metadata=item.get(
                "metadata",
                {},
            ),

        )

        self.transactions[
            tx.signature
        ] = tx

        loaded += 1

    self.statistics[
        "transactions_cached"
    ] = len(
        self.transactions
    )

    return loaded


# ==========================================================


def save_wallet_history(
    self,
    wallet: WalletAddress,
    filepath: Union[
        str,
        Path,
    ],
) -> Path:
    """
    Save one wallet's history.
    """

    filepath = Path(filepath)

    history = self.wallet_histories.get(
        wallet,
        [],
    )

    data = [

        tx.signature

        for tx in history

    ]

    with filepath.open(

        "w",

        encoding="utf-8",

    ) as fp:

        json.dump(

            data,

            fp,

            indent=4,

        )

    return filepath


# ==========================================================


def load_wallet_history(
    self,
    wallet: WalletAddress,
    filepath: Union[
        str,
        Path,
    ],
) -> int:
    """
    Restore a wallet history from disk.

    Existing TransactionRecords are reused
    from self.transactions.
    """

    filepath = Path(filepath)

    with filepath.open(

        "r",

        encoding="utf-8",

    ) as fp:

        signatures = json.load(fp)

    history = []

    for signature in signatures:

        tx = self.transactions.get(
            signature
        )

        if tx:

            history.append(
                tx
            )

    self.wallet_histories[
        wallet
    ] = history

    self.statistics[
        "wallets_cached"
    ] = len(
        self.wallet_histories
    )

    return len(history)


# ==========================================================


def clear_cache(
    self,
    *,
    transactions: bool = True,
    wallets: bool = True,
    expiry: bool = True,
) -> None:
    """
    Clear internal caches.

    Individual cache types can be
    selectively preserved.
    """

    if transactions:

        self.transaction_cache.clear()

        self.transactions.clear()

    if wallets:

        self.wallet_cache.clear()

        self.wallet_histories.clear()

    if expiry:

        self.cache_expiry.clear()

    self.downloaded_signatures.clear()

    self.pending_downloads.clear()

    self.program_index.clear()

    self.token_index.clear()

    self.wallet_index.clear()

    self.statistics[
        "cache_evictions"
    ] += 1

    self.statistics[
        "transactions_cached"
    ] = 0

    self.statistics[
        "wallets_cached"
    ] = 0

    self.logger.info(
        "TransactionFetcher cache cleared."
    )

# ==========================================================
# Part 10
# Analytics
# ==========================================================

def transaction_statistics(
    self,
) -> Dict[str, Any]:
    """
    Return overall transaction statistics.
    """

    transactions = list(
        self.transactions.values()
    )

    total = len(transactions)

    successful = sum(
        tx.success
        for tx in transactions
    )

    failed = total - successful

    unique_wallets = len(
        {

            wallet

            for tx in transactions

            for wallet in tx.wallets

        }

    )

    unique_programs = len(
        {

            program

            for tx in transactions

            for program in tx.programs

        }

    )

    avg_fee = (
        statistics.mean(
            tx.fee
            for tx in transactions
        )
        if total
        else 0
    )

    return {

        "total_transactions":
            total,

        "successful":
            successful,

        "failed":
            failed,

        "success_rate":
            successful / total
            if total
            else 0,

        "unique_wallets":
            unique_wallets,

        "unique_programs":
            unique_programs,

        "average_fee":
            avg_fee,

    }


# ==========================================================


def wallet_statistics(
    self,
) -> Dict[str, Any]:
    """
    Statistics for cached wallet histories.
    """

    wallets = len(
        self.wallet_histories
    )

    history_sizes = [

        len(history)

        for history

        in self.wallet_histories.values()

    ]

    return {

        "wallets_cached":
            wallets,

        "largest_history":
            max(
                history_sizes,
                default=0,
            ),

        "smallest_history":
            min(
                history_sizes,
                default=0,
            ),

        "average_history_size":

            statistics.mean(
                history_sizes
            )

            if history_sizes

            else 0,

    }


# ==========================================================


def download_metrics(
    self,
) -> Dict[str, Any]:
    """
    Download performance metrics.
    """

    download_times = (
        self._download_times
    )

    return {

        "downloads":

            self.statistics[
                "transactions_downloaded"
            ],

        "failed":

            self.statistics[
                "failed_downloads"
            ],

        "average_download_time":

            statistics.mean(
                download_times
            )

            if download_times

            else 0,

        "fastest_download":

            min(
                download_times,
                default=0,
            ),

        "slowest_download":

            max(
                download_times,
                default=0,
            ),

    }


# ==========================================================


def cache_statistics(
    self,
) -> Dict[str, Any]:
    """
    Cache performance metrics.
    """

    hits = self.statistics[
        "cache_hits"
    ]

    misses = self.statistics[
        "cache_misses"
    ]

    total = hits + misses

    return {

        "hits":
            hits,

        "misses":
            misses,

        "writes":

            self.statistics[
                "cache_writes"
            ],

        "evictions":

            self.statistics[
                "cache_evictions"
            ],

        "hit_rate":

            hits / total

            if total

            else 0,

        "transaction_cache":

            len(
                self.transaction_cache
            ),

        "wallet_cache":

            len(
                self.wallet_cache
            ),

    }


# ==========================================================


def explain_history(
    self,
    wallet: WalletAddress,
) -> str:
    """
    Produce a concise natural-language
    summary of a wallet's transaction history.
    """

    history = self.wallet_histories.get(
        wallet,
        [],
    )

    if not history:

        return (
            "No transaction history is "
            "currently available."
        )

    total = len(history)

    successful = sum(
        tx.success
        for tx in history
    )

    failed = total - successful

    unique_programs = len(
        {

            program

            for tx in history

            for program in tx.programs

        }

    )

    unique_tokens = len(
        {

            transfer.get("mint")

            for tx in history

            for transfer

            in tx.token_transfers

            if transfer.get("mint")

        }

    )

    first_tx = min(

        (

            tx.block_time

            for tx in history

            if tx.block_time
            is not None

        ),

        default=None,

    )

    latest_tx = max(

        (

            tx.block_time

            for tx in history

            if tx.block_time
            is not None

        ),

        default=None,

    )

    return (
        f"Wallet {wallet} contains "
        f"{total:,} cached transactions. "
        f"{successful:,} succeeded and "
        f"{failed:,} failed. "
        f"It interacted with "
        f"{unique_programs} unique programs "
        f"and {unique_tokens} unique token mints. "
        f"Recorded activity spans from "
        f"{first_tx} to {latest_tx}."
    )

# ==========================================================
# Part 11
# Engine
# ==========================================================

def fetch(
    self,
    wallet: WalletAddress,
    *,
    mode: Optional[FetchMode] = None,
    limit: Optional[int] = None,
) -> FetchResult:
    """
    Primary entry point for downloading
    transaction history.

    Automatically selects the configured
    fetch strategy and updates internal
    statistics.
    """

    result = self.fetch_wallet_history(
        wallet=wallet,
        mode=mode,
        limit=limit,
    )

    if self.config.deduplicate:
        result.transactions = self.remove_duplicates(
            result.transactions
        )

    self.wallet_histories[wallet] = result.transactions

    self.update_statistics()

    return result


# ==========================================================


def fetch_all(
    self,
    wallets: List[WalletAddress],
    *,
    mode: Optional[FetchMode] = None,
    limit: Optional[int] = None,
) -> Dict[WalletAddress, FetchResult]:
    """
    Download histories for multiple wallets.
    """

    results: Dict[
        WalletAddress,
        FetchResult,
    ] = {}

    for wallet in wallets:

        try:

            results[wallet] = self.fetch(
                wallet=wallet,
                mode=mode,
                limit=limit,
            )

        except Exception as exc:

            self.logger.exception(
                "Failed to fetch %s",
                wallet,
            )

            failed = FetchResult(
                wallet=wallet,
                mode=mode or self.config.mode,
                status=FetchStatus.FAILED,
            )

            failed.metadata["error"] = str(exc)

            failed.finished_at = datetime.utcnow()

            results[wallet] = failed

    self.update_statistics()

    return results


# ==========================================================


def refresh_history(
    self,
    wallet: WalletAddress,
) -> FetchResult:
    """
    Refresh a cached wallet history.

    Performs an incremental download when
    possible, otherwise falls back to a
    recent history fetch.
    """

    history = self.wallet_histories.get(
        wallet,
        [],
    )

    if history:

        newest = max(
            history,
            key=lambda tx: (
                tx.block_time or 0,
                tx.slot,
            ),
        )

        incremental = self.fetch_history_until(
            wallet,
            newest.signature,
        )

        merged = self.merge_histories(
            history,
            incremental.transactions,
        )

        self.wallet_histories[
            wallet
        ] = merged

        incremental.transactions = merged

        self.statistics[
            "last_refresh"
        ] = datetime.utcnow()

        self.update_statistics()

        return incremental

    return self.fetch_recent_history(
        wallet,
    )


# ==========================================================


def update_statistics(
    self,
) -> Dict[str, Any]:
    """
    Refresh global runtime statistics.
    """

    self.statistics[
        "transactions_cached"
    ] = len(
        self.transactions
    )

    self.statistics[
        "wallets_cached"
    ] = len(
        self.wallet_histories
    )

    self.statistics[
        "history_fetches"
    ] = sum(
        len(history)
        for history
        in self.wallet_histories.values()
    )

    self.statistics[
        "cache_size"
    ] = (
        len(self.transaction_cache)
        + len(self.wallet_cache)
    )

    self.statistics[
        "uptime_seconds"
    ] = (
        time.time()
        - self.statistics["start_time"]
    )

    return self.statistics            
