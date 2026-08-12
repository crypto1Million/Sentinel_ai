"""
PostgreSQL Session Manager
==========================
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

    @contextmanager
    def session(self) -> Generator:

        session = self.connection.Session()

        try:

            yield session

            session.commit()

        except Exception:

            session.rollback()

            raise

        finally:

            session.close()

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
        "autocommit": False,
        "autoflush": False,
    }