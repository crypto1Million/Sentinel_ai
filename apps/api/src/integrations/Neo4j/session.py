"""
Neo4j Session Manager
=====================
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator


class SessionManager:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, connection):

        self.connection = connection

    ###########################################################################
    # Sessions
    ###########################################################################

    @contextmanager
    def session(self) -> Generator:

        session = self.connection.driver.session()

        try:

            yield session

        finally:

            session.close()

    ###########################################################################

    @contextmanager
    def write_session(self):

        session = self.connection.driver.session()

        try:

            yield session

        finally:

            session.close()

    ###########################################################################

    @contextmanager
    def read_session(self):

        session = self.connection.driver.session()

        try:

            yield session

        finally:

            session.close()

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {
            "component": "SessionManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "sessions": "managed",
        }


###############################################################################
# Utilities
###############################################################################


def session_metadata():

    return {
        "provider": "Neo4j",
    }