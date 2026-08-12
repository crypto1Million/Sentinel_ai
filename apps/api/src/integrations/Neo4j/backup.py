"""
Neo4j Backup Manager
====================
"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


class Neo4jBackup:

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self, backup_dir: str):

        self.backup_dir = Path(backup_dir)

        self.backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    ###########################################################################
    # Backup
    ###########################################################################

    def create_backup(self):

        filename = (
            self.backup_dir
            / f"neo4j_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.dump"
        )

        return filename

    ###########################################################################

    def backup_database(self):

        backup_file = self.create_backup()

        command = [
            "neo4j-admin",
            "database",
            "dump",
            "neo4j",
            f"--to-path={backup_file.parent}",
        ]

        subprocess.run(
            command,
            check=False,
        )

        return backup_file

    ###########################################################################

    def restore_database(
        self,
        dump_file: str,
    ):

        command = [
            "neo4j-admin",
            "database",
            "load",
            "neo4j",
            f"--from-path={dump_file}",
            "--overwrite-destination=true",
        ]

        subprocess.run(
            command,
            check=False,
        )

    ###########################################################################

    def list_backups(self):

        return sorted(
            self.backup_dir.glob("*.dump")
        )

    ###########################################################################

    def delete_backup(
        self,
        backup_name: str,
    ):

        file = self.backup_dir / backup_name

        if file.exists():

            file.unlink()

    ###########################################################################

    def diagnostics(self):

        return {
            "backups": len(self.list_backups()),
        }

    ###########################################################################

    def summary(self):

        return {
            "backup_directory": str(self.backup_dir),
        }


###############################################################################
# Utilities
###############################################################################


def backup_metadata():

    return {
        "extension": ".dump",
    }