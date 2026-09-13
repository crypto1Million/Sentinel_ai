from __future__ import annotations

from typing import Any

from chains.base_client import BaseClient


class BaseTokenIngestion:
    def __init__(
        self,
        client: BaseClient | None = None,
    ) -> None:
        self.client = client or BaseClient()

    def ingest(
        self,
        token: str,
    ) -> dict[str, Any]:
        return self.client.token_metadata(token)