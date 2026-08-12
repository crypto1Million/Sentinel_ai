###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from contextlib import contextmanager
from queue import Queue
from threading import Lock
from typing import Any

###############################################################################
# DatabaseSession
###############################################################################


class DatabaseSession:
    """
    Database session manager.
    """

    def __init__(self) -> None:
        self._session: Any = None
        self._active_sessions = 0
        self._lock = Lock()

    ###########################################################################
    # Session Management
    ###########################################################################

    def create_session(self) -> Any:
        """
        Create a new session.
        """

        with self._lock:
            self._active_sessions += 1

        self._session = object()

        return self._session

    ###########################################################################

    def get_session(self) -> Any:
        """
        Return current session.
        """

        if self._session is None:
            return self.create_session()

        return self._session

    ###########################################################################

    def close_session(self) -> None:
        """
        Close session.
        """

        with self._lock:
            self._active_sessions = max(
                0,
                self._active_sessions - 1,
            )

        self._session = None

    ###########################################################################

    def reset_session(self) -> Any:
        """
        Reset session.
        """

        self.close_session()

        return self.create_session()

    ###########################################################################

    @contextmanager
    def session_scope(self):
        """
        Session context.
        """

        session = self.get_session()

        try:
            yield session

        finally:
            self.close_session()

    ###########################################################################

    def active_sessions(self) -> int:
        """
        Active session count.
        """

        return self._active_sessions

    ###########################################################################

    def diagnostics(self) -> dict:
        """
        Session diagnostics.
        """

        return {
            "active_sessions": self._active_sessions,
            "session_exists": self._session is not None,
        }


###############################################################################
# Connection Pool
###############################################################################

_connection_pool: Queue = Queue()


def initialize_pool(
    size: int = 10,
) -> None:
    """
    Initialize connection pool.
    """

    while not _connection_pool.empty():
        _connection_pool.get()

    for _ in range(size):
        _connection_pool.put(object())


###############################################################################


def acquire() -> Any:
    """
    Acquire pooled connection.
    """

    return _connection_pool.get()


###############################################################################


def release(
    connection: Any,
) -> None:
    """
    Return connection to pool.
    """

    _connection_pool.put(connection)


###############################################################################


def pool_statistics() -> dict:
    """
    Pool information.
    """

    return {
        "available_connections": _connection_pool.qsize(),
    }


###############################################################################


def cleanup_pool() -> None:
    """
    Cleanup pool.
    """

    while not _connection_pool.empty():
        _connection_pool.get()


###############################################################################
# Runtime
###############################################################################


def summary() -> dict:
    """
    Runtime summary.
    """

    return {
        "module": "session",
        "pool_size": _connection_pool.qsize(),
    }


###############################################################################
# Utilities
###############################################################################


def verify_session(
    session: Any,
) -> bool:
    """
    Verify session.
    """

    return session is not None


###############################################################################


def session_metadata(
    session: Any,
) -> dict:
    """
    Session metadata.
    """

    return {
        "id": id(session),
        "valid": verify_session(session),
    }