import asyncio
import logging
from datetime import datetime
from typing import Dict, List

from .watchlist_repository import WatchlistRepository

from apps.api.src.services.dexscreener import DexScreenerService
from apps.api.src.services.helius import HeliusService
from apps.api.src.services.pumpfun import PumpFunService
from apps.api.src.services.raydium import RaydiumService

logger = logging.getLogger(__name__)


class WatchlistSync:

    """
    Synchronizes every token inside user watchlists with
    live blockchain and market data.
    """

    def __init__(
        self,
        repository: WatchlistRepository,
    ):

        self.repository = repository

        self.dex = DexScreenerService()

        self.helius = HeliusService()

        self.pumpfun = PumpFunService()

        self.raydium = RaydiumService()

        self.running = False

        self.interval = 5

    # --------------------------------------------------

    async def sync_watchlist(
        self,
        watchlist_id: str
    ) -> List[Dict]:

        results = []

        tokens = self.repository.get_tokens(
            watchlist_id
        )

        for token in tokens:

            data = await self.sync_token(
                token.mint
            )

            results.append(data)

        return results

    # --------------------------------------------------

    async def sync_token(
        self,
        mint: str
    ) -> Dict:

        logger.info(f"Syncing {mint}")

        dex = await self.dex.get_token(mint)

        holders = await self.helius.get_token_holders(
            mint
        )

        pump = await self.pumpfun.get_token(
            mint
        )

        raydium = await self.raydium.get_pool(
            mint
        )

        return {

            "mint": mint,

            "price":
                dex.get("price"),

            "market_cap":
                dex.get("market_cap"),

            "volume":
                dex.get("volume"),

            "liquidity":
                dex.get("liquidity"),

            "holders":
                holders,

            "pumpfun":
                pump,

            "raydium":
                raydium,

            "updated_at":
                datetime.utcnow()

        }

    # --------------------------------------------------

    async def sync_all(
        self,
        user_id: str
    ):

        watchlists = self.repository.get_user_watchlists(
            user_id
        )

        synced = {}

        for watchlist in watchlists:

            synced[
                watchlist.id
            ] = await self.sync_watchlist(
                watchlist.id
            )

        return synced

    # --------------------------------------------------

    async def run_forever(
        self,
        user_id: str
    ):

        self.running = True

        logger.info(
            "Watchlist Sync Started"
        )

        while self.running:

            try:

                await self.sync_all(
                    user_id
                )

            except Exception as e:

                logger.exception(e)

            await asyncio.sleep(
                self.interval
            )

    # --------------------------------------------------

    def stop(self):

        self.running = False