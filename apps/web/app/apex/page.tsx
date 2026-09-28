"use client";

import { useState } from "react";
import ChainTabs from "@/components/ChainTabs/ChainTabs";

type Period = "1D" | "3D" | "7D" | "30D";

const leaders = [
  ["ShadowFox", "SOL", "$18,420", "94"],
  ["AlphaNode", "BASE", "$14,870", "92"],
  ["WhalePrime", "ETH", "$11,620", "90"],
  ["MomentumX", "BNB", "$9,840", "88"],
  ["NightHawk", "HOOD", "$8,230", "86"],
  ["SentinelOne", "SOL", "$7,910", "84"],
];

export default function ApexPage() {
  const [period, setPeriod] = useState<Period>("1D");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Apex</h1>
        <p className="mt-1 text-sm text-[#777]">
          Competitive trading performance and leaderboard intelligence.
        </p>
      </div>

      <ChainTabs />

      <div className="flex gap-2 overflow-x-auto">
        {(["1D", "3D", "7D", "30D"] as Period[]).map((value) => (
          <button
            key={value}
            type="button"
            onClick={() => setPeriod(value)}
            className={[
              "rounded-lg border px-4 py-2 text-sm",
              period === value
                ? "border-[#5A4718] bg-[#17130A] text-[#F5C84C]"
                : "border-[#292929] bg-[#101010] text-[#888]",
            ].join(" ")}
          >
            {value}
          </button>
        ))}
      </div>

      <section className="rounded-2xl border border-[#292929] bg-[#101010] p-5">
        <div className="mb-5 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">
              Apex {period} Leaderboard
            </h2>

            <p className="text-sm text-[#666]">
              Ranked trading performance for the selected period.
            </p>
          </div>

          <div className="rounded-lg bg-[#17130A] px-3 py-2 text-xs text-[#F5C84C]">
            APEX
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[720px] text-sm">
            <thead>
              <tr className="border-b border-[#292929] text-left text-[#666]">
                <th className="px-4 py-3">Rank</th>
                <th className="px-4 py-3">Trader</th>
                <th className="px-4 py-3">Chain</th>
                <th className="px-4 py-3">PnL</th>
                <th className="px-4 py-3">Sentinel</th>
              </tr>
            </thead>

            <tbody>
              {leaders.map(([name, chain, pnl, score], index) => (
                <tr
                  key={name}
                  className="border-b border-[#1D1D1D] hover:bg-[#151515]"
                >
                  <td className="px-4 py-4 font-bold text-[#F5C84C]">
                    #{index + 1}
                  </td>

                  <td className="px-4 py-4 font-semibold">
                    {name}
                  </td>

                  <td className="px-4 py-4 text-[#999]">
                    {chain}
                  </td>

                  <td className="px-4 py-4 font-semibold text-green-400">
                    +{pnl}
                  </td>

                  <td className="px-4 py-4 font-semibold">
                    {score}/100
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