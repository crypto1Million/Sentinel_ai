from ingestion.pumpfun_ingestor import PumpFunIngestor
from ingestion.raydium_ingestor import RaydiumIngestor
from ingestion.dexscreener_ingestor import DexScreenerIngestor


class TokenIngestionEngine:

    def __init__(self):

        self.pumpfun = PumpFunIngestor()

        self.raydium = RaydiumIngestor()

        self.dex = DexScreenerIngestor()

    async def run(self):

        pump_tokens = (
            await self.pumpfun
            .fetch_new_tokens()
        )

        raydium_pairs = (
            await self.raydium
            .fetch_pairs()
        )

        print(
            f"Pump Tokens: {len(pump_tokens)}"
        )

        print(
            f"Raydium Pairs: {len(raydium_pairs)}"
        )