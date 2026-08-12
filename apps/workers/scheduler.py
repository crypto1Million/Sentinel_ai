import asyncio

from token_worker import TokenWorker
from score_worker import ScoreWorker
from wallet_worker import WalletWorker
from narrative_worker import NarrativeWorker
from rug_worker import RugWorker
from j7_worker import J7Worker
from discover_worker import DiscoverWorker
from alert_worker import AlertWorker
from portfolio_worker import PortfolioWorker


async def start_workers():

    await asyncio.gather(

        TokenWorker().run(),

        ScoreWorker().run(),

        WalletWorker().run(),

        NarrativeWorker().run(),

        RugWorker().run(),

        J7Worker().run(),

        DiscoverWorker().run(),

        AlertWorker().run(),

        PortfolioWorker().run()
    )


if __name__ == "__main__":

    asyncio.run(
        start_workers()
    )