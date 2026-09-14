from __future__ import annotations

from typing import Any

from chains.evm.client import EVMClient
from chains.models import ChainAdapter, ChainConfig


class EVMChainAdapter:
    def __init__(
        self,
        config: ChainConfig,
    ) -> None:
        self.config = config
        self.client = EVMClient(config)

    async def health(self) -> dict[str, Any]:
        return await self.client.health()

    async def quote(
        self,
        input_token: str,
        output_token: str,
        amount: str,
        wallet: str | None = None,
        slippage_bps: int = 50,
    ) -> dict[str, Any]:
        return {
            "status": "adapter_ready",
            "chain": self.config.id.value,
            "input_token": input_token,
            "output_token": output_token,
            "amount": amount,
            "wallet": wallet,
            "slippage_bps": slippage_bps,
        }

    async def build_swap(
        self,
        input_token: str,
        output_token: str,
        amount: str,
        wallet: str,
        slippage_bps: int,
        priority_fee: int | None = None,
        jito_tip: int | None = None,
    ) -> dict[str, Any]:
        return {
            "status": "awaiting_evm_adapter",
            "chain": self.config.id.value,
            "wallet": wallet,
            "input_token": input_token,
            "output_token": output_token,
            "amount": amount,
            "slippage_bps": slippage_bps,
            "priority_fee": priority_fee,
        }

    async def execute(
        self,
        signed_transaction: str,
        request_id: str,
    ) -> dict[str, Any]:
        raise NotImplementedError(
            f"EVM execution adapter is not "
            f"implemented for {self.config.id.value}"
        )