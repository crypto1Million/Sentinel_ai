import ChainTabs from "@/components/ChainTabs/ChainTabs";

const assets = [
  ["AAPL", "Apple", "$228.41", "+1.84%"],
  ["TSLA", "Tesla", "$341.22", "+3.21%"],
  ["NVDA", "NVIDIA", "$181.76", "+2.41%"],
  ["AMZN", "Amazon", "$231.09", "-0.64%"],
  ["MSFT", "Microsoft", "$512.34", "+0.92%"],
  ["COIN", "Coinbase", "$327.18", "+4.11%"],
];

export default function XStocksPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">xStocks</h1>
        <p className="mt-1 text-sm text-[#777]">
          Cross-chain market dashboard for tokenized equity exposure.
        </p>
      </div>

      <ChainTabs />

      <div className="grid gap-4 md:grid-cols-3">
        {[
          ["Tracked Assets", "126"],
          ["Market Value", "$4.82M"],
          ["24h Flow", "+$184K"],
        ].map(([label, value]) => (
          <div
            key={label}
            className="rounded-2xl border border-[#292929] bg-[#101010] p-5"
          >
            <div className="text-xs uppercase tracking-wider text-[#666]">
              {label}
            </div>

            <div className="mt-2 text-2xl font-bold text-white">
              {value}
            </div>
          </div>
        ))}
      </div>

      <section className="rounded-2xl border border-[#292929] bg-[#101010] p-5">
        <div className="mb-5">
          <h2 className="text-xl font-semibold">
            Market Watch
          </h2>

          <p className="text-sm text-[#666]">
            Example dashboard structure; connect to the actual xStocks feed later.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px] text-sm">
            <thead>
              <tr className="border-b border-[#292929] text-left text-[#666]">
                <th className="px-4 py-3">Symbol</th>
                <th className="px-4 py-3">Asset</th>
                <th className="px-4 py-3">Price</th>
                <th className="px-4 py-3">24h</th>
              </tr>
            </thead>

            <tbody>
              {assets.map(([symbol, name, price, change]) => (
                <tr
                  key={symbol}
                  className="border-b border-[#1D1D1D] hover:bg-[#151515]"
                >
                  <td className="px-4 py-4 font-semibold">
                    {symbol}
                  </td>

                  <td className="px-4 py-4 text-[#999]">
                    {name}
                  </td>

                  <td className="px-4 py-4">
                    {price}
                  </td>

                  <td
                    className={[
                      "px-4 py-4 font-semibold",
                      change.startsWith("+")
                        ? "text-green-400"
                        : "text-red-400",
                    ].join(" ")}
                  >
                    {change}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}