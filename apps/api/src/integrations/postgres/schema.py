"""
Database Schema Utilities
=========================
"""

from __future__ import annotations

from sqlalchemy import MetaData


###############################################################################
# DatabaseSchema
###############################################################################


class DatabaseSchema:

    ###########################################################################

    def __init__(self, metadata: MetaData):

        self.metadata = metadata

    ###########################################################################

    def create_all(self, engine):

        self.metadata.create_all(engine)

    ###########################################################################

    def drop_all(self, engine):

        self.metadata.drop_all(engine)

    ###########################################################################

    def tables(self):

        return list(self.metadata.tables.keys())

    ###########################################################################

    def table(self, name: str):

        return self.metadata.tables.get(name)

    ###########################################################################

    def exists(self, name: str):

        return name in self.metadata.tables

    ###########################################################################

    def diagnostics(self):

        return {
            "tables": self.tables(),
            "count": len(self.tables()),
        }

    ###########################################################################

    def summary(self):

        return {
            "schema": "loaded",
        }


###############################################################################
# Utilities
###############################################################################


def metadata_summary(metadata: MetaData):

    return {
        "tables": list(metadata.tables.keys()),
    }