from __future__ import annotations

from config.settings import get_settings
from chains.models import Chain
from providers.evm.base_ws import EVMWebSocketAdapter


class RobinhoodWebSocketAdapter(
    EVMWebSocketAdapter
):
    """
    Robinhood Chain realtime EVM adapter.

    Uses the configured production WSS provider.
    """

    def __init__(
        self,
        *,
        extra_contract_addresses: tuple[str, ...] = (),
    ) -> None:
        settings = get_settings()

        registry_addresses = (
            self._registry_addresses()
        )

        super().__init__(
            chain=Chain.ROBINHOOD,
            wss_url=settings.ROBINHOOD_WSS_URL,
            source="robinhood.wss",
            contract_addresses=tuple(
                set(
                    registry_addresses
                ).union(
                    extra_contract_addresses
                )
            ),
            stream_semantics="robinhood_wss",
        )