# ==========================================================
# Imports
# ==========================================================

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    Literal,
    TypeAlias,
)

import aiohttp
import requests

# ==========================================================
# Constants
# ==========================================================

DEFAULT_RPC_TIMEOUT = 30

DEFAULT_MAX_RETRIES = 5

DEFAULT_RETRY_DELAY = 1.0

DEFAULT_BATCH_SIZE = 100

DEFAULT_RATE_LIMIT = 50

DEFAULT_CACHE_TTL = 300

DEFAULT_COMMITMENT = "confirmed"

DEFAULT_ENCODING = "jsonParsed"

DEFAULT_HELIUS_MAINNET = (
    "https://mainnet.helius-rpc.com/"
)

DEFAULT_HELIUS_DEVNET = (
    "https://devnet.helius-rpc.com/"
)

# ==========================================================
# Enums
# ==========================================================

class Network(Enum):
    MAINNET = "mainnet"

    DEVNET = "devnet"


class Commitment(Enum):
    PROCESSED = "processed"

    CONFIRMED = "confirmed"

    FINALIZED = "finalized"


class Encoding(Enum):
    JSON = "json"

    JSON_PARSED = "jsonParsed"

    BASE64 = "base64"


class RPCMethod(Enum):
    GET_BALANCE = "getBalance"

    GET_ACCOUNT_INFO = "getAccountInfo"

    GET_MULTIPLE_ACCOUNTS = "getMultipleAccounts"

    GET_SIGNATURES = (
        "getSignaturesForAddress"
    )

    GET_TRANSACTION = (
        "getTransaction"
    )

    GET_BLOCK = "getBlock"

    GET_SLOT = "getSlot"

    GET_TOKEN_ACCOUNTS = (
        "getTokenAccountsByOwner"
    )

    GET_PROGRAM_ACCOUNTS = (
        "getProgramAccounts"
    )

    GET_LARGEST_ACCOUNTS = (
        "getLargestAccounts"
    )

    GET_LATEST_BLOCKHASH = (
        "getLatestBlockhash"
    )


# ==========================================================
# Type Aliases
# ==========================================================

WalletAddress: TypeAlias = str

Signature: TypeAlias = str

Slot: TypeAlias = int

RPCParams: TypeAlias = List[Any]

RPCResult: TypeAlias = Dict[str, Any]

Attributes: TypeAlias = Dict[str, Any]

JSONType: TypeAlias = Dict[str, Any]

# ==========================================================
# Configuration
# ==========================================================

@dataclass(slots=True)
class HeliusConfig:
    """
    Helius client configuration.
    """

    api_key: str

    network: Network = (
        Network.MAINNET
    )

    timeout: int = (
        DEFAULT_RPC_TIMEOUT
    )

    commitment: Commitment = (
        Commitment.CONFIRMED
    )

    encoding: Encoding = (
        Encoding.JSON_PARSED
    )

    max_retries: int = (
        DEFAULT_MAX_RETRIES
    )

    retry_delay: float = (
        DEFAULT_RETRY_DELAY
    )

    batch_size: int = (
        DEFAULT_BATCH_SIZE
    )

    rate_limit: int = (
        DEFAULT_RATE_LIMIT
    )

    cache_ttl: int = (
        DEFAULT_CACHE_TTL
    )

    use_async: bool = True

    verify_ssl: bool = True


# ==========================================================
# RPC Response
# ==========================================================

@dataclass(slots=True)
class HeliusResponse:
    """
    Standardized Helius RPC response.
    """

    success: bool

    method: str

    result: Optional[Any] = None

    error: Optional[Any] = None

    status_code: int = 200

    request_time: float = 0.0

    slot: Optional[int] = None

    metadata: Attributes = field(
        default_factory=dict
    )

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    @property
    def ok(self) -> bool:
        return self.success

    def to_dict(self) -> Dict[str, Any]:

        return {

            "success": self.success,

            "method": self.method,

            "result": self.result,

            "error": self.error,

            "status_code": self.status_code,

            "request_time": self.request_time,

            "slot": self.slot,

            "metadata": self.metadata,

            "timestamp": (
                self.timestamp.isoformat()
            ),

        }


# ==========================================================
# RPC Error
# ==========================================================

class RPCError(Exception):
    """
    Generic Helius RPC exception.
    """

    def __init__(
        self,
        message: str,
        method: Optional[str] = None,
        code: Optional[int] = None,
        data: Optional[Any] = None,
    ):

        super().__init__(message)

        self.method = method

        self.code = code

        self.data = data

    def __str__(self):

        text = super().__str__()

        if self.method:

            text += (
                f" | method={self.method}"
            )

        if self.code is not None:

            text += (
                f" | code={self.code}"
            )

        return text

# ==========================================================
# Part 2
# Initialization
# HTTP Session
# Authentication
# Rate Limiter
# ==========================================================

class HeliusClient:
    """
    Production-grade Helius RPC client.

    Provides:

        • HTTP connection pooling
        • Automatic authentication
        • Rate limiting
        • Retry support
        • Request caching
        • Async + Sync support
    """

    # ======================================================
    # Initialization
    # ======================================================

    def __init__(
        self,
        config: HeliusConfig,
    ) -> None:

        self.config = config

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.base_url = self._build_endpoint()

        self.session = self._create_session()

        self.async_session: Optional[
            aiohttp.ClientSession
        ] = None

        self.headers = self._build_headers()

        self.statistics: Dict[str, Any] = {

            "requests": 0,

            "successful_requests": 0,

            "failed_requests": 0,

            "cache_hits": 0,

            "cache_misses": 0,

            "rate_limited": 0,

            "retries": 0,

            "bytes_received": 0,

            "bytes_sent": 0,

            "last_request": None,

        }

        self.cache: Dict[
            str,
            Any,
        ] = {}

        self.cache_expiry: Dict[
            str,
            float,
        ] = {}

        # -----------------------------
        # Rate Limiter
        # -----------------------------

        self._request_times: List[
            float
        ] = []

        self._rate_lock = asyncio.Lock()

        self.logger.info(

            "HeliusClient initialized "

            f"({config.network.value})"

        )

    # ======================================================
    # HTTP Session
    # ======================================================

    def _create_session(
        self,
    ) -> requests.Session:
        """
        Create reusable HTTP session.
        """

        session = requests.Session()

        adapter = requests.adapters.HTTPAdapter(

            pool_connections=20,

            pool_maxsize=50,

            max_retries=0,

        )

        session.mount(
            "https://",
            adapter,
        )

        session.mount(
            "http://",
            adapter,
        )

        session.headers.update(
            self.headers
            if hasattr(self, "headers")
            else {}
        )

        return session

    async def get_async_session(
        self,
    ) -> aiohttp.ClientSession:
        """
        Lazy async session creation.
        """

        if (

            self.async_session is None

            or

            self.async_session.closed

        ):

            timeout = aiohttp.ClientTimeout(

                total=self.config.timeout

            )

            connector = aiohttp.TCPConnector(

                ssl=self.config.verify_ssl,

                limit=50,

            )

            self.async_session = (

                aiohttp.ClientSession(

                    timeout=timeout,

                    connector=connector,

                    headers=self.headers,

                )

            )

        return self.async_session

    # ======================================================
    # Authentication
    # ======================================================

    def _build_endpoint(
        self,
    ) -> str:
        """
        Construct Helius endpoint.
        """

        if self.config.network == Network.DEVNET:

            base = DEFAULT_HELIUS_DEVNET

        else:

            base = DEFAULT_HELIUS_MAINNET

        return (

            f"{base}"

            f"?api-key="

            f"{self.config.api_key}"

        )

    def _build_headers(
        self,
    ) -> Dict[str, str]:
        """
        Default HTTP headers.
        """

        return {

            "Content-Type":
                "application/json",

            "Accept":
                "application/json",

            "User-Agent":
                "SentinelAI/1.0",

        }

    # ======================================================
    # Rate Limiter
    # ======================================================

    async def wait_for_rate_limit(
        self,
    ) -> None:
        """
        Sliding-window rate limiter.

        Prevents exceeding configured
        requests/second.
        """

        async with self._rate_lock:

            now = time.time()

            self._request_times = [

                t

                for t in self._request_times

                if now - t < 1.0

            ]

            if (

                len(self._request_times)

                >=

                self.config.rate_limit

            ):

                wait = (

                    1.0

                    -

                    (

                        now

                        -

                        self._request_times[0]

                    )

                )

                if wait > 0:

                    self.statistics[
                        "rate_limited"
                    ] += 1

                    await asyncio.sleep(wait)

            self._request_times.append(
                time.time()
            )

    def check_rate_limit(
        self,
    ) -> None:
        """
        Synchronous rate limiter.
        """

        now = time.time()

        self._request_times = [

            t

            for t in self._request_times

            if now - t < 1.0

        ]

        if (

            len(self._request_times)

            >=

            self.config.rate_limit

        ):

            wait = (

                1.0

                -

                (

                    now

                    -

                    self._request_times[0]

                )

            )

            if wait > 0:

                self.statistics[
                    "rate_limited"
                ] += 1

                time.sleep(wait)

        self._request_times.append(
            time.time()
        )

# ==========================================================
# Part 3
# Generic RPC
# ==========================================================

def rpc(
    self,
    method: Union[
        RPCMethod,
        str,
    ],
    params: Optional[
        RPCParams
    ] = None,
) -> HeliusResponse:
    """
    Execute a single RPC request.
    """

    self.check_rate_limit()

    if isinstance(
        method,
        RPCMethod,
    ):
        method = method.value

    payload = {

        "jsonrpc": "2.0",

        "id": 1,

        "method": method,

        "params": params or [],

    }

    start = time.perf_counter()

    self.statistics[
        "requests"
    ] += 1

    try:

        response = self.retry_request(
            payload
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        self.statistics[
            "successful_requests"
        ] += 1

        self.statistics[
            "last_request"
        ] = datetime.utcnow()

        return HeliusResponse(

            success=True,

            method=method,

            result=response.get(
                "result"
            ),

            error=response.get(
                "error"
            ),

            status_code=200,

            request_time=elapsed,

            slot=response.get(
                "result",
                {},
            ).get(
                "context",
                {},
            ).get(
                "slot"
            )
            if isinstance(
                response.get(
                    "result"
                ),
                dict,
            )
            else None,

        )

    except Exception as exc:

        self.statistics[
            "failed_requests"
        ] += 1

        return HeliusResponse(

            success=False,

            method=method,

            error=str(exc),

            status_code=500,

        )


# ==========================================================


def batch_rpc(
    self,
    requests_data: List[
        Tuple[
            Union[
                RPCMethod,
                str,
            ],
            RPCParams,
        ]
    ],
) -> List[
    HeliusResponse
]:
    """
    Execute multiple RPC requests
    in a single batch.
    """

    self.check_rate_limit()

    payload = []

    for idx, (
        method,
        params,
    ) in enumerate(
        requests_data,
        start=1,
    ):

        if isinstance(
            method,
            RPCMethod,
        ):
            method = method.value

        payload.append({

            "jsonrpc": "2.0",

            "id": idx,

            "method": method,

            "params": params,

        })

    start = time.perf_counter()

    response = self.retry_request(
        payload
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    results = []

    for item in response:

        results.append(

            HeliusResponse(

                success=(
                    "error"
                    not in item
                ),

                method=item.get(
                    "method",
                    "",
                ),

                result=item.get(
                    "result"
                ),

                error=item.get(
                    "error"
                ),

                status_code=200,

                request_time=elapsed,

            )

        )

    return results


# ==========================================================


def retry_request(
    self,
    payload: Any,
) -> JSONType:
    """
    Execute HTTP request with
    automatic retry.
    """

    delay = (
        self.config.retry_delay
    )

    last_error = None

    for attempt in range(

        self.config.max_retries

    ):

        try:

            response = self.session.post(

                self.base_url,

                json=payload,

                timeout=self.config.timeout,

                verify=self.config.verify_ssl,

            )

            self.statistics[
                "bytes_received"
            ] += len(
                response.content
            )

            self.statistics[
                "bytes_sent"
            ] += len(
                json.dumps(
                    payload
                )
            )

            response.raise_for_status()

            return response.json()

        except Exception as exc:

            last_error = exc

            self.statistics[
                "retries"
            ] += 1

            if (

                attempt

                <

                self.config.max_retries
                - 1

            ):

                time.sleep(
                    delay
                )

                delay *= 2

    raise RPCError(

        str(last_error),

        code=500,

    )


# ==========================================================


def health_check(
    self,
) -> bool:
    """
    Verify RPC availability.

    Uses getSlot().
    """

    try:

        response = self.rpc(

            RPCMethod.GET_SLOT

        )

        return response.success

    except Exception:

        return False

# ==========================================================
# Part 4
# Wallet APIs
# ==========================================================

def get_balance(
    self,
    wallet: WalletAddress,
) -> HeliusResponse:
    """
    Return SOL balance for a wallet.
    """

    return self.rpc(

        RPCMethod.GET_BALANCE,

        [

            wallet,

            {

                "commitment":
                    self.config.commitment.value

            },

        ],

    )


# ==========================================================


def get_account_info(
    self,
    wallet: WalletAddress,
) -> HeliusResponse:
    """
    Return account information.
    """

    return self.rpc(

        RPCMethod.GET_ACCOUNT_INFO,

        [

            wallet,

            {

                "encoding":
                    self.config.encoding.value,

                "commitment":
                    self.config.commitment.value,

            },

        ],

    )


# ==========================================================


def get_token_accounts(
    self,
    wallet: WalletAddress,
    *,
    program_id: str = (
        "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    ),
) -> HeliusResponse:
    """
    Return all SPL token accounts owned
    by the wallet.
    """

    return self.rpc(

        RPCMethod.GET_TOKEN_ACCOUNTS,

        [

            wallet,

            {

                "programId":
                    program_id

            },

            {

                "encoding":
                    self.config.encoding.value,

            },

        ],

    )


# ==========================================================


def get_assets(
    self,
    wallet: WalletAddress,
    *,
    page: int = 1,
    limit: int = 100,
) -> HeliusResponse:
    """
    Return all assets owned by a wallet.

    Uses Helius DAS API.
    """

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method":
            "getAssetsByOwner",

        "params": {

            "ownerAddress":
                wallet,

            "page":
                page,

            "limit":
                limit,

        },

    }

    response = self.retry_request(
        payload
    )

    return HeliusResponse(

        success=True,

        method="getAssetsByOwner",

        result=response.get(
            "result"
        ),

    )


# ==========================================================


def get_portfolio(
    self,
    wallet: WalletAddress,
) -> Dict[str, Any]:
    """
    Build a complete wallet portfolio.

    Includes:

        • SOL balance
        • Account info
        • Token accounts
        • Digital assets
    """

    balance = self.get_balance(
        wallet
    )

    account = self.get_account_info(
        wallet
    )

    tokens = self.get_token_accounts(
        wallet
    )

    assets = self.get_assets(
        wallet
    )

    portfolio = {

        "wallet": wallet,

        "balance":
            balance.result,

        "account":
            account.result,

        "token_accounts":
            tokens.result,

        "assets":
            assets.result,

        "generated_at":
            datetime.utcnow(),

    }

    return portfolio

# ==========================================================
# Part 5
# Transaction APIs
# ==========================================================

def get_signatures(
    self,
    wallet: WalletAddress,
    *,
    limit: int = 100,
    before: Optional[Signature] = None,
    until: Optional[Signature] = None,
) -> HeliusResponse:
    """
    Fetch transaction signatures for a wallet.
    """

    params = [

        wallet,

        {

            "limit": limit,

            "commitment":
                self.config.commitment.value,

        },

    ]

    if before is not None:
        params[1]["before"] = before

    if until is not None:
        params[1]["until"] = until

    return self.rpc(

        RPCMethod.GET_SIGNATURES,

        params,

    )


# ==========================================================


def get_transaction(
    self,
    signature: Signature,
) -> HeliusResponse:
    """
    Fetch a transaction by signature.
    """

    return self.rpc(

        RPCMethod.GET_TRANSACTION,

        [

            signature,

            {

                "encoding":
                    self.config.encoding.value,

                "commitment":
                    self.config.commitment.value,

                "maxSupportedTransactionVersion": 0,

            },

        ],

    )


# ==========================================================


def get_transactions(
    self,
    signatures: List[Signature],
) -> List[HeliusResponse]:
    """
    Fetch multiple transactions.

    Uses batch RPC automatically.
    """

    requests = [

        (

            RPCMethod.GET_TRANSACTION,

            [

                signature,

                {

                    "encoding":
                        self.config.encoding.value,

                    "commitment":
                        self.config.commitment.value,

                    "maxSupportedTransactionVersion": 0,

                },

            ],

        )

        for signature in signatures

    ]

    return self.batch_rpc(
        requests
    )


# ==========================================================


def get_parsed_transaction(
    self,
    signature: Signature,
) -> Dict[str, Any]:
    """
    Return parsed transaction.

    Raises RPCError if unavailable.
    """

    response = self.get_transaction(
        signature
    )

    if not response.success:

        raise RPCError(

            "Unable to fetch transaction.",

            method="getTransaction",

            data=response.error,

        )

    return response.result


# ==========================================================


def get_enriched_transaction(
    self,
    signature: Signature,
) -> Dict[str, Any]:
    """
    Return a normalized transaction object.

    Used throughout Sentinel AI.

    Extracts:

        • slot
        • timestamp
        • fee
        • signers
        • instructions
        • token transfers
        • SOL transfers
        • accounts
        • logs
    """

    tx = self.get_parsed_transaction(
        signature
    )

    meta = tx.get(
        "meta",
        {},
    )

    transaction = tx.get(
        "transaction",
        {},
    )

    message = transaction.get(
        "message",
        {},
    )

    return {

        "signature":
            signature,

        "slot":
            tx.get("slot"),

        "block_time":
            tx.get("blockTime"),

        "version":
            tx.get("version"),

        "fee":
            meta.get("fee", 0),

        "status":
            "success"

            if meta.get("err") is None

            else "failed",

        "accounts":
            message.get(
                "accountKeys",
                [],
            ),

        "signers": [

            account

            for account in message.get(
                "accountKeys",
                [],
            )

            if isinstance(account, dict)

            and account.get(
                "signer",
                False,
            )

        ],

        "instructions":
            message.get(
                "instructions",
                [],
            ),

        "inner_instructions":
            meta.get(
                "innerInstructions",
                [],
            ),

        "pre_balances":
            meta.get(
                "preBalances",
                [],
            ),

        "post_balances":
            meta.get(
                "postBalances",
                [],
            ),

        "pre_token_balances":
            meta.get(
                "preTokenBalances",
                [],
            ),

        "post_token_balances":
            meta.get(
                "postTokenBalances",
                [],
            ),

        "log_messages":
            meta.get(
                "logMessages",
                [],
            ),

        "compute_units":
            meta.get(
                "computeUnitsConsumed",
            ),

        "loaded_addresses":
            meta.get(
                "loadedAddresses",
                {},
            ),

        "raw":
            tx,

    }


# ==========================================================
# Part 6
# History APIs
# ==========================================================

def get_wallet_history(
    self,
    wallet: WalletAddress,
    *,
    limit: int = 1000,
    before: Optional[Signature] = None,
    until: Optional[Signature] = None,
) -> List[Dict[str, Any]]:
    """
    Fetch complete wallet transaction history.

    Returns normalized enriched transactions.
    """

    signatures = self.get_signatures(
        wallet,
        limit=limit,
        before=before,
        until=until,
    )

    if not signatures.success:
        return []

    history: List[
        Dict[str, Any]
    ] = []

    for item in signatures.result:

        signature = item.get(
            "signature"
        )

        if signature is None:
            continue

        try:

            history.append(

                self.get_enriched_transaction(
                    signature
                )

            )

        except Exception:

            continue

    return history


# ==========================================================


def get_token_history(
    self,
    wallet: WalletAddress,
    token_mint: str,
    *,
    limit: int = 1000,
) -> List[Dict[str, Any]]:
    """
    Return history involving a specific SPL token.
    """

    history = self.get_wallet_history(
        wallet,
        limit=limit,
    )

    filtered = []

    for tx in history:

        token_balances = (

            tx.get(
                "post_token_balances",
                [],
            )

            +

            tx.get(
                "pre_token_balances",
                [],
            )

        )

        for token in token_balances:

            mint = token.get(
                "mint"
            )

            if mint == token_mint:

                filtered.append(
                    tx
                )

                break

    return filtered


# ==========================================================


def get_sol_history(
    self,
    wallet: WalletAddress,
    *,
    limit: int = 1000,
) -> List[Dict[str, Any]]:
    """
    Return only SOL transfer history.
    """

    history = self.get_wallet_history(
        wallet,
        limit=limit,
    )

    sol_history = []

    for tx in history:

        pre = tx.get(
            "pre_balances",
            [],
        )

        post = tx.get(
            "post_balances",
            [],
        )

        if pre != post:

            sol_history.append(
                tx
            )

    return sol_history


# ==========================================================


def stream_history(
    self,
    wallet: WalletAddress,
    *,
    batch_size: int = 100,
):
    """
    Generator for streaming large wallet histories.

    Avoids loading everything into memory.
    """

    before = None

    while True:

        response = self.get_signatures(

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

        signatures = response.result

        for item in signatures:

            signature = item.get(
                "signature"
            )

            if signature is None:
                continue

            try:

                yield self.get_enriched_transaction(
                    signature
                )

            except Exception:

                continue

        before = signatures[-1].get(
            "signature"
        )

        if len(signatures) < batch_size:
            break


# ==========================================================


def recursive_history(
    self,
    wallet: WalletAddress,
    *,
    depth: int = 3,
    visited: Optional[
        Set[WalletAddress]
    ] = None,
) -> Dict[
    WalletAddress,
    List[Dict[str, Any]]
]:
    """
    Recursively collect transaction histories
    from connected wallets.

    Used by FundingTracker and Wallet DNA.
    """

    if visited is None:

        visited = set()

    if (

        wallet in visited

        or

        depth <= 0

    ):

        return {}

    visited.add(
        wallet
    )

    histories = {

        wallet: self.get_wallet_history(
            wallet
        )

    }

    neighbors = set()

    for tx in histories[wallet]:

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

                address != wallet

            ):

                neighbors.add(
                    address
                )

    for neighbor in neighbors:

        histories.update(

            self.recursive_history(

                neighbor,

                depth=depth - 1,

                visited=visited,

            )

        )

    return histories

# ==========================================================
# Part 7
# NFT APIs
# ==========================================================

def get_nft(
    self,
    asset_id: str,
) -> HeliusResponse:
    """
    Fetch a single NFT/Compressed Asset.

    Uses Helius DAS getAsset().
    """

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method": "getAsset",

        "params": {

            "id": asset_id,

        },

    }

    response = self.retry_request(
        payload
    )

    return HeliusResponse(

        success="error" not in response,

        method="getAsset",

        result=response.get(
            "result"
        ),

        error=response.get(
            "error"
        ),

    )


# ==========================================================


def get_nfts(
    self,
    wallet: WalletAddress,
    *,
    page: int = 1,
    limit: int = 100,
) -> HeliusResponse:
    """
    Fetch every NFT owned by a wallet.

    Uses DAS getAssetsByOwner().
    """

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method": "getAssetsByOwner",

        "params": {

            "ownerAddress": wallet,

            "page": page,

            "limit": limit,

            "displayOptions": {

                "showCollectionMetadata": True,

                "showFungible": False,

            },

        },

    }

    response = self.retry_request(
        payload
    )

    return HeliusResponse(

        success="error" not in response,

        method="getAssetsByOwner",

        result=response.get(
            "result"
        ),

        error=response.get(
            "error"
        ),

    )


# ==========================================================


def get_collection(
    self,
    collection_id: str,
    *,
    page: int = 1,
    limit: int = 100,
) -> HeliusResponse:
    """
    Fetch all assets inside a collection.

    Uses DAS getAssetsByGroup().
    """

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method": "getAssetsByGroup",

        "params": {

            "groupKey": "collection",

            "groupValue": collection_id,

            "page": page,

            "limit": limit,

        },

    }

    response = self.retry_request(
        payload
    )

    return HeliusResponse(

        success="error" not in response,

        method="getAssetsByGroup",

        result=response.get(
            "result"
        ),

        error=response.get(
            "error"
        ),

    )


# ==========================================================


def get_metadata(
    self,
    asset_id: str,
) -> Dict[str, Any]:
    """
    Return normalized NFT metadata.

    Includes:

        • name
        • symbol
        • description
        • image
        • attributes
        • collection
        • creators
        • royalty info
    """

    response = self.get_nft(
        asset_id
    )

    if not response.success:

        raise RPCError(

            "Unable to fetch NFT.",

            method="getAsset",

            data=response.error,

        )

    asset = response.result

    content = asset.get(
        "content",
        {},
    )

    metadata = content.get(
        "metadata",
        {},
    )

    grouping = asset.get(
        "grouping",
        [],
    )

    royalty = asset.get(
        "royalty",
        {},
    )

    creators = royalty.get(
        "creators",
        [],
    )

    image = None

    files = content.get(
        "files",
        [],
    )

    if files:

        image = files[0].get(
            "uri"
        )

    return {

        "asset_id": asset_id,

        "name": metadata.get(
            "name"
        ),

        "symbol": metadata.get(
            "symbol"
        ),

        "description": metadata.get(
            "description"
        ),

        "image": image,

        "attributes": metadata.get(
            "attributes",
            [],
        ),

        "collection": grouping,

        "creators": creators,

        "seller_fee_basis_points":

            royalty.get(
                "basis_points"
            ),

        "compressed":

            asset.get(
                "compression",
                {}
            ).get(
                "compressed",
                False,
            ),

        "mutable":

            asset.get(
                "mutable",
                False,
            ),

        "raw": asset,

    }

# ==========================================================
# Part 8
# DAS APIs
# ==========================================================

def search_assets(
    self,
    *,
    owner: Optional[WalletAddress] = None,
    creator: Optional[str] = None,
    authority: Optional[str] = None,
    grouping: Optional[str] = None,
    page: int = 1,
    limit: int = 100,
) -> HeliusResponse:
    """
    Search assets using Helius DAS searchAssets().
    """

    params = {

        "page": page,

        "limit": limit,

    }

    if owner:
        params["ownerAddress"] = owner

    if creator:
        params["creatorAddress"] = creator

    if authority:
        params["authorityAddress"] = authority

    if grouping:
        params["grouping"] = grouping

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method": "searchAssets",

        "params": params,

    }

    response = self.retry_request(payload)

    return HeliusResponse(

        success="error" not in response,

        method="searchAssets",

        result=response.get("result"),

        error=response.get("error"),

    )


# ==========================================================


def get_asset(
    self,
    asset_id: str,
) -> HeliusResponse:
    """
    Wrapper around DAS getAsset().
    """

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method": "getAsset",

        "params": {

            "id": asset_id,

        },

    }

    response = self.retry_request(payload)

    return HeliusResponse(

        success="error" not in response,

        method="getAsset",

        result=response.get("result"),

        error=response.get("error"),

    )


# ==========================================================


def get_assets_by_owner(
    self,
    owner: WalletAddress,
    *,
    page: int = 1,
    limit: int = 100,
) -> HeliusResponse:
    """
    DAS getAssetsByOwner().
    """

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method": "getAssetsByOwner",

        "params": {

            "ownerAddress": owner,

            "page": page,

            "limit": limit,

        },

    }

    response = self.retry_request(payload)

    return HeliusResponse(

        success="error" not in response,

        method="getAssetsByOwner",

        result=response.get("result"),

        error=response.get("error"),

    )


# ==========================================================


def get_assets_by_group(
    self,
    group_key: str,
    group_value: str,
    *,
    page: int = 1,
    limit: int = 100,
) -> HeliusResponse:
    """
    DAS getAssetsByGroup().
    """

    payload = {

        "jsonrpc": "2.0",

        "id": "sentinel",

        "method": "getAssetsByGroup",

        "params": {

            "groupKey": group_key,

            "groupValue": group_value,

            "page": page,

            "limit": limit,

        },

    }

    response = self.retry_request(payload)

    return HeliusResponse(

        success="error" not in response,

        method="getAssetsByGroup",

        result=response.get("result"),

        error=response.get("error"),

    )


# ==========================================================


def search_transactions(
    self,
    *,
    wallet: Optional[WalletAddress] = None,
    signature: Optional[Signature] = None,
    before: Optional[Signature] = None,
    until: Optional[Signature] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """
    High-level transaction search helper.

    Internally uses getSignaturesForAddress()
    followed by enriched transaction retrieval.
    """

    if wallet is None:
        return []

    signatures = self.get_signatures(

        wallet,

        limit=limit,

        before=before,

        until=until,

    )

    if not signatures.success:
        return []

    transactions = []

    for item in signatures.result:

        sig = item.get("signature")

        if signature is not None:

            if sig != signature:
                continue

        try:

            transactions.append(

                self.get_enriched_transaction(sig)

            )

        except Exception:

            continue

    return transactions

# ==========================================================
# Part 9
# Webhooks
# ==========================================================

def create_webhook(
    self,
    webhook_url: str,
    account_addresses: List[WalletAddress],
    *,
    webhook_type: str = "enhanced",
    transaction_types: Optional[
        List[str]
    ] = None,
    auth_header: Optional[str] = None,
) -> HeliusResponse:
    """
    Create a Helius webhook.
    """

    endpoint = (
        "https://api.helius.xyz/v0/webhooks"
        f"?api-key={self.config.api_key}"
    )

    payload = {

        "webhookURL": webhook_url,

        "accountAddresses":
            account_addresses,

        "webhookType":
            webhook_type,

        "transactionTypes":
            transaction_types or [],

    }

    if auth_header:

        payload["authHeader"] = auth_header

    response = self.session.post(

        endpoint,

        json=payload,

        timeout=self.config.timeout,

    )

    response.raise_for_status()

    data = response.json()

    return HeliusResponse(

        success=True,

        method="createWebhook",

        result=data,

    )


# ==========================================================


def delete_webhook(
    self,
    webhook_id: str,
) -> bool:
    """
    Delete a webhook.
    """

    endpoint = (

        f"https://api.helius.xyz/v0/webhooks/{webhook_id}"

        f"?api-key={self.config.api_key}"

    )

    response = self.session.delete(

        endpoint,

        timeout=self.config.timeout,

    )

    return response.status_code in (

        200,

        204,

    )


# ==========================================================


def edit_webhook(
    self,
    webhook_id: str,
    *,
    webhook_url: Optional[str] = None,
    account_addresses: Optional[
        List[WalletAddress]
    ] = None,
    transaction_types: Optional[
        List[str]
    ] = None,
) -> HeliusResponse:
    """
    Update an existing webhook.
    """

    endpoint = (

        f"https://api.helius.xyz/v0/webhooks/{webhook_id}"

        f"?api-key={self.config.api_key}"

    )

    payload: Dict[str, Any] = {}

    if webhook_url:

        payload["webhookURL"] = webhook_url

    if account_addresses:

        payload["accountAddresses"] = (
            account_addresses
        )

    if transaction_types:

        payload["transactionTypes"] = (
            transaction_types
        )

    response = self.session.put(

        endpoint,

        json=payload,

        timeout=self.config.timeout,

    )

    response.raise_for_status()

    return HeliusResponse(

        success=True,

        method="editWebhook",

        result=response.json(),

    )


# ==========================================================


def list_webhooks(
    self,
) -> HeliusResponse:
    """
    List all configured webhooks.
    """

    endpoint = (

        "https://api.helius.xyz/v0/webhooks"

        f"?api-key={self.config.api_key}"

    )

    response = self.session.get(

        endpoint,

        timeout=self.config.timeout,

    )

    response.raise_for_status()

    return HeliusResponse(

        success=True,

        method="listWebhooks",

        result=response.json(),

    )


# ==========================================================


def parse_webhook(
    self,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize an incoming Helius webhook payload.

    Returns a Sentinel-friendly structure.
    """

    events = payload.get(
        "events",
        []
    )

    parsed_events = []

    for event in events:

        parsed_events.append({

            "signature":
                event.get(
                    "signature"
                ),

            "slot":
                event.get(
                    "slot"
                ),

            "timestamp":
                event.get(
                    "timestamp"
                ),

            "type":
                event.get(
                    "type"
                ),

            "source":
                event.get(
                    "source"
                ),

            "fee":
                event.get(
                    "fee"
                ),

            "description":
                event.get(
                    "description"
                ),

            "accounts":
                event.get(
                    "accountData",
                    [],
                ),

            "native_transfers":
                event.get(
                    "nativeTransfers",
                    [],
                ),

            "token_transfers":
                event.get(
                    "tokenTransfers",
                    [],
                ),

            "instructions":
                event.get(
                    "instructions",
                    [],
                ),

            "raw":
                event,

        })

    return {

        "event_count":
            len(parsed_events),

        "received_at":
            datetime.utcnow(),

        "events":
            parsed_events,

    }

# ==========================================================
# Part 10
# Performance
# ==========================================================

def batch_requests(
    self,
    requests_data: List[
        Tuple[
            Union[RPCMethod, str],
            RPCParams,
        ]
    ],
    *,
    batch_size: Optional[int] = None,
) -> List[HeliusResponse]:
    """
    Execute a large number of RPC requests in batches.
    """

    batch_size = (

        batch_size

        or

        self.config.batch_size

    )

    results: List[
        HeliusResponse
    ] = []

    for i in range(

        0,

        len(requests_data),

        batch_size,

    ):

        chunk = requests_data[
            i:i + batch_size
        ]

        results.extend(

            self.batch_rpc(
                chunk
            )

        )

    return results


# ==========================================================


async def parallel_requests(
    self,
    requests_data: List[
        Tuple[
            Union[RPCMethod, str],
            RPCParams,
        ]
    ],
    *,
    concurrency: int = 20,
) -> List[HeliusResponse]:
    """
    Execute multiple RPC requests concurrently.
    """

    semaphore = asyncio.Semaphore(
        concurrency
    )

    session = await self.get_async_session()

    async def worker(
        method,
        params,
    ) -> HeliusResponse:

        async with semaphore:

            await self.wait_for_rate_limit()

            if isinstance(
                method,
                RPCMethod,
            ):
                method = method.value

            payload = {

                "jsonrpc": "2.0",

                "id": 1,

                "method": method,

                "params": params,

            }

            start = time.perf_counter()

            try:

                async with session.post(

                    self.base_url,

                    json=payload,

                ) as response:

                    response.raise_for_status()

                    data = await response.json()

                    elapsed = (

                        time.perf_counter()

                        - start

                    )

                    self.statistics[
                        "requests"
                    ] += 1

                    self.statistics[
                        "successful_requests"
                    ] += 1

                    return HeliusResponse(

                        success=True,

                        method=method,

                        result=data.get(
                            "result"
                        ),

                        error=data.get(
                            "error"
                        ),

                        status_code=response.status,

                        request_time=elapsed,

                    )

            except Exception as exc:

                self.statistics[
                    "failed_requests"
                ] += 1

                return HeliusResponse(

                    success=False,

                    method=method,

                    error=str(exc),

                    status_code=500,

                )

    tasks = [

        worker(
            method,
            params,
        )

        for method, params

        in requests_data

    ]

    return await asyncio.gather(
        *tasks
    )


# ==========================================================


def cache(
    self,
    key: str,
    value: Any = None,
    *,
    ttl: Optional[int] = None,
) -> Any:
    """
    Generic cache helper.

    Usage:

        cache(key)
            -> read

        cache(key, value)
            -> write
    """

    now = time.time()

    if value is None:

        expiry = self.cache_expiry.get(
            key
        )

        if (

            expiry is None

            or

            expiry < now

        ):

            self.statistics[
                "cache_misses"
            ] += 1

            self.cache.pop(
                key,
                None,
            )

            self.cache_expiry.pop(
                key,
                None,
            )

            return None

        self.statistics[
            "cache_hits"
        ] += 1

        return self.cache.get(
            key
        )

    ttl = (

        ttl

        or

        self.config.cache_ttl

    )

    self.cache[key] = value

    self.cache_expiry[key] = (

        now + ttl

    )

    return value


# ==========================================================


def metrics(
    self,
) -> Dict[str, Any]:
    """
    Return runtime performance metrics.
    """

    total = max(

        1,

        self.statistics[
            "requests"
        ],

    )

    return {

        "uptime_seconds":

            time.time()

            - self._request_times[0]

            if self._request_times

            else 0,

        "requests":

            self.statistics[
                "requests"
            ],

        "successful":

            self.statistics[
                "successful_requests"
            ],

        "failed":

            self.statistics[
                "failed_requests"
            ],

        "success_rate":

            round(

                self.statistics[
                    "successful_requests"
                ]

                / total

                * 100,

                2,

            ),

        "cache_hit_rate":

            round(

                self.statistics[
                    "cache_hits"
                ]

                /

                max(

                    1,

                    self.statistics[
                        "cache_hits"
                    ]

                    +

                    self.statistics[
                        "cache_misses"
                    ],

                )

                * 100,

                2,

            ),

        "bytes_sent":

            self.statistics[
                "bytes_sent"
            ],

        "bytes_received":

            self.statistics[
                "bytes_received"
            ],

        "rate_limited":

            self.statistics[
                "rate_limited"
            ],

        "retries":

            self.statistics[
                "retries"
            ],

    }


# ==========================================================


def statistics(
    self,
) -> Dict[str, Any]:
    """
    Return complete client statistics.
    """

    stats = dict(
        self.statistics
    )

    stats.update({

        "network":

            self.config.network.value,

        "endpoint":

            self.base_url,

        "cached_items":

            len(
                self.cache
            ),

        "active_rate_window":

            len(
                self._request_times
            ),

        "timestamp":

            datetime.utcnow(),

    })

    return stats

# ==========================================================
# Part 11
# Utilities
# ==========================================================

def endpoint(
    self,
) -> str:
    """
    Return active Helius endpoint.
    """

    return self.base_url


# ==========================================================


def headers(
    self,
) -> Dict[str, str]:
    """
    Return HTTP headers currently
    used by the client.
    """

    return dict(self.session.headers)


# ==========================================================


def validate_response(
    self,
    response: Union[
        Dict[str, Any],
        List[Any],
    ],
) -> bool:
    """
    Validate Helius RPC response.

    Raises RPCError if invalid.
    """

    if response is None:

        raise RPCError(
            "Empty response."
        )

    if isinstance(
        response,
        dict,
    ):

        if "error" in response:

            error = response["error"]

            raise RPCError(

                error.get(
                    "message",
                    "RPC Error",
                ),

                code=error.get(
                    "code"
                ),

                data=error,

            )

        if (

            "result"

            not in response

            and

            "jsonrpc"

            not in response

        ):

            raise RPCError(
                "Malformed RPC response."
            )

        return True

    if isinstance(
        response,
        list,
    ):

        for item in response:

            self.validate_response(
                item
            )

        return True

    raise RPCError(
        "Unknown response format."
    )


# ==========================================================


def close(
    self,
) -> None:
    """
    Close HTTP resources.
    """

    try:

        self.session.close()

    except Exception:

        pass

    if (

        self.async_session

        and

        not self.async_session.closed

    ):

        try:

            loop = asyncio.get_event_loop()

            if loop.is_running():

                loop.create_task(
                    self.async_session.close()
                )

            else:

                loop.run_until_complete(
                    self.async_session.close()
                )

        except Exception:

            pass

    self.logger.info(
        "HeliusClient closed."
    )


# ==========================================================


def __enter__(
    self,
):
    """
    Context manager entry.
    """

    return self


# ==========================================================


def __exit__(
    self,
    exc_type,
    exc_val,
    exc_tb,
):
    """
    Context manager exit.
    """

    self.close()

    return False


# ==========================================================


async def __aenter__(
    self,
):
    """
    Async context manager entry.
    """

    await self.get_async_session()

    return self


# ==========================================================


async def __aexit__(
    self,
    exc_type,
    exc_val,
    exc_tb,
):
    """
    Async context manager exit.
    """

    if (

        self.async_session

        and

        not self.async_session.closed

    ):

        await self.async_session.close()

    self.session.close()

    return False        
