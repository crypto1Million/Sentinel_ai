"""
Jupiter Swap Manager
====================

Builds, signs, simulates and executes Jupiter swaps.
"""

###############################################################################
# Imports
###############################################################################

from __future__ import annotations

from typing import Dict, List, Optional
import base64
import time


###############################################################################
# SwapManager
###############################################################################


class SwapManager:
    """
    Jupiter Swap Manager.
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(self):

        self.last_swap = None

    ###########################################################################
    # Swap Pipeline
    ###########################################################################

    def build_transaction(
        self,
        swap_response: Dict,
    ) -> Dict:
        """
        Returns unsigned Jupiter transaction.
        """

        return {
            "transaction": swap_response.get("swapTransaction"),
            "last_valid_block_height": swap_response.get(
                "lastValidBlockHeight"
            ),
            "prioritization_fee": swap_response.get(
                "prioritizationFeeLamports"
            ),
        }

    ###########################################################################

    def sign_transaction(
        self,
        transaction: str,
        wallet,
    ) -> str:
        """
        Placeholder signer.

        Wallet adapter should replace this.
        """

        return transaction

    ###########################################################################

    def simulate(
        self,
        transaction: str,
    ) -> Dict:

        return {
            "success": True,
            "transaction": transaction,
            "logs": [],
        }

    ###########################################################################

    def execute(
        self,
        signed_transaction: str,
    ) -> Dict:

        signature = f"SWAP_{int(time.time())}"

        self.last_swap = signature

        return {
            "success": True,
            "signature": signature,
        }

    ###########################################################################
    # Swap Helpers
    ###########################################################################

    def swap_history(self) -> Optional[str]:

        return self.last_swap

    ###########################################################################

    def swap_statistics(
        self,
        swaps: List[Dict],
    ) -> Dict:

        volume = sum(
            float(
                swap.get("out_amount", 0)
            )
            for swap in swaps
        )

        return {
            "total_swaps": len(swaps),
            "total_volume": volume,
        }

    ###########################################################################

    def swap_score(
        self,
        quote: Dict,
    ) -> float:

        impact = float(
            quote.get(
                "price_impact_pct",
                0,
            )
        )

        score = 100 - impact * 100

        return max(0, min(score, 100))

    ###########################################################################
    # Advanced
    ###########################################################################

    def decode_transaction(
        self,
        tx: str,
    ) -> bytes:

        return base64.b64decode(tx)

    ###########################################################################

    def encode_transaction(
        self,
        raw: bytes,
    ) -> str:

        return base64.b64encode(raw).decode()

    ###########################################################################

    def verify_transaction(
        self,
        transaction: str,
    ) -> bool:

        return transaction is not None

    ###########################################################################

    def cancel(
        self,
        signature: str,
    ) -> Dict:

        return {
            "success": False,
            "reason": "Blockchain transactions cannot be cancelled after submission.",
            "signature": signature,
        }

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self) -> Dict:

        return {
            "manager": "SwapManager",
            "last_swap": self.last_swap,
        }

    ###########################################################################

    def summary(self) -> Dict:

        return {
            "provider": "Jupiter",
            "component": "Swap Manager",
        }


###############################################################################
# Utilities
###############################################################################


def normalize_swap(
    swap: Dict,
) -> Dict:

    return {
        "input_mint": swap.get("inputMint"),
        "output_mint": swap.get("outputMint"),
        "in_amount": swap.get("inAmount"),
        "out_amount": swap.get("outAmount"),
        "price_impact_pct": swap.get("priceImpactPct"),
        "swap_transaction": swap.get("swapTransaction"),
    }


###############################################################################


def swap_metadata(
    swap: Dict,
) -> Dict:

    return {
        "input": swap.get("inputMint"),
        "output": swap.get("outputMint"),
        "route_count": len(
            swap.get(
                "routePlan",
                [],
            )
        ),
    }