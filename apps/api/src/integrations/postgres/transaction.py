"""
Transaction Manager
===================
"""

from __future__ import annotations

from contextlib import contextmanager


###############################################################################
# TransactionManager
###############################################################################


class TransactionManager:

    def __init__(self, session):

        self.session = session

    ###########################################################################

    @contextmanager
    def transaction(self):

        try:

            yield self.session

            self.session.commit()

        except Exception:

            self.session.rollback()

            raise

    ###########################################################################

    def begin(self):

        return self.session.begin()

    ###########################################################################

    def commit(self):

        self.session.commit()

    ###########################################################################

    def rollback(self):

        self.session.rollback()

    ###########################################################################

    def diagnostics(self):

        return {
            "transactions": "enabled",
        }

    ###########################################################################

    def summary(self):

        return {
            "status": "ready",
        }


###############################################################################
# Utilities
###############################################################################


def transaction_metadata():

    return {
        "atomic": True,
    }