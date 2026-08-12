from dataclasses import dataclass
from typing import List


@dataclass
class BlockTrade:
    slot: int
    signature: str
    wallet: str
    token: str
    side: str
    amount: float
    timestamp: int


class BlockAnalyzer:

    def analyze(self, trades: List[BlockTrade]):

        trades = sorted(trades, key=lambda x: x.timestamp)

        return {
            "total_transactions": len(trades),
            "first_trade": trades[0].timestamp if trades else None,
            "last_trade": trades[-1].timestamp if trades else None,
            "wallets": len(set(t.wallet for t in trades))
        }