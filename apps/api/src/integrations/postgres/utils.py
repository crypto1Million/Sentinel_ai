"""
PostgreSQL Utilities
====================
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict


###############################################################################
# SQL Utilities
###############################################################################


def compile_query(query):

    return str(query)


###############################################################################


def normalize_result(row):

    if row is None:

        return None

    return dict(row._mapping)


###############################################################################


def normalize_results(rows):

    return [
        normalize_result(r)
        for r in rows
    ]


###############################################################################
# Metadata
###############################################################################


def checksum(value: str):

    return hashlib.sha256(
        value.encode()
    ).hexdigest()


###############################################################################


def table_name(model):

    return model.__tablename__


###############################################################################


def schema_name(metadata):

    return list(metadata.tables.keys())


###############################################################################
# Runtime
###############################################################################


def diagnostics():

    return {
        "utilities": "ready",
    }


###############################################################################


def summary():

    return {
        "module": "postgres.utils",
    }