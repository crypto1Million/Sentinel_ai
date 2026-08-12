"""
PostgreSQL Client
=================

High-level PostgreSQL client.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from sqlalchemy import text

from .connection import PostgreSQLConnection


###############################################################################
# PostgreSQLClient
###############################################################################


class PostgreSQLClient:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        connection: PostgreSQLConnection,
    ):

        self.connection = connection

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(self):

        return self.connection.connect()

    ###########################################################################

    def disconnect(self):

        return self.connection.disconnect()

    ###########################################################################

    def health(self):

        return self.connection.health()

    ###########################################################################
    # Queries
    ###########################################################################

    def execute(
        self,
        sql: str,
        params: Optional[Dict] = None,
    ):

        with self.connection.session() as session:

            result = session.execute(
                text(sql),
                params or {},
            )

            session.commit()

            return result

    ###########################################################################

    def fetch_one(
        self,
        sql: str,
        params: Optional[Dict] = None,
    ):

        return self.execute(
            sql,
            params,
        ).first()

    ###########################################################################

    def fetch_all(
        self,
        sql: str,
        params: Optional[Dict] = None,
    ):

        return self.execute(
            sql,
            params,
        ).all()

    ###########################################################################

    def scalar(
        self,
        sql: str,
        params: Optional[Dict] = None,
    ):

        result = self.execute(
            sql,
            params,
        )

        return result.scalar()

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "client": "PostgreSQLClient",
            "connected": self.connection.is_connected,
        }

    ###########################################################################

    def summary(self):

        return {
            "provider": "PostgreSQL",
            "status": (
                "connected"
                if self.connection.is_connected
                else "disconnected"
            ),
        }


###############################################################################
# Utilities
###############################################################################


def normalize_result(
    rows: List[Any],
):

    return [dict(r._mapping) for r in rows]