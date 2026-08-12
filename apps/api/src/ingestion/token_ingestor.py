from sqlalchemy.orm import Session

from models.token import Token

from services.helius import HeliusClient
from services.dexscreener import DexScreenerClient


class TokenIngestor:

    def __init__(self):

        self.helius = HeliusClient()
        self.dex = DexScreenerClient()

    async def ingest(
        self,
        db: Session,
        mint_address: str
    ):

        existing = (
            db.query(Token)
            .filter(
                Token.mint_address == mint_address
            )
            .first()
        )

        if existing:
            return existing

        asset = await self.helius.get_asset(
            mint_address
        )

        result = asset.get("result", {})

        token = Token(
            mint_address=mint_address,
            symbol=result.get("symbol"),
            name=result.get("name"),
        )

        db.add(token)
        db.commit()
        db.refresh(token)

        return token