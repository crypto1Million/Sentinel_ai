###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from abc import ABC
from contextlib import contextmanager
from typing import Any, Iterable

###############################################################################
# BaseRepository
###############################################################################


class BaseRepository(ABC):
    """
    Base repository for all database backends.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        connection: Any,
    ) -> None:
        self.connection = connection

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(self) -> None:
        """
        Open connection.
        """
        ...

    ###########################################################################

    def disconnect(self) -> None:
        """
        Close connection.
        """
        ...

    ###########################################################################
    # Execution
    ###########################################################################

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> Any:
        """
        Execute SQL.
        """
        ...

    ###########################################################################

    def fetch_one(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> Any:
        """
        Fetch single row.
        """
        ...

    ###########################################################################

    def fetch_all(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[Any]:
        """
        Fetch rows.
        """
        ...

    ###########################################################################
    # CRUD
    ###########################################################################

    def insert(
        self,
        table: str,
        values: dict,
    ) -> Any:
        ...

    ###########################################################################

    def update(
        self,
        table: str,
        values: dict,
        where: dict,
    ) -> Any:
        ...

    ###########################################################################

    def delete(
        self,
        table: str,
        where: dict,
    ) -> Any:
        ...

    ###########################################################################

    def exists(
        self,
        table: str,
        where: dict,
    ) -> bool:
        ...

    ###########################################################################

    def count(
        self,
        table: str,
        where: dict | None = None,
    ) -> int:
        ...

    ###########################################################################

    def paginate(
        self,
        query: str,
        limit: int,
        offset: int,
    ) -> list[Any]:
        ...

    ###########################################################################
    # Transactions
    ###########################################################################

    @contextmanager
    def transaction(self):
        """
        Transaction scope.
        """

        try:
            yield self
            self.commit()

        except Exception:
            self.rollback()
            raise

    ###########################################################################

    def commit(self) -> None:
        ...

    ###########################################################################

    def rollback(self) -> None:
        ...

    ###########################################################################

    def close(self) -> None:
        ...

    ###########################################################################

    def diagnostics(self) -> dict:
        """
        Repository diagnostics.
        """

        return {
            "repository": self.__class__.__name__,
            "connected": self.connection is not None,
        }


###############################################################################
# Mixins
###############################################################################


class CRUDMixin:
    """
    Common CRUD helpers.
    """

    def create(self, *args, **kwargs):
        return self.insert(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.fetch_one(*args, **kwargs)

    def read_all(self, *args, **kwargs):
        return self.fetch_all(*args, **kwargs)

    def remove(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


###############################################################################


class PaginationMixin:
    """
    Pagination helpers.
    """

    def page(
        self,
        query: str,
        limit: int,
        offset: int,
    ):
        return self.paginate(
            query=query,
            limit=limit,
            offset=offset,
        )


###############################################################################


class FilterMixin:
    """
    Filter helpers.
    """

    def filter(
        self,
        query: str,
        filters: dict,
    ):
        return build_filters(
            query,
            filters,
        )


###############################################################################
# Runtime
###############################################################################


def summary() -> dict:
    """
    Repository summary.
    """

    return {
        "module": "base_repository",
        "mixins": [
            "CRUDMixin",
            "PaginationMixin",
            "FilterMixin",
        ],
    }


###############################################################################
# Utilities
###############################################################################


def build_query(
    table: str,
    columns: Iterable[str],
) -> str:
    """
    Build SELECT query.
    """

    return (
        f"SELECT {', '.join(columns)} "
        f"FROM {table}"
    )


###############################################################################


def build_filters(
    query: str,
    filters: dict,
) -> str:
    """
    Append WHERE clause.
    """

    if not filters:
        return query

    conditions = [
        f"{key}=:{key}"
        for key in filters.keys()
    ]

    return (
        query
        + " WHERE "
        + " AND ".join(conditions)
    )


###############################################################################


def safe_execute(
    repository: BaseRepository,
    query: str,
    parameters: dict | None = None,
):
    """
    Safe execution wrapper.
    """

    try:
        return repository.execute(
            query,
            parameters,
        )

    except Exception:
        repository.rollback()
        raise


###############################################################################


def normalize_result(
    result: Any,
):
    """
    Normalize database result.
    """

    if result is None:
        return {}

    return result