from __future__ import annotations

from typing import Any

from web3 import Web3

from chains.base_client import BaseClient


TRANSFER_TOPIC = Web3.keccak(
    text="Transfer(address,address,uint256)"
).hex()


class BaseHolderIntelligence:
    def __init__(
        self,
        client: BaseClient | None = None,
    ) -> None:
        self.client = client or BaseClient()

    def discover_recent_wallets(
        self,
        token: str,
        block_window: int = 500,
    ) -> list[str]:
        w3 = self.client.w3

        latest = w3.eth.block_number

        logs = w3.eth.get_logs(
            {
                "address": w3.to_checksum_address(
                    token
                ),
                "fromBlock": max(
                    0,
                    latest - block_window,
                ),
                "toBlock": latest,
                "topics": [
                    TRANSFER_TOPIC
                ],
            }
        )

        wallets: set[str] = set()

        for log in logs:
            if len(log["topics"]) < 3:
                continue

            from_topic = (
                log["topics"][1].hex()
            )

            to_topic = (
                log["topics"][2].hex()
            )

            sender = (
                "0x"
                + from_topic[-40:]
            )

            recipient = (
                "0x"
                + to_topic[-40:]
            )

            if int(sender, 16) != 0:
                wallets.add(
                    Web3.to_checksum_address(
                        sender
                    )
                )

            if int(recipient, 16) != 0:
                wallets.add(
                    Web3.to_checksum_address(
                        recipient
                    )
                )

        return list(wallets)

    def analyze(
        self,
        token: str,
        block_window: int = 500,
    ) -> dict[str, Any]:
        metadata = self.client.token_metadata(
            token
        )

        wallets = self.discover_recent_wallets(
            token,
            block_window,
        )

        total_supply = int(
            metadata["total_supply"]
        )

        holders = []

        for wallet in wallets:
            try:
                balance = self.client.token_balance(
                    token,
                    wallet,
                )
            except Exception:
                continue

            percentage = (
                (
                    balance
                    / total_supply
                )
                * 100
                if total_supply > 0
                else 0
            )

            if balance > 0:
                holders.append(
                    {
                        "wallet": wallet,
                        "balance": str(balance),
                        "percentage": round(
                            percentage,
                            4,
                        ),
                    }
                )

        holders.sort(
            key=lambda item: int(
                item["balance"]
            ),
            reverse=True,
        )

        top10 = sum(
            item["percentage"]
            for item in holders[:10]
        )

        top25 = sum(
            item["percentage"]
            for item in holders[:25]
        )

        return {
            "chain": "base",
            "token": token,
            "holders": holders,
            "top10_percent": round(
                top10,
                2,
            ),
            "top25_percent": round(
                top25,
                2,
            ),
            "windowed": True,
        }