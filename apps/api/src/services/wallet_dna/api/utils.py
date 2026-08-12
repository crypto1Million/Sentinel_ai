###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import Request

###############################################################################
# Constants
###############################################################################

REQUEST_ID_HEADER = "X-Request-ID"

DEFAULT_USER_AGENT = "Unknown"

###############################################################################
# Request Helpers
###############################################################################

def client_ip(
    request: Request,
) -> str:
    """
    Return client IP address.
    """

    forwarded = request.headers.get(
        "X-Forwarded-For"
    )

    if forwarded:
        return forwarded.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


###############################################################################


def user_agent(
    request: Request,
) -> str:
    """
    Return request User-Agent.
    """

    return request.headers.get(
        "User-Agent",
        DEFAULT_USER_AGENT,
    )


###############################################################################


def request_size(
    request: Request,
) -> int:
    """
    Return request size in bytes.
    """

    value = request.headers.get(
        "Content-Length",
        "0",
    )

    try:
        return int(value)
    except ValueError:
        return 0


###############################################################################


def request_id(
    request: Request,
) -> str:
    """
    Return existing request ID
    or generate one.
    """

    return request.headers.get(
        REQUEST_ID_HEADER,
        str(uuid4()),
    )


###############################################################################


def request_context(
    request: Request,
) -> dict[str, Any]:
    """
    Common request metadata.
    """

    return {
        "id": request_id(request),
        "method": request.method,
        "path": request.url.path,
        "client_ip": client_ip(request),
        "user_agent": user_agent(request),
        "size": request_size(request),
    }

###############################################################################
# Response Helpers
###############################################################################

from datetime import datetime, timezone
import re


def timestamp() -> str:
    """
    Return current UTC ISO timestamp.
    """

    return (
        datetime.now(timezone.utc)
        .isoformat()
    )


###############################################################################


def response_time(
    start_time: float,
    end_time: float,
) -> float:
    """
    Response time in milliseconds.
    """

    return round(
        (end_time - start_time) * 1000,
        2,
    )


###############################################################################


def success_message(
    message: str = "Success",
) -> dict:
    """
    Standard success payload.
    """

    return {
        "success": True,
        "message": message,
        "timestamp": timestamp(),
    }


###############################################################################


def error_message(
    message: str = "Error",
    code: str = "UNKNOWN_ERROR",
) -> dict:
    """
    Standard error payload.
    """

    return {
        "success": False,
        "error": message,
        "code": code,
        "timestamp": timestamp(),
    }


###############################################################################


def envelope(
    data: object,
    *,
    success: bool = True,
    message: str = "OK",
) -> dict:
    """
    Wrap API responses in a common envelope.
    """

    return {
        "success": success,
        "message": message,
        "timestamp": timestamp(),
        "data": data,
    }


###############################################################################
# String Utilities
###############################################################################

_SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


def slugify(
    text: str,
) -> str:
    """
    Convert text into URL slug.
    """

    text = text.lower().strip()

    text = _SLUG_PATTERN.sub(
        "-",
        text,
    )

    return text.strip("-")


###############################################################################


def truncate(
    text: str,
    length: int = 100,
    suffix: str = "...",
) -> str:
    """
    Truncate long text.
    """

    if len(text) <= length:
        return text

    return text[:length].rstrip() + suffix


###############################################################################


def snake_to_camel(
    text: str,
) -> str:
    """
    snake_case -> camelCase
    """

    parts = text.split("_")

    return (
        parts[0]
        + "".join(
            word.capitalize()
            for word in parts[1:]
        )
    )


###############################################################################


def camel_to_snake(
    text: str,
) -> str:
    """
    camelCase -> snake_case
    """

    return re.sub(
        r"(?<!^)(?=[A-Z])",
        "_",
        text,
    ).lower()


###############################################################################


def sanitize_text(
    text: str,
) -> str:
    """
    Remove duplicate whitespace and trim.
    """

    return " ".join(text.split())

###############################################################################
# Time Utilities
###############################################################################

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from typing import Any
import json


def utc_now() -> datetime:
    """
    Current UTC datetime.
    """

    return datetime.now(timezone.utc)


###############################################################################


def unix_timestamp() -> int:
    """
    Current Unix timestamp.
    """

    return int(
        utc_now().timestamp()
    )


###############################################################################


def iso_timestamp() -> str:
    """
    ISO-8601 timestamp.
    """

    return utc_now().isoformat()


###############################################################################


def parse_datetime(
    value: str,
) -> datetime:
    """
    Parse ISO datetime.
    """

    return datetime.fromisoformat(value)


###############################################################################


def human_duration(
    seconds: int,
) -> str:
    """
    Human readable duration.
    """

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours:
        return f"{hours}h {minutes}m"

    if minutes:
        return f"{minutes}m {secs}s"

    return f"{secs}s"


###############################################################################
# Serialization
###############################################################################

def decimal_to_float(
    value: Decimal,
) -> float:
    """
    Convert Decimal to float.
    """

    return float(value)


###############################################################################


def bytes_to_hex(
    value: bytes,
) -> str:
    """
    Bytes → hex string.
    """

    return value.hex()


###############################################################################


def serialize_uuid(
    value: UUID,
) -> str:
    """
    UUID → string.
    """

    return str(value)


###############################################################################


def clean_none(
    obj: Any,
) -> Any:
    """
    Recursively remove None values.
    """

    if isinstance(obj, dict):

        return {
            k: clean_none(v)
            for k, v in obj.items()
            if v is not None
        }

    if isinstance(obj, list):

        return [
            clean_none(v)
            for v in obj
            if v is not None
        ]

    return obj


###############################################################################


def jsonable(
    obj: Any,
) -> Any:
    """
    Convert common Python objects into JSON-safe values.
    """

    if isinstance(obj, Decimal):
        return decimal_to_float(obj)

    if isinstance(obj, UUID):
        return serialize_uuid(obj)

    if isinstance(obj, bytes):
        return bytes_to_hex(obj)

    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, dict):
        return {
            k: jsonable(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [
            jsonable(v)
            for v in obj
        ]

    return obj

###############################################################################
# Validation Helpers
###############################################################################

import base64
from urllib.parse import urlencode


def is_valid_uuid(
    value: str,
) -> bool:
    """
    Validate UUID string.
    """

    try:
        UUID(value)
        return True
    except Exception:
        return False


###############################################################################


def is_valid_wallet(
    value: str,
) -> bool:
    """
    Validate Solana wallet address.
    """

    return (
        isinstance(value, str)
        and 32 <= len(value) <= 44
    )


###############################################################################


def is_valid_token(
    value: str,
) -> bool:
    """
    Validate token mint address.
    """

    return is_valid_wallet(value)


###############################################################################


def is_valid_signature(
    value: str,
) -> bool:
    """
    Validate transaction signature.
    """

    return (
        isinstance(value, str)
        and len(value) >= 64
    )


###############################################################################


def validate_request(
    condition: bool,
    message: str,
) -> None:
    """
    Raise validation error when condition fails.
    """

    if not condition:
        raise ValueError(message)


###############################################################################
# Pagination Helpers
###############################################################################

DEFAULT_LIMIT = 25
MAX_LIMIT = 100


def safe_limit(
    value: int | None,
) -> int:
    """
    Clamp page size.
    """

    if value is None:
        return DEFAULT_LIMIT

    return max(
        1,
        min(value, MAX_LIMIT),
    )


###############################################################################


def safe_offset(
    value: int | None,
) -> int:
    """
    Clamp offset.
    """

    if value is None:
        return 0

    return max(0, value)


###############################################################################


def build_links(
    *,
    base_url: str,
    limit: int,
    offset: int,
    total: int,
) -> dict[str, str | None]:
    """
    Build previous/next pagination links.
    """

    previous = None
    next_page = None

    if offset > 0:
        previous = (
            f"{base_url}?"
            + urlencode(
                {
                    "limit": limit,
                    "offset": max(
                        offset - limit,
                        0,
                    ),
                }
            )
        )

    if offset + limit < total:
        next_page = (
            f"{base_url}?"
            + urlencode(
                {
                    "limit": limit,
                    "offset": offset + limit,
                }
            )
        )

    return {
        "previous": previous,
        "next": next_page,
    }


###############################################################################


def cursor_token(
    value: str,
) -> str:
    """
    Encode cursor token.
    """

    return base64.urlsafe_b64encode(
        value.encode()
    ).decode()

###############################################################################
# Runtime Helpers
###############################################################################

import hashlib
import secrets
import string
import time
import uuid

try:
    import psutil
except ImportError:
    psutil = None


_START_TIME = time.time()


def runtime_info() -> dict[str, Any]:
    """
    Runtime information.
    """

    return {
        "started_at": _START_TIME,
        "uptime_seconds": uptime(),
        "python_version": sys.version.split()[0],
        "platform": platform.system(),
    }


###############################################################################


def memory_usage() -> dict[str, float]:
    """
    Current process memory usage (MB).
    """

    if psutil is None:
        return {
            "rss_mb": 0.0,
            "vms_mb": 0.0,
        }

    process = psutil.Process()

    memory = process.memory_info()

    return {
        "rss_mb": round(memory.rss / 1024**2, 2),
        "vms_mb": round(memory.vms / 1024**2, 2),
    }


###############################################################################


def uptime() -> float:
    """
    Seconds since process startup.
    """

    return round(
        time.time() - _START_TIME,
        2,
    )


###############################################################################


def diagnostics() -> dict[str, Any]:
    """
    Runtime diagnostics.
    """

    return {
        "runtime": runtime_info(),
        "memory": memory_usage(),
    }


###############################################################################
# Miscellaneous
###############################################################################

def generate_uuid() -> str:
    """
    Generate UUID4 string.
    """

    return str(uuid.uuid4())


###############################################################################


def random_string(
    length: int = 32,
) -> str:
    """
    Generate secure random string.
    """

    alphabet = (
        string.ascii_letters
        + string.digits
    )

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


###############################################################################


def hash_value(
    value: str,
    algorithm: str = "sha256",
) -> str:
    """
    Hash a string.
    """

    hasher = hashlib.new(algorithm)

    hasher.update(value.encode())

    return hasher.hexdigest()


###############################################################################


def secure_compare(
    a: str,
    b: str,
) -> bool:
    """
    Timing-safe comparison.
    """

    return secrets.compare_digest(a, b)


###############################################################################


def summary() -> dict[str, Any]:
    """
    Utility module summary.
    """

    return {
        "runtime": runtime_info(),
        "memory": memory_usage(),
        "uptime_seconds": uptime(),
    }                