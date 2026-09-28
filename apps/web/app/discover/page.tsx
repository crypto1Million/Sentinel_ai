import ChainTabs from "@/components/ChainTabs/ChainTabs";
import TokenCard from "@/components/TokenCard/TokenCard";
import ScoreCard from "@/components/ScoreCard/ScoreCard";

const tokens = [
  {
    symbol: "$NOVA",
    marketCap: 482000,
    holders: 1842,
  },
  {
    symbol: "$SENTRY",
    marketCap: 1280000,
    holders: 4217,
  },
  {
    symbol: "$MOONAI",
    marketCap: 920000,
    holders: 2871,
  },
  {
    symbol: "$PIXEL",
    marketCap: 315000,
    holders: 1164,
  },
  {
    symbol: "$ROAR",
    marketCap: 742000,
    holders: 2119,
  },
  {
    symbol: "$KILO",
    marketCap: 1930000,
    holders: 6381,
  },
];

const intelligence = [
  ["Trending", "18"],
  ["New launches", "42"],
  ["Graduating", "7"],
  ["Migration signals", "11"],
];

export default function DiscoverPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Discover</h1>
        <p className="mt-1 text-sm text-[#777]">
          Cross-chain token discovery and early opportunity detection.
        </p>
      </div>

      <ChainTabs />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <ScoreCard title="Live Tokens" score={128} />
        <ScoreCard title="Trending" score={34} />
        <ScoreCard title="New Launches" score={42} />
        <ScoreCard title="Opportunities" score={17} />
      </div>

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
              LIVE
            </span>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {tokens.map((token) => (
              <TokenCard
                key={token.symbol}
                symbol={token.symbol}
                marketCap={token.marketCap}
                holders={token.holders}
              />
            ))}
          </div>
        </section>

        <aside className="rounded-2xl border border-[#292929] bg-[#101010] p-5">
          <h2 className="text-lg font-semibold">
            Discovery Intelligence
          </h2>

          <div className="mt-5 space-y-3">
            {intelligence.map(([label, value]) => (
              <div
                key={label}
                className="flex items-center justify-between rounded-xl bg-[#171717] p-4"
              >
                <span className="text-sm text-[#888]">
                  {label}
                </span>

                <span className="font-semibold text-white">
                  {value}
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