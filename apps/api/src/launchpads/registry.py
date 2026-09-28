from __future__ import annotations

from chains.models import Chain

from launchpads.models import (
    DiscoveryMethod,
    LaunchpadConfig,
    LaunchpadType,
)


LAUNCHPADS: tuple[LaunchpadConfig, ...] = (

    # =========================================================
    # SOLANA
    # =========================================================

    LaunchpadConfig(
        slug="pumpfun",
        name="Pump.fun",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://pump.fun",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
        program_ids=(
            "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",
        ),
    ),

    LaunchpadConfig(
        slug="raydium-launchlab",
        name="Raydium LaunchLab",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://raydium.io/launchpad",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
        notes=(
            "Raydium permissionless bonding-curve launch infrastructure."
        ),
    ),

    LaunchpadConfig(
        slug="meteora-dbc",
        name="Meteora Dynamic Bonding Curve",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://meteora.ag",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
        notes=(
            "Meteora launch infrastructure using configurable "
            "dynamic bonding curves."
        ),
    ),

    LaunchpadConfig(
        slug="meteora-launch-pool",
        name="Meteora Launch Pool",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.LIQUIDITY_LAUNCH,
        website="https://launch.meteora.ag",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
        notes=(
            "Single-sided liquidity launch infrastructure."
        ),
    ),

    LaunchpadConfig(
        slug="jupiter-studio",
        name="Jupiter Studio",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://studio.jup.ag",
        discovery_method=DiscoveryMethod.API,
    ),

    LaunchpadConfig(
        slug="moonshot",
        name="Moonshot",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://moonshot.money",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="bonkfun",
        name="BONKfun",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://letsbonk.fun",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="heaven",
        name="Heaven",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://heaven.xyz",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
    ),

    LaunchpadConfig(
        slug="believe",
        name="Believe",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://believe.app",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="bags",
        name="Bags",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://bags.fm",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
    ),

    LaunchpadConfig(
        slug="boop",
        name="Boop",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://boop.fun",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
        program_ids=(
            "boop8hVGQGqehUK2iVEMEnMrL5RbjywRzHKBmBE7ry4",
        ),
    ),

    LaunchpadConfig(
        slug="daos-fun",
        name="DAOS.FUN",
        chain=Chain.SOLANA,
        launchpad_type=LaunchpadType.DAO_LAUNCH,
        website="https://www.daos.fun",
        discovery_method=DiscoveryMethod.ONCHAIN_PROGRAM,
    ),

    # =========================================================
    # BASE
    # =========================================================

    LaunchpadConfig(
        slug="clanker",
        name="Clanker",
        chain=Chain.BASE,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://clanker.world",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    LaunchpadConfig(
        slug="zora",
        name="Zora Coins",
        chain=Chain.BASE,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://zora.co",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    LaunchpadConfig(
        slug="uniswap-liquidity-launchpad",
        name="Uniswap Liquidity Launchpad",
        chain=Chain.BASE,
        launchpad_type=LaunchpadType.AUCTION,
        website="https://app.uniswap.org",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
        contract_addresses=(
            "0x0000FffFBE8efE702c8703aE3477FF5dE3d319C0",
            "0x000000001F26a0044BaA66024e7b6599c61963F8",
        ),
    ),

    LaunchpadConfig(
        slug="pinksale",
        name="PinkSale",
        chain=Chain.BASE,
        launchpad_type=LaunchpadType.FAIR_LAUNCH,
        website="https://www.pinksale.finance",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    # =========================================================
    # ETHEREUM
    # =========================================================

    LaunchpadConfig(
        slug="zora",
        name="Zora Coins",
        chain=Chain.ETHEREUM,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://zora.co",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    LaunchpadConfig(
        slug="uniswap-liquidity-launchpad",
        name="Uniswap Liquidity Launchpad",
        chain=Chain.ETHEREUM,
        launchpad_type=LaunchpadType.AUCTION,
        website="https://app.uniswap.org",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
        contract_addresses=(
            "0x0000FffFBE8efE702c8703aE3477FF5dE3d319C0",
            "0x000000001F26a0044BaA66024e7b6599c61963F8",
        ),
    ),

    LaunchpadConfig(
        slug="pinksale",
        name="PinkSale",
        chain=Chain.ETHEREUM,
        launchpad_type=LaunchpadType.FAIR_LAUNCH,
        website="https://www.pinksale.finance",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    # =========================================================
    # BNB CHAIN
    # =========================================================

    LaunchpadConfig(
        slug="four-meme",
        name="Four.Meme",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://four.meme",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    LaunchpadConfig(
        slug="flap",
        name="Flap",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://flap.sh",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    LaunchpadConfig(
        slug="gra-fun",
        name="Gra.Fun",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://gra.fun",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="burve",
        name="Burve",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://burve.io",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="pinksale",
        name="PinkSale",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.FAIR_LAUNCH,
        website="https://www.pinksale.finance",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="tokenfi",
        name="TokenFi",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://tokenfi.com",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    LaunchpadConfig(
        slug="beeper",
        name="Beeper",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://beeper.global",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="holoworldai",
        name="HoloworldAI",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.AGENT_TOKEN,
        website="https://holoworldai.com",
        discovery_method=DiscoveryMethod.INDEXER,
    ),

    LaunchpadConfig(
        slug="pancakeswap-springboard",
        name="PancakeSwap SpringBoard",
        chain=Chain.BNB,
        launchpad_type=LaunchpadType.TOKEN_LAUNCH,
        website="https://pancakeswap.finance",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    # =========================================================
    # ROBINHOOD CHAIN
    # =========================================================

    LaunchpadConfig(
        slug="hood-fun",
        name="hood.fun",
        chain=Chain.ROBINHOOD,
        launchpad_type=LaunchpadType.BONDING_CURVE,
        website="https://hood.fun",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
    ),

    LaunchpadConfig(
        slug="uniswap-liquidity-launchpad",
        name="Uniswap Liquidity Launchpad",
        chain=Chain.ROBINHOOD,
        launchpad_type=LaunchpadType.AUCTION,
        website="https://app.uniswap.org",
        discovery_method=DiscoveryMethod.ONCHAIN_CONTRACT,
        contract_addresses=(
            "0x0000FffFBE8efE702c8703aE3477FF5dE3d319C0",
            "0x000000001F26a0044BaA66024e7b6599c61963F8",
        ),
    ),

    LaunchpadConfig(
        slug="pinksale",
        name="PinkSale",
        chain=Chain.ROBINHOOD,
        launchpad_type=LaunchpadType.FAIR_LAUNCH,
        website="https://www.pinksale.finance",
        discovery_method=DiscoveryMethod.INDEXER,
    ),
)


def get_launchpads(
    chain: Chain | None = None,
    active_only: bool = True,
) -> list[LaunchpadConfig]:
    result = list(LAUNCHPADS)

    if chain is not None:
        result = [
            item
            for item in result
            if item.chain == chain
        ]

    if active_only:
        result = [
            item
            for item in result
            if item.active
        ]

    return result


def get_launchpad(
    chain: Chain,
    slug: str,
) -> LaunchpadConfig:
    for item in LAUNCHPADS:
        if (
            item.chain == chain
            and item.slug == slug
        ):
            if not item.active:
                raise ValueError(
                    f"Launchpad is inactive: {slug}"
                )

            return item

    raise ValueError(
        f"Launchpad not found: "
        f"{chain.value}/{slug}"
    )