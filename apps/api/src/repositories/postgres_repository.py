###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from .base_repository import BaseRepository

###############################################################################
# PostgreSQLRepository
###############################################################################


class PostgreSQLRepository(BaseRepository):
    """
    PostgreSQL repository implementation.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        engine: Engine,
    ) -> None:

        super().__init__(engine)

        self.engine = engine
        self.connection = None

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(
        self,
    ) -> None:

        self.connection = self.engine.connect()

    ###########################################################################

    def disconnect(
        self,
    ) -> None:

        if self.connection:
            self.connection.close()

        self.connection = None

    ###########################################################################
    # Execution
    ###########################################################################

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> Any:

        return self.connection.execute(
            text(query),
            parameters or {},
        )

    ###########################################################################

    def execute_many(
        self,
        query: str,
        rows: list[dict],
    ) -> Any:

        return self.connection.execute(
            text(query),
            rows,
        )

    ###########################################################################

    def fetch_one(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> dict | None:

        result = self.execute(
            query,
            parameters,
        ).mappings().first()

        return dict(result) if result else None

    ###########################################################################

    def fetch_all(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[dict]:

        rows = self.execute(
            query,
            parameters,
        ).mappings().all()

        return [
            dict(row)
            for row in rows
        ]

    ###########################################################################
    # CRUD
    ###########################################################################

    def insert(
        self,
        table: str,
        values: dict,
    ) -> Any:

        columns = ", ".join(values.keys())
        params = ", ".join(
            f":{k}"
            for k in values.keys()
        )

        query = (
            f"INSERT INTO {table}"
            f" ({columns})"
            f" VALUES ({params})"
        )

        return self.execute(
            query,
            values,
        )

    ###########################################################################

    def update(
        self,
        table: str,
        values: dict,
        where: dict,
    ) -> Any:

        setters = ", ".join(
            f"{k}=:{k}"
            for k in values.keys()
        )

        conditions = " AND ".join(
            f"{k}=:where_{k}"
            for k in where.keys()
        )

        params = values.copy()

        for key, value in where.items():
            params[f"where_{key}"] = value

        query = (
            f"UPDATE {table}"
            f" SET {setters}"
            f" WHERE {conditions}"
        )

        return self.execute(
            query,
            params,
        )

    ###########################################################################

    def delete(
        self,
        table: str,
        where: dict,
    ) -> Any:

        conditions = " AND ".join(
            f"{k}=:{k}"
            for k in where.keys()
        )

        query = (
            f"DELETE FROM {table}"
            f" WHERE {conditions}"
        )

        return self.execute(
            query,
            where,
        )

    ###########################################################################

    def upsert(
        self,
        table: str,
        values: dict,
        conflict_column: str,
    ) -> Any:

        columns = ", ".join(values.keys())

        params = ", ".join(
            f":{k}"
            for k in values.keys()
        )

        updates = ", ".join(
            f"{k}=EXCLUDED.{k}"
            for k in values.keys()
            if k != conflict_column
        )

        query = f"""
        INSERT INTO {table}
        ({columns})
        VALUES ({params})
        ON CONFLICT ({conflict_column})
        DO UPDATE SET
        {updates}
        """

        return self.execute(
            query,
            values,
        )

    ###########################################################################

    def count(
        self,
        table: str,
        where: dict | None = None,
    ) -> int:

        query = f"SELECT COUNT(*) AS total FROM {table}"

        if where:

            query += " WHERE "

            query += " AND ".join(
                f"{k}=:{k}"
                for k in where.keys()
            )

        result = self.fetch_one(
            query,
            where,
        )

        return result["total"]

    ###########################################################################

    def exists(
        self,
        table: str,
        where: dict,
    ) -> bool:

        return self.count(
            table,
            where,
        ) > 0

    ###########################################################################

    def raw_query(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[dict]:

        return self.fetch_all(
            query,
            parameters,
        )

    ###########################################################################
    # Health
    ###########################################################################

    def health(
        self,
    ) -> bool:

        try:

            self.execute(
                "SELECT 1",
            )

            return True

        except SQLAlchemyError:

            return False

    ###########################################################################

    def diagnostics(
        self,
    ) -> dict:

        return {
            "repository": "PostgreSQL",
            "connected": self.connection is not None,
            "healthy": self.health(),
        }


###############################################################################
# Runtime
###############################################################################


def summary(
) -> dict:

    return {
        "repository": "PostgreSQL",
        "supports_upsert": True,
        "supports_transactions": True,
    }


###############################################################################
# Utilities
###############################################################################


def compile_query(
    query: str,
) -> str:

    return query.strip()


###############################################################################


def sanitize_parameters(
    parameters: dict | None,
) -> dict:

    return parameters or {}


###############################################################################


def explain_query(
    repository: PostgreSQLRepository,
    query: str,
) -> list[dict]:

    return repository.fetch_all(
        f"EXPLAIN {query}",
    )