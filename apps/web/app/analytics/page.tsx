import ChainTabs from "@/components/ChainTabs/ChainTabs";

const performance = [
  ["Win Rate", 67],
  ["Average ROI", 42],
  ["Risk Efficiency", 81],
  ["Execution Quality", 76],
];

const activity = [
  ["Trades", "184"],
  ["Winning Trades", "123"],
  ["Losing Trades", "61"],
  ["Avg Hold", "18m"],
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="mt-1 text-sm text-[#777]">
          Trading performance, intelligence and behavioral analytics.
        </p>
      </div>

      <ChainTabs />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {activity.map(([label, value]) => (
          <div
            key={label}
            className="rounded-2xl border border-[#292929] bg-[#101010] p-5"
          >
            <div className="text-xs uppercase tracking-wider text-[#666]">
              {label}
            </div>

            <div className="mt-2 text-2xl font-bold">
              {value}
            </div>
          </div>
        ))}
      </div>

      <section className="rounded-2xl border border-[#292929] bg-[#101010] p-6">
        <h2 className="text-xl font-semibold">
          Performance Metrics
        </h2>

        <div className="mt-6 space-y-5">
          {performance.map(([label, raw]) => {
            const value = Number(raw);

            return (
              <div key={label}>
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span className="text-[#999]">{label}</span>
                  <span className="font-semibold text-white">
                    {value}
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-[#202020]">
                  <div
                    className="h-full rounded-full bg-[#D4AF37]"
                    style={{
                      width: `${Math.max(
                        0,
                        Math.min(value, 100)
                      )}%`,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="rounded-2xl border border-[#292929] bg-[#101010] p-6">
          <h2 className="text-xl font-semibold">
            Trading Behavior
          </h2>

          <div className="mt-5 space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-[#777]">
                Early entries
              </span>
              <span>78%</span>
            </div>

            <div className="flex justify-between">
              <span className="text-[#777]">
                Momentum entries
              </span>
              <span>64%</span>
            </div>

            <div className="flex justify-between">
              <span className="text-[#777]">
                Stop-loss usage
              </span>
              <span>41%</span>
            </div>

            <div className="flex justify-between">
              <span className="text-[#777]">
                Large-position discipline
              </span>
              <span>83%</span>
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-[#292929] bg-[#101010] p-6">
          <h2 className="text-xl font-semibold">
            Sentinel Intelligence
          </h2>

          <p className="mt-4 leading-7 text-[#999]">
            Analytics should eventually combine trade history,
            wallet behavior, narrative exposure, execution quality,
            drawdown, opportunity selection and risk events.
          </p>
        </section>
      </div>
    </div>
  );
}