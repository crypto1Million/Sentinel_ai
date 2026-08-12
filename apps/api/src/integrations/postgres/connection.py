"""
PostgreSQL Connection
=====================
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


###############################################################################
# PostgreSQLConnection
###############################################################################


class PostgreSQLConnection:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        url: str,
    ):

        self.url = url

        self.engine = None

        self.Session = None

    ###########################################################################
    # Connection
    ###########################################################################

    def connect(self):

        self.engine = create_engine(
            self.url,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=30,
        )

        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

        return self.engine

    ###########################################################################

    def disconnect(self):

        if self.engine:

            self.engine.dispose()

            self.engine = None

    ###########################################################################

    def session(self):

        return self.Session()

    ###########################################################################

    @property
    def is_connected(self):

        return self.engine is not None

    ###########################################################################

    def health(self):

        return {
            "healthy": self.is_connected,
            "url": self.url,
        }

    ###########################################################################

    def diagnostics(self):

        return {
            "engine": str(self.engine),
        }

    ###########################################################################

    def summary(self):

        return {
            "database": "PostgreSQL",
            "connected": self.is_connected,
        }


###############################################################################
# Utilities
###############################################################################


def connection_url(
    host: str,
    port: int,
    database: str,
    username: str,
    password: str,
):

    return (
        f"postgresql+psycopg://"
        f"{username}:{password}"
        f"@{host}:{port}/{database}"
    )