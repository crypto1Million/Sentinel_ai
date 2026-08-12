###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Any

from clickhouse_connect import get_client
from clickhouse_connect.driver.client import Client

from .base_repository import BaseRepository

###############################################################################
# ClickHouseRepository
###############################################################################


class ClickHouseRepository(BaseRepository):
    """
    ClickHouse repository implementation.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
    ) -> None:

        super().__init__(None)

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        self.client: Client | None = None

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(
        self,
    ) -> None:

        self.client = get_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
        )

    ###########################################################################

    def disconnect(
        self,
    ) -> None:

        if self.client:
            self.client.close()

        self.client = None

    ###########################################################################
    # Execution
    ###########################################################################

    def execute(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> Any:

        return self.client.command(
            query,
            parameters=parameters,
        )

    ###########################################################################

    def execute_many(
        self,
        query: str,
        rows: list[dict],
    ) -> Any:

        return self.client.insert(
            query,
            rows,
        )

    ###########################################################################

    def fetch_one(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> dict | None:

        result = self.client.query(
            query,
            parameters=parameters,
        )

        if not result.result_rows:
            return None

        return dict(
            zip(
                result.column_names,
                result.result_rows[0],
            )
        )

    ###########################################################################

    def fetch_all(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[dict]:

        result = self.client.query(
            query,
            parameters=parameters,
        )

        return [
            dict(zip(result.column_names, row))
            for row in result.result_rows
        ]

    ###########################################################################
    # CRUD
    ###########################################################################

    def insert(
        self,
        table: str,
        values: dict,
    ) -> Any:

        return self.client.insert(
            table,
            [list(values.values())],
            column_names=list(values.keys()),
        )

    ###########################################################################

    def bulk_insert(
        self,
        table: str,
        rows: list[dict],
    ) -> Any:

        if not rows:
            return None

        return self.client.insert(
            table,
            [
                list(row.values())
                for row in rows
            ],
            column_names=list(rows[0].keys()),
        )

    ###########################################################################

    def update(
        self,
        table: str,
        values: dict,
        where: str,
    ) -> Any:

        setters = ", ".join(
            f"{k}='{v}'"
            for k, v in values.items()
        )

        query = (
            f"ALTER TABLE {table} "
            f"UPDATE {setters} "
            f"WHERE {where}"
        )

        return self.execute(query)

    ###########################################################################

    def delete(
        self,
        table: str,
        where: str,
    ) -> Any:

        query = (
            f"ALTER TABLE {table} "
            f"DELETE WHERE {where}"
        )

        return self.execute(query)

    ###########################################################################

    def optimize_table(
        self,
        table: str,
    ) -> None:

        self.execute(
            f"OPTIMIZE TABLE {table} FINAL"
        )

    ###########################################################################

    def truncate(
        self,
        table: str,
    ) -> None:

        self.execute(
            f"TRUNCATE TABLE {table}"
        )

    ###########################################################################

    def raw_query(
        self,
        query: str,
    ) -> list[dict]:

        return self.fetch_all(query)

    ###########################################################################
    # Health
    ###########################################################################

    def health(
        self,
    ) -> bool:

        try:

            self.execute("SELECT 1")

            return True

        except Exception:

            return False

    ###########################################################################

    def diagnostics(
        self,
    ) -> dict:

        return {
            "repository": "ClickHouse",
            "connected": self.client is not None,
            "healthy": self.health(),
        }


###############################################################################
# Analytics
###############################################################################


def aggregate(
    repository: ClickHouseRepository,
    query: str,
):

    return repository.fetch_all(query)


###############################################################################


def group_by(
    repository: ClickHouseRepository,
    query: str,
):

    return repository.fetch_all(query)


###############################################################################


def time_series(
    repository: ClickHouseRepository,
    query: str,
):

    return repository.fetch_all(query)


###############################################################################


def histogram(
    repository: ClickHouseRepository,
    query: str,
):

    return repository.fetch_all(query)


###############################################################################


def percentile(
    repository: ClickHouseRepository,
    query: str,
):

    return repository.fetch_one(query)


###############################################################################
# Runtime
###############################################################################


def summary():

    return {
        "repository": "ClickHouse",
        "analytics": True,
        "bulk_insert": True,
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
    repository: ClickHouseRepository,
    query: str,
):

    return repository.fetch_all(
        f"EXPLAIN {query}"
    )


###############################################################################


def optimize_query(
    query: str,
) -> str:

    return query.strip()