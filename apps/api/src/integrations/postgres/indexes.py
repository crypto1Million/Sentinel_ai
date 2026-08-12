"""
Index Manager
=============
"""

from __future__ import annotations

from sqlalchemy import Index


###############################################################################
# IndexManager
###############################################################################


class IndexManager:

    def __init__(self):

        self.indexes = []

    ###########################################################################

    def register(self, index: Index):

        self.indexes.append(index)

    ###########################################################################

    def create_all(self, engine):

        for index in self.indexes:

            index.create(
                bind=engine,
                checkfirst=True,
            )

    ###########################################################################

    def drop_all(self, engine):

        for index in self.indexes:

            index.drop(
                bind=engine,
                checkfirst=True,
            )

    ###########################################################################

    def list_indexes(self):

        return [
            idx.name
            for idx in self.indexes
        ]

    ###########################################################################

    def diagnostics(self):

        return {
            "indexes": self.list_indexes(),
        }

    ###########################################################################

    def summary(self):

        return {
            "count": len(self.indexes),
        }


###############################################################################
# Utilities
###############################################################################


def build_index(name, *columns):

    return Index(name, *columns)