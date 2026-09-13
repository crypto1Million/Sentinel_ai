from __future__ import annotations

from typing import Any

from web3 import Web3

from chains.base_client import BaseClient


ZERO_ADDRESS = (
    "0x0000000000000000000000000000000000000000"
)


class BaseRugRadar:
    def __init__(
        self,
        client: BaseClient | None = None,
    ) -> None:
        self.client = client or BaseClient()

    def analyze(
        self,
        token: str,
        top10_percent: float = 0,
        pool_count: int = 0,
    ) -> dict[str, Any]:
        w3 = self.client.w3

        address = w3.to_checksum_address(
            token
        )

        code = self.client.get_code(
            address
        )

        has_code = len(code) > 2

        metadata = (
            self.client.token_metadata(
                address
            )
        )

        owner = metadata.get(
            "owner"
        )

        owner_renounced = (
            owner is not None
            and str(owner).lower()
            == ZERO_ADDRESS.lower()
        )

        bytecode = code.hex().lower()

        # Common capability selectors.
        mint_selector = "40c10f19"
        pause_selector = "8456cb59"
        upgrade_selector = "3659cfe6"

        mint_capability = (
            mint_selector in bytecode
        )

        pause_capability = (
            pause_selector in bytecode
        )

        upgrade_capability = (
            upgrade_selector in bytecode
        )

        risk = 10

        if not has_code:
            risk += 80

        if mint_capability:
            risk += 25

        if pause_capability:
            risk += 10

        if upgrade_capability:
            risk += 10

        if not owner_renounced and owner:
            risk += 5

        if pool_count == 0:
            risk += 20

        if top10_percent >= 50:
            risk += 15

        risk = max(
            0,
            min(
                100,
                risk,
            ),
        )

        if risk < 25:
            level = "LOW"
        elif risk < 50:
            level = "MEDIUM"
        elif risk < 75:
            level = "HIGH"
        else:
            level = "CRITICAL"

        return {
            "chain": "base",
            "token": address,
            "rug_score": risk,
            "risk_level": level,
            "contract_exists": has_code,
            "owner": owner,
            "ownership_renounced": owner_renounced,
            "mint_capability_detected": mint_capability,
            "pause_capability_detected": pause_capability,
            "upgrade_capability_detected": upgrade_capability,
            "liquidity_locked": None,
            "liquidity_burned": None,
        }