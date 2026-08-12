"""
Reusable PostgreSQL Queries
===========================
"""

from __future__ import annotations

from sqlalchemy import text


###############################################################################
# QueryManager
###############################################################################


class QueryManager:

    def __init__(self, session):

        self.session = session

    ###########################################################################

    def execute(self, sql: str, params=None):

        return self.session.execute(
            text(sql),
            params or {},
        )

    ###########################################################################

    def fetch_one(self, sql: str, params=None):

        return self.execute(sql, params).first()

    ###########################################################################

    def fetch_all(self, sql: str, params=None):

        return self.execute(sql, params).all()

    ###########################################################################

    def scalar(self, sql: str, params=None):

        return self.execute(sql, params).scalar()

    ###########################################################################

    def diagnostics(self):

        return {
            "query_manager": "ready",
        }

    ###########################################################################

    def summary(self):

        return {
            "status": "active",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_rows(rows):

    return [dict(r._mapping) for r in rows]