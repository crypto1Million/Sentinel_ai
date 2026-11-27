"use client";

import ChainTabs from "@/components/ChainTabs/ChainTabs";
import TokenCard from "@/components/TokenCard/TokenCard";
import ScoreCard from "@/components/ScoreCard/ScoreCard";

import { useRealtimeStore } from "@/store/realtimeStore";
import { useChainStore } from "@/store/chainStore";

function readString(...values: unknown[]): string | undefined {
  for (const value of values) {
    if (typeof value === "string" && value.trim()) {
      return value.trim();
    }
  }

  return undefined;
}

function readNumber(...values: unknown[]): number | undefined {
  for (const value of values) {
    if (typeof value === "number" && Number.isFinite(value)) {
      return value;
    }

    if (typeof value === "string" && value.trim()) {
      const parsed = Number(value);

      if (Number.isFinite(parsed)) {
        return parsed;
      }
    }
  }

  return undefined;
}

export default function DiscoverPage() {
  // Actual RealtimeStore collections
  const tokenRecords = useRealtimeStore((state) => state.tokens);
  const scoreRecords = useRealtimeStore((state) => state.scores);
  const walletRecords = useRealtimeStore((state) => state.wallets);
  const alerts = useRealtimeStore((state) => state.alerts);

  const connectionStatus = useRealtimeStore(
    (state) => state.connections.tokens
  );

  const selectedChain = useChainStore(
     (state) => state.selectedChain
  );

  // Convert canonical entity state into TokenCard props
  const tokens = Object.entries(tokenRecords)
    .filter(
     ([, entity]) =>
       (entity.chain ?? "unknown").toLowerCase()
       === selectedChain
  )
  .map(([, entity]) => {

      const mint =
        readString(
          values.token_mint,
          values.mint,
          values.token_address,
          values.address
        ) || entity.entityId;

      const symbol =
        readString(
          values.symbol,
          values.ticker
        ) || mint.slice(0, 10);

      return {
        mint,
        symbol,
        chain: (
          entity.chain ||
          readString(values.chain, values.network) ||
          "solana"
        ).toLowerCase(),

        marketCap: readNumber(
          values.market_cap_usd,
          values.market_cap,
          values.marketCap
        ),

        holders: readNumber(
          values.holders,
          values.holder_count,
          values.num_holders
        ),

        price: readNumber(
          values.price_usd,
          values.price,
          values.priceUsd
        ),

        observedAt: entity.observedAt,
      };
    })
    .sort((a, b) =>
      b.observedAt.localeCompare(a.observedAt)
    );

  // Actual current entity counts, not fabricated event totals
  const intelligence = [
    {
      label: "Tracked Tokens",
      value: tokens.length,
    },
    {
      label: "Score Records",
      value: Object.keys(scoreRecords).length,
    },
    {
      label: "Tracked Wallets",
      value: Object.keys(walletRecords).length,
    },
    {
      label: "Active Alerts",
      value: alerts.length,
    },
  ];

  const statusLabel = connectionStatus.toUpperCase();

  return (
    <div className="space-y-6">

      {/* HEADER */}
      <div>
        <h1 className="text-3xl font-bold">
          Discover
        </h1>

        <p className="mt-1 text-sm text-[#777]">
          Cross-chain token discovery and early opportunity detection.
        </p>
      </div>

      <ChainTabs />

      {/* LIVE METRICS */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

        {intelligence.map((item) => (
          <ScoreCard
            key={item.label}
            title={item.label}
            score={item.value}
          />
        ))}

      </div>

      {/* DISCOVER FEED */}
      <div className="grid gap-6 xl:grid-cols-[1fr_320px]">

        <section className="rounded-2xl border border-[#292929] bg-[#101010] p-5">

          <div className="mb-5 flex items-center justify-between">

            <div>
              <h2 className="text-xl font-semibold">
                Discover Feed
              </h2>

              <p className="text-sm text-[#666]">
                Canonical token state across supported chains.
              </p>
            </div>

            <span className="rounded-full border border-[#433716] bg-[#17130A] px-3 py-1 text-xs text-[#F5C84C]">
              {statusLabel}
            </span>

          </div>

          {/* TOKEN CARDS */}
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

            {tokens.length > 0 ? (

              tokens.slice(0, 12).map((token) => (
                <TokenCard
                  key={`${token.chain}:${token.mint}`}
                  symbol={token.symbol}
                  marketCap={token.marketCap}
                  holders={token.holders}
                  chain={token.chain}
                  price={token.price}
                  mint={token.mint}
                />
              ))

            ) : (

              <div className="col-span-full rounded-xl border border-dashed border-[#333] p-8 text-center">

                <p className="text-sm font-medium text-[#C8C8C8]">
                  Waiting for canonical token events
                </p>

                <p className="mt-2 text-xs text-[#777]">
                  Token cards appear as real token, pool, launchpad
                  and intelligence events arrive.
                </p>

              </div>

            )}

          </div>

        </section>

        {/* DISCOVERY INTELLIGENCE */}
        <aside className="rounded-2xl border border-[#292929] bg-[#101010] p-5">

          <h2 className="text-lg font-semibold">
            Discovery Intelligence
          </h2>

          <div className="mt-5 space-y-3">

            {intelligence.map(({ label, value }) => (

              <div
                key={label}
                className="flex items-center justify-between rounded-xl bg-[#171717] p-4"
              >

                <span className="text-sm text-[#888]">
                  {label}
                </span>

                <span className="font-semibold text-white">
                  {value.toLocaleString()}
                </span>

              </div>

            ))}

          </div>

          <div className="mt-5 rounded-xl border border-[#433716] bg-[#17130A] p-4">

            <div className="text-xs uppercase tracking-wider text-[#777]">
              Sentinel Engine
            </div>

            <div className="mt-2 text-sm text-[#D0D0D0]">
              Discovery ranking combines opportunity, wallet,
              narrative, volume and security intelligence.
            </div>

          </div>

        </aside>

      </div>

    </div>
  );
}
