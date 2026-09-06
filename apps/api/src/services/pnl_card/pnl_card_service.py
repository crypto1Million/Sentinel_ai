```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


@dataclass
class PNLCardResult:
    """
    Result returned after generating a PNL card.
    """

    image_path: str
    pnl_sol: float
    pnl_usd: float
    pnl_percent: float


class PNLCardService:
    """
    Generates SentinelAI PNL cards for closed trades.

    Responsibilities:
    - Calculate/display PNL information.
    - Generate the PNL card image.
    - Optionally include a token image.
    - Return the generated image path.

    It does NOT execute trades or manage positions.
    """

    def __init__(
        self,
        output_dir: str | Path = "data/pnl_cards",
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.font_regular = self._load_font(30)
        self.font_small = self._load_font(24)
        self.font_medium = self._load_font(36)
        self.font_large = self._load_font(64)
        self.font_title = self._load_font(42)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    async def generate_for_closed_trade(
        self,
        trade: Any,
        sol_usd_price: float | None = None,
    ) -> PNLCardResult:

        entry_price = float(
            self._get(trade, "entry_price", 0)
        )

        exit_price = float(
            self._get(trade, "exit_price", 0)
        )

        quantity = float(
            self._get(
                trade,
                "quantity",
                self._get(trade, "token_amount", 0),
            )
        )

        entry_value_sol = float(
            self._get(
                trade,
                "entry_value_sol",
                self._get(trade, "entry_sol", 0),
            )
        )

        exit_value_sol = float(
            self._get(
                trade,
                "exit_value_sol",
                self._get(trade, "exit_sol", 0),
            )
        )
        
        logo = logo.resize((140, 40))

        canvas.alpha_composite(
            logo,
            (40, 30),
        )
        
        # -----------------------------------------------------
        # Calculate PNL
        # -----------------------------------------------------

        if entry_value_sol and exit_value_sol:
            pnl_sol = exit_value_sol - entry_value_sol

        elif entry_price and exit_price and quantity:
            pnl_sol = (
                exit_price - entry_price
            ) * quantity

        else:
            pnl_sol = 0.0

        if entry_value_sol:
            pnl_percent = (
                pnl_sol / entry_value_sol
            ) * 100

        elif entry_price:
            pnl_percent = (
                (exit_price - entry_price)
                / entry_price
            ) * 100

        else:
            pnl_percent = 0.0

        pnl_usd = (
            pnl_sol * sol_usd_price
            if sol_usd_price is not None
            else 0.0
        )

        # -----------------------------------------------------
        # Token metadata
        # -----------------------------------------------------

        token_name = str(
            self._get(
                trade,
                "token_name",
                self._get(
                    trade,
                    "symbol",
                    "UNKNOWN",
                ),
            )
        )

        symbol = str(
            self._get(
                trade,
                "symbol",
                token_name,
            )
        )

        image_url = self._get(
            trade,
            "image_url",
            self._get(
                trade,
                "token_image_url",
                None,
            ),
        )

        trader_handle = str(
            self._get(
                trade,
                "trader_handle",
                "SentinelAI",
            )
        )

        chain = str(
            self._get(
                trade,
                "chain",
                "SOL",
            )
        )

        closed_at = self._get(
            trade,
            "closed_at",
            datetime.utcnow(),
        )

        # -----------------------------------------------------
        # Generate image
        # -----------------------------------------------------

        image = await self._build_card(
            token_name=token_name,
            symbol=symbol,
            pnl_sol=pnl_sol,
            pnl_usd=pnl_usd,
            pnl_percent=pnl_percent,
            entry_price=entry_price,
            exit_price=exit_price,
            trader_handle=trader_handle,
            chain=chain,
            image_url=image_url,
            closed_at=closed_at,
        )

        # -----------------------------------------------------
        # Save
        # -----------------------------------------------------

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        safe_symbol = "".join(
            character
            for character in symbol
            if character.isalnum()
            or character in ("-", "_")
        )

        if not safe_symbol:
            safe_symbol = "token"

        filename = (
            f"{timestamp}_{safe_symbol}_pnl.png"
        )

        output_path = (
            self.output_dir / filename
        )

        image.save(
            output_path,
            format="PNG",
            optimize=True,
        )

        return PNLCardResult(
            image_path=str(output_path),
            pnl_sol=pnl_sol,
            pnl_usd=pnl_usd,
            pnl_percent=pnl_percent,
        )

    # ---------------------------------------------------------
    # Card builder
    # ---------------------------------------------------------

    async def _build_card(
        self,
        token_name: str,
        symbol: str,
        pnl_sol: float,
        pnl_usd: float,
        pnl_percent: float,
        entry_price: float,
        exit_price: float,
        trader_handle: str,
        chain: str,
        image_url: str | None,
        closed_at: datetime,
    ) -> Image.Image:

        width = 1400
        height = 800

        image = Image.new(
            "RGB",
            (width, height),
            "#080B10",
        )

        draw = ImageDraw.Draw(image)

        # -----------------------------------------------------
        # Background panels
        # -----------------------------------------------------

        draw.rounded_rectangle(
            (40, 40, width - 40, height - 40),
            radius=32,
            fill="#11161D",
            outline="#27303B",
            width=2,
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        draw.text(
            (90, 75),
            "SENTINELAI",
            font=self.font_title,
            fill="#F5F7FA",
        )

        draw.text(
            (90, 130),
            "TRADE PERFORMANCE",
            font=self.font_small,
            fill="#6F7B88",
        )

        # -----------------------------------------------------
        # Token information
        # -----------------------------------------------------

        token_image = None

        if image_url:
            token_image = await self._download_image(
                image_url
            )

        if token_image:
            token_image = self._prepare_token_image(
                token_image,
                size=150,
            )

            image.paste(
                token_image,
                (90, 210),
                token_image,
            )

            token_x = 280

        else:
            token_x = 90

        draw.text(
            (token_x, 215),
            token_name,
            font=self.font_title,
            fill="#FFFFFF",
        )

        draw.text(
            (token_x, 270),
            f"${symbol}",
            font=self.font_medium,
            fill="#8B98A7",
        )

        draw.text(
            (token_x, 325),
            f"{chain} • CLOSED TRADE",
            font=self.font_small,
            fill="#687482",
        )

        # -----------------------------------------------------
        # PNL
        # -----------------------------------------------------

        positive = pnl_sol >= 0

        pnl_color = (
            "#39E58C"
            if positive
            else "#FF5364"
        )

        pnl_prefix = "+" if positive else ""

        pnl_text = (
            f"{pnl_prefix}${abs(pnl_usd):,.2f}"
            if pnl_usd
            else f"{pnl_prefix}{pnl_sol:.4f} SOL"
        )

        draw.text(
            (90, 430),
            pnl_text,
            font=self.font_large,
            fill=pnl_color,
        )

        draw.text(
            (90, 510),
            f"{pnl_prefix}{pnl_percent:.2f}%",
            font=self.font_medium,
            fill=pnl_color,
        )

        # -----------------------------------------------------
        # Entry / Exit
        # -----------------------------------------------------

        info_y = 625

        draw.text(
            (90, info_y),
            "ENTRY",
            font=self.font_small,
            fill="#697582",
        )

        draw.text(
            (90, info_y + 42),
            self._format_price(entry_price),
            font=self.font_medium,
            fill="#FFFFFF",
        )

        draw.text(
            (450, info_y),
            "EXIT",
            font=self.font_small,
            fill="#697582",
        )

        draw.text(
            (450, info_y + 42),
            self._format_price(exit_price),
            font=self.font_medium,
            fill="#FFFFFF",
        )

        # -----------------------------------------------------
        # Footer
        # -----------------------------------------------------

        footer = (
            f"@{trader_handle}"
            if not trader_handle.startswith("@")
            else trader_handle
        )

        draw.text(
            (950, 665),
            footer,
            font=self.font_medium,
            fill="#FFFFFF",
        )

        draw.text(
            (950, 710),
            closed_at.strftime(
                "%B %d, %Y"
            ),
            font=self.font_small,
            fill="#687482",
        )

        return image

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _get(
        obj: Any,
        key: str,
        default: Any = None,
    ) -> Any:

        if isinstance(obj, dict):
            return obj.get(key, default)

        return getattr(
            obj,
            key,
            default,
        )

    @staticmethod
    def _format_price(
        price: float,
    ) -> str:

        if price >= 1:
            return f"${price:,.4f}"

        if price >= 0.000001:
            return f"${price:.8f}"

        return f"${price:.12f}"

    @staticmethod
    def _load_font(
        size: int,
    ):

        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]

        for path in font_paths:
            try:
                return ImageFont.truetype(
                    path,
                    size,
                )
            except OSError:
                continue

        return ImageFont.load_default()

    @staticmethod
    def _prepare_token_image(
        token_image: Image.Image,
        size: int,
    ) -> Image.Image:

        token_image = token_image.convert(
            "RGBA"
        )

        token_image.thumbnail(
            (size, size)
        )

        canvas = Image.new(
            "RGBA",
            (size, size),
            (0, 0, 0, 0),
        )

        x = (
            size - token_image.width
        ) // 2

        y = (
            size - token_image.height
        ) // 2

        canvas.paste(
            token_image,
            (x, y),
            token_image,
        )

        return canvas

    @staticmethod
    async def _download_image(
        image_url: str,
    ) -> Image.Image | None:

        try:
            import httpx

            async with httpx.AsyncClient(
                timeout=10.0,
                follow_redirects=True,
            ) as client:

                response = await client.get(
                    image_url
                )

                response.raise_for_status()

                from io import BytesIO

                return Image.open(
                    BytesIO(response.content)
                )

        except Exception:
            # PNL generation should never
            # break trade finalization because
            # a token image failed to load.
            return None
```
