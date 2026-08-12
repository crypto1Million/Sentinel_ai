"""
Database Backup Manager
=======================
"""

from __future__ import annotations

import subprocess
from pathlib import Path


###############################################################################
# BackupManager
###############################################################################


class BackupManager:

    def __init__(
        self,
        database_url: str,
    ):

        self.database_url = database_url

    ###########################################################################

    def backup(
        self,
        output_file: str,
    ):

        subprocess.run(
            [
                "pg_dump",
                self.database_url,
                "-f",
                output_file,
            ],
            check=True,
        )

        return output_file

    ###########################################################################

    def restore(
        self,
        backup_file: str,
    ):

        subprocess.run(
            [
                "psql",
                self.database_url,
                "-f",
                backup_file,
            ],
            check=True,
        )

    ###########################################################################

    def archive(
        self,
        directory: str,
    ):

        return list(
            Path(directory).glob("*.sql")
        )

    ###########################################################################

    def diagnostics(self):

        return {
            "component": "BackupManager",
        }

    ###########################################################################

    def summary(self):

        return {
            "backup": "enabled",
        }


###############################################################################
# Utilities
###############################################################################


def backup_filename():

    from datetime import datetime

    return (
        f"backup_"
        f"{datetime.utcnow():%Y%m%d_%H%M%S}.sql"
    )