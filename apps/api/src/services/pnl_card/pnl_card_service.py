from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class PNLCardResult:
    image_path: str
    pnl_sol: float
    pnl_usd: float
    pnl_percent: float


class PNLCardService:
    """Generate a local PNG summary for an already-closed trade."""

    def __init__(self, output_dir: str | Path = "data/pnl_cards") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get(obj: Any, key: str, default: Any = None) -> Any:
        return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

    @staticmethod
    def _font(size: int) -> ImageFont.ImageFont:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size=size)
        except OSError:
            return ImageFont.load_default()

    @staticmethod
    def _safe_number(value: Any, field: str) -> float:
        try:
            number = float(value or 0)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field} must be numeric") from exc
        if not (number == number and abs(number) != float("inf")):
            raise ValueError(f"{field} must be finite")
        return number

    async def generate_for_closed_trade(
        self,
        trade: Any,
        sol_usd_price: float | None = None,
    ) -> PNLCardResult:
        entry_price = self._safe_number(self._get(trade, "entry_price"), "entry_price")
        exit_price = self._safe_number(self._get(trade, "exit_price"), "exit_price")
        quantity = self._safe_number(self._get(trade, "quantity", self._get(trade, "token_amount", 0)), "quantity")
        entry_sol = self._safe_number(self._get(trade, "entry_value_sol", self._get(trade, "entry_sol", 0)), "entry_value_sol")
        exit_sol = self._safe_number(self._get(trade, "exit_value_sol", self._get(trade, "exit_sol", 0)), "exit_value_sol")
        if entry_sol or exit_sol:
            pnl_sol = exit_sol - entry_sol
        elif entry_price and exit_price and quantity:
            pnl_sol = (exit_price - entry_price) * quantity
        else:
            raise ValueError("Trade must include entry/exit SOL values or prices and quantity")
        pnl_percent = (pnl_sol / entry_sol * 100) if entry_sol else (((exit_price - entry_price) / entry_price) * 100 if entry_price else 0.0)
        usd_price = self._safe_number(sol_usd_price, "sol_usd_price") if sol_usd_price is not None else 0.0
        pnl_usd = pnl_sol * usd_price
        token_name = str(self._get(trade, "token_name", self._get(trade, "symbol", "UNKNOWN")))
        symbol = str(self._get(trade, "symbol", token_name))
        chain = str(self._get(trade, "chain", "solana")).upper()
        trader = str(self._get(trade, "trader_handle", "SentinelAI"))
        closed_at = self._get(trade, "closed_at", datetime.now(timezone.utc))
        if isinstance(closed_at, str):
            try:
                closed_at = datetime.fromisoformat(closed_at.replace("Z", "+00:00"))
            except ValueError:
                closed_at = datetime.now(timezone.utc)
        if not isinstance(closed_at, datetime):
            closed_at = datetime.now(timezone.utc)
        image = self._build_card(token_name, symbol, chain, trader, pnl_sol, pnl_usd, pnl_percent, entry_price, exit_price, closed_at)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        safe_symbol = "".join(c for c in symbol if c.isalnum() or c in "-_") or "token"
        output = self.output_dir / f"{timestamp}_{safe_symbol}_pnl.png"
        image.save(output, format="PNG", optimize=True)
        return PNLCardResult(str(output), pnl_sol, pnl_usd, pnl_percent)

    def _build_card(
        self,
        token_name: str,
        symbol: str,
        chain: str,
        trader: str,
        pnl_sol: float,
        pnl_usd: float,
        pnl_percent: float,
        entry_price: float,
        exit_price: float,
        closed_at: datetime,
    ) -> Image.Image:
        width, height = 1400, 800
        image = Image.new("RGB", (width, height), "#080B10")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((40, 40, width - 40, height - 40), radius=32, fill="#11161D", outline="#27303B", width=2)
        draw.text((90, 75), "SENTINELAI", font=self._font(42), fill="#F5F7FA")
        draw.text((90, 135), "TRADE PERFORMANCE", font=self._font(22), fill="#778391")
        draw.text((90, 235), token_name[:38], font=self._font(42), fill="#FFFFFF")
        draw.text((90, 295), f"${symbol[:20]}  ·  {chain}", font=self._font(25), fill="#8B98A7")
        positive = pnl_sol >= 0
        pnl_color = "#39E58C" if positive else "#FF5364"
        prefix = "+" if positive else ""
        headline = f"{prefix}${abs(pnl_usd):,.2f}" if pnl_usd else f"{prefix}{pnl_sol:.4f} SOL"
        draw.text((90, 430), headline, font=self._font(68), fill=pnl_color)
        draw.text((92, 525), f"{prefix}{pnl_percent:.2f}%", font=self._font(38), fill=pnl_color)
        draw.text((90, 640), "ENTRY", font=self._font(22), fill="#778391")
        draw.text((90, 680), f"{entry_price:.10g}", font=self._font(30), fill="#FFFFFF")
        draw.text((470, 640), "EXIT", font=self._font(22), fill="#778391")
        draw.text((470, 680), f"{exit_price:.10g}", font=self._font(30), fill="#FFFFFF")
        draw.text((940, 660), trader[:26], font=self._font(26), fill="#FFFFFF")
        draw.text((940, 705), closed_at.strftime("%b %d, %Y %H:%M UTC"), font=self._font(18), fill="#778391")
        return image

