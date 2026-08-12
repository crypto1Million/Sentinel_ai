"""
Mock PostgreSQL Integration
===========================

Fake PostgreSQL tables, CRUD operations and transactions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


class MockPostgres:

    def __init__(self):

        self.tables: Dict[str, List[Dict[str, Any]]] = {}

        self.transactions: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Tables
    # ------------------------------------------------------------------

    def create_table(
        self,
        name: str,
    ):

        self.tables.setdefault(
            name,
            [],
        )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def insert(
        self,
        table: str,
        row: Dict[str, Any],
    ):

        self.create_table(table)

        record = deepcopy(row)

        self.tables[table].append(record)

        return record

    def select(
        self,
        table: str,
        filters: Dict[str, Any] | None = None,
    ):

        rows = self.tables.get(
            table,
            [],
        )

        if not filters:
            return deepcopy(rows)

        return [
            deepcopy(row)
            for row in rows
            if all(
                row.get(key) == value
                for key, value in filters.items()
            )
        ]

    def update(
        self,
        table: str,
        filters: Dict[str, Any],
        updates: Dict[str, Any],
    ):

        count = 0

        for row in self.tables.get(table, []):

            if all(
                row.get(key) == value
                for key, value in filters.items()
            ):

                row.update(updates)

                count += 1

        return count

    def delete(
        self,
        table: str,
        filters: Dict[str, Any],
    ):

        rows = self.tables.get(
            table,
            [],
        )

        original_count = len(rows)

        self.tables[table] = [
            row
            for row in rows
            if not all(
                row.get(key) == value
                for key, value in filters.items()
            )
        ]

        return original_count - len(
            self.tables[table]
        )

    # ------------------------------------------------------------------
    # Transactions
    # ------------------------------------------------------------------

    def begin(self):

        transaction = {
            "snapshot": deepcopy(self.tables),
            "active": True,
        }

        self.transactions.append(transaction)

        return transaction

    def commit(
        self,
        transaction: Dict[str, Any],
    ):

        transaction["active"] = False

        return True

    def rollback(
        self,
        transaction: Dict[str, Any],
    ):

        self.tables = deepcopy(
            transaction["snapshot"]
        )

        transaction["active"] = False

        return True

    # ------------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------------

    def diagnostics(self):

        return {
            "connected": True,
            "tables": len(self.tables),
            "transactions": len(
                self.transactions
            ),
        }

    def summary(self):

        return {
            "service": "mock-postgres",
            "tables": list(
                self.tables.keys()
            ),
        }


def mock_postgres() -> MockPostgres:

    database = MockPostgres()

    database.create_table("wallets")
    database.create_table("tokens")
    database.create_table("bundles")
    database.create_table("transactions")

    return database