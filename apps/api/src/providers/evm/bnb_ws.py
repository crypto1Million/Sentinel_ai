from __future__ import annotations

from collections.abc import Sequence

from config.settings import get_settings
from providers.evm.base_ws import EVMWebSocketAdapter


class BNBWebSocketAdapter(
    EVMWebSocketAdapter
):
    """
    BNB Smart Chain Mainnet realtime chain observer.
    """

    def __init__(
        self,
        *,
        log_addresses: Sequence[str] | None = None,
        log_topics: Sequence[str | None] | None = None,
    ) -> None:
        settings = get_settings()

        wss_url = (
            settings.BNB_WSS_URL
            or self._build_alchemy_url(
                settings.ALCHEMY_API_KEY
            )
        )

        super().__init__(
            chain="bnb",
            chain_id=settings.BNB_CHAIN_ID,
            wss_url=wss_url,
            provider_name="alchemy",
            log_addresses=log_addresses,
            log_topics=log_topics,
            reconnect_delay_seconds=(
                settings.REALTIME_RECONNECT_DELAY_SECONDS
            ),
            max_reconnect_delay_seconds=(
                settings.REALTIME_MAX_RECONNECT_DELAY_SECONDS
            ),
            heartbeat_seconds=(
                settings.REALTIME_HEARTBEAT_SECONDS
            ),
        )

    @staticmethod
    def _build_alchemy_url(
        api_key: str,
    ) -> str:
        if not api_key.strip():
            return ""

        return (
            "wss://bnb-mainnet.g.alchemy.com/v2/"
            f"{api_key.strip()}"
        )