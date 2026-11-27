from __future__ import annotations

import asyncio
import logging

from config.logging import setup_logging
from config.settings import get_settings

from ingestion.token_ingestion_engine import (
    TokenIngestionEngine,
)

from intelligence.worker import IntelligenceWorker

from ingestion.elysium_deployment_scanner import (
    ElysiumDeploymentScanner,
)


async def main() -> None:
    setup_logging()

    settings = get_settings()

    tasks = [
        asyncio.create_task(
            IntelligenceWorker().run(),
            name="sentinel-event-pipeline",
        ),

        asyncio.create_task(
            TokenIngestionEngine().run_forever(),
            name="sentinel-pumpfun-ingestion",
        ),
    ]

    if settings.ELYSIUM_RPC_URL:
        tasks.append(
            asyncio.create_task(
                ElysiumDeploymentScanner().run_forever(),
                name="sentinel-elysium-ingestion",
            )
        )

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO
    )

    asyncio.run(main())