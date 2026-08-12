###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import uuid
from contextlib import contextmanager
from typing import Any

###############################################################################
# TransactionManager
###############################################################################


class TransactionManager:
    """
    Generic transaction manager.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        connection: Any,
    ) -> None:
        self.connection = connection
        self._active = False
        self._savepoints: list[str] = []

    ###########################################################################
    # Transaction Control
    ###########################################################################

    def begin(
        self,
    ) -> None:
        """
        Begin transaction.
        """

        self._active = True

    ###########################################################################

    def commit(
        self,
    ) -> None:
        """
        Commit transaction.
        """

        self._active = False
        self._savepoints.clear()

    ###########################################################################

    def rollback(
        self,
    ) -> None:
        """
        Rollback transaction.
        """

        self._active = False
        self._savepoints.clear()

    ###########################################################################

    def savepoint(
        self,
    ) -> str:
        """
        Create savepoint.
        """

        point = f"sp_{uuid.uuid4().hex[:8]}"

        self._savepoints.append(point)

        return point

    ###########################################################################

    def release_savepoint(
        self,
        savepoint: str,
    ) -> None:
        """
        Release savepoint.
        """

        if savepoint in self._savepoints:
            self._savepoints.remove(savepoint)

    ###########################################################################

    @contextmanager
    def transaction_scope(
        self,
    ):
        """
        Transaction context manager.
        """

        self.begin()

        try:
            yield self
            self.commit()

        except Exception:
            self.rollback()
            raise

    ###########################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Transaction diagnostics.
        """

        return {
            "active": self._active,
            "savepoints": len(self._savepoints),
        }


###############################################################################
# Batch Transactions
###############################################################################


def batch_insert(
    repository: Any,
    table: str,
    rows: list[dict[str, Any]],
) -> int:
    """
    Batch insert.
    """

    for row in rows:
        repository.insert(
            table=table,
            values=row,
        )

    return len(rows)


###############################################################################


def batch_update(
    repository: Any,
    table: str,
    updates: list[dict[str, Any]],
    where_key: str = "id",
) -> int:
    """
    Batch update.
    """

    for row in updates:

        where = {
            where_key: row[where_key],
        }

        values = {
            k: v
            for k, v in row.items()
            if k != where_key
        }

        repository.update(
            table=table,
            values=values,
            where=where,
        )

    return len(updates)


###############################################################################


def batch_delete(
    repository: Any,
    table: str,
    ids: list[Any],
    key: str = "id",
) -> int:
    """
    Batch delete.
    """

    for value in ids:
        repository.delete(
            table=table,
            where={
                key: value,
            },
        )

    return len(ids)


###############################################################################


def batch_execute(
    operations: list,
) -> list[Any]:
    """
    Execute multiple operations.
    """

    results = []

    for operation in operations:
        results.append(operation())

    return results


###############################################################################
# Runtime
###############################################################################


def summary(
) -> dict[str, Any]:
    """
    Module summary.
    """

    return {
        "module": "transaction",
        "supports_batch": True,
        "supports_savepoints": True,
    }


###############################################################################
# Utilities
###############################################################################


def transaction_id(
) -> str:
    """
    Generate transaction id.
    """

    return uuid.uuid4().hex


###############################################################################


def transaction_metadata(
    manager: TransactionManager,
) -> dict[str, Any]:
    """
    Transaction metadata.
    """

    return {
        "transaction_id": transaction_id(),
        "active": manager._active,
        "savepoints": manager._savepoints,
    }