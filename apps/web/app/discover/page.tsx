"use client";

import ChainTabs from "@/components/ChainTabs/ChainTabs";

import TokenCard from "@/components/TokenCard/TokenCard";

import ScoreCard from "@/components/ScoreCard/ScoreCard";

import {
  useRealtimeStore
} from "@/store/realtimeStore";


export default function DiscoverPage() {

  const tokensByKey = useRealtimeStore(
    (state) => state.tokensByKey
  );

  const eventCounts = useRealtimeStore(
    (state) => state.eventCountsByType
  );

  const connectionStatus = useRealtimeStore(
    (state) => state.connectionStatus
  );


  const tokens = Object.values(
    tokensByKey
  ).sort((a, b) =>

    b.observedAt.localeCompare(
      a.observedAt
    )

  );


  const intelligence = [

    {
      label: "Market intelligence",

      value:
        eventCounts[
          "market_intelligence.updated"
        ] || 0,
    },

    {
      label: "New launches",

      value:
        eventCounts[
          "launchpad.detected"
        ] || 0,
    },

    {
      label: "Rug Radar updates",

      value:
        eventCounts[
          "rug.updated"
        ] || 0,
    },

    {
      label: "Wallet DNA updates",

      value:
        eventCounts[
          "wallet_dna.updated"
        ] || 0,
    },

  ];


  const statusLabel =

    connectionStatus === "connected"

      ? "CONNECTED"

      : connectionStatus === "reconnecting"

        ? "RECONNECTING"

        : connectionStatus === "connecting"

          ? "CONNECTING"

          : connectionStatus.toUpperCase();


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

        <ScoreCard

          title="Live Tokens"

          score={tokens.length}

        />

        <ScoreCard

          title="Score Events"

          score={
            eventCounts["score.updated"] || 0
          }

        />

        <ScoreCard

          title="New Launches"

          score={
            eventCounts["launchpad.detected"] || 0
          }

        />

        <ScoreCard

          title="Market Signals"

          score={
            eventCounts[
              "market_intelligence.updated"
            ] || 0
          }

        />

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

                Sentinel-ranked tokens across the active chain.

              </p>

            </div>


            <span className="rounded-full border border-[#433716] bg-[#17130A] px-3 py-1 text-xs text-[#F5C84C]">

              {statusLabel}

            </span>

          </div>


          {/* LIVE TOKEN CARDS */}

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

            {tokens.length > 0 ? (

              tokens.slice(0, 12).map((token) => (

                <TokenCard

                  key={`${token.chain}:${token.mint}`}

                  symbol={
                    token.symbol ||
                    token.name ||
                    token.mint
                  }

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

                  Token cards appear as real token, pool, launchpad and intelligence events arrive.

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