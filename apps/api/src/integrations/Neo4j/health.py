"""
Neo4j Health Monitoring
=======================
"""

from __future__ import annotations

from datetime import datetime


class Neo4jHealth:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, connection):

        self.connection = connection

    ###########################################################################
    # Health Checks
    ###########################################################################

    def ping(self):

        try:

            with self.connection.session() as session:

                session.run("RETURN 1")

            return True

        except Exception:

            return False

    ###########################################################################

    def connectivity(self):

        return {
            "connected": self.connection.is_connected,
            "healthy": self.ping(),
        }

    ###########################################################################

    def database_status(self):

        try:

            with self.connection.session() as session:

                result = session.run(
                    "CALL db.info()"
                ).single()

            return dict(result)

        except Exception as e:

            return {"error": str(e)}

    ###########################################################################

    def node_count(self):

        with self.connection.session() as session:

            return session.run(
                """
                MATCH (n)
                RETURN count(n) AS nodes
                """
            ).single()["nodes"]

    ###########################################################################

    def relationship_count(self):

        with self.connection.session() as session:

            return session.run(
                """
                MATCH ()-[r]->()
                RETURN count(r) AS relationships
                """
            ).single()["relationships"]

    ###########################################################################

    def diagnostics(self):

        return {
            "database": self.database_status(),
            "nodes": self.node_count(),
            "relationships": self.relationship_count(),
            "healthy": self.ping(),
        }

    ###########################################################################

    def summary(self):

        return {
            "neo4j": "healthy" if self.ping() else "offline",
            "timestamp": datetime.utcnow().isoformat(),
        }


###############################################################################
# Utilities
###############################################################################


def health_metadata():

    return {
        "provider": "Neo4j",
    }