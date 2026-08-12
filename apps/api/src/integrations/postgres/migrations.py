"""
Alembic Migration Manager
=========================
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class MigrationManager:

    ###########################################################################

    def current(self):

        subprocess.run(
            ["alembic", "current"],
            check=False,
        )

    ###########################################################################

    def upgrade(self, revision="head"):

        subprocess.run(
            ["alembic", "upgrade", revision],
            check=True,
        )

    ###########################################################################

    def downgrade(self, revision):

        subprocess.run(
            ["alembic", "downgrade", revision],
            check=True,
        )

    ###########################################################################

    def revision(self, message):

        subprocess.run(
            [
                "alembic",
                "revision",
                "--autogenerate",
                "-m",
                message,
            ],
            check=True,
        )

    ###########################################################################

    def history(self):

        subprocess.run(
            ["alembic", "history"],
            check=False,
        )

    ###########################################################################

    def stamp(self, revision):

        subprocess.run(
            [
                "alembic",
                "stamp",
                revision,
            ],
            check=True,
        )

    ###########################################################################

    def diagnostics(self):

        return {
            "component": "MigrationManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "migration_tool": "Alembic",
        }


###############################################################################
# Utilities
###############################################################################


def migration_directory():

    return Path("alembic")