"use client";

import { useState } from "react";
import ChainTabs from "@/components/ChainTabs/ChainTabs";

const recruits = [
  {
    name: "Trader Alpha",
    status: "ACTIVE",
    volume: "$18,420",
    rewards: "$184",
  },
  {
    name: "WhaleNode",
    status: "ACTIVE",
    volume: "$12,840",
    rewards: "$128",
  },
  {
    name: "MomentumUser",
    status: "PENDING",
    volume: "$4,220",
    rewards: "$42",
  },
];

export default function RecruitsPage() {
  const [copied, setCopied] = useState(false);

  async function copyCode() {
    await navigator.clipboard.writeText("SENTINEL-ADX92");
    setCopied(true);

    window.setTimeout(() => {
      setCopied(false);
    }, 1500);
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Recruits</h1>
        <p className="mt-1 text-sm text-[#777]">
          Referral network, trader growth and reward tracking.
        </p>
      </div>

      <ChainTabs />

      <div className="grid gap-4 md:grid-cols-3">
        {[
          ["Total Recruits", "24"],
          ["Active Traders", "17"],
          ["Rewards Earned", "$2,418"],
        ].map(([label, value]) => (
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

      <div className="rounded-2xl border border-[#5A4718] bg-[#17130A] p-6">
        <div className="text-xs uppercase tracking-wider text-[#777]">
          Your Referral Code
        </div>

        <div className="mt-2 text-3xl font-black text-[#F5C84C]">
          SENTINEL-ADX92
        </div>

        <button
          type="button"
          onClick={() => void copyCode()}
          className="mt-4 rounded-lg bg-[#D4AF37] px-4 py-2 font-semibold text-black"
        >
          {copied ? "Copied" : "Copy Code"}
        </button>
      </div>

      <section className="rounded-2xl border border-[#292929] bg-[#101010] p-5">
        <h2 className="text-xl font-semibold">
          Recruit Activity
        </h2>

        <div className="mt-5 space-y-3">
          {recruits.map((recruit) => (
            <div
              key={recruit.name}
              className="grid gap-3 rounded-xl border border-[#292929] bg-[#171717] p-4 md:grid-cols-4"
            >
              <div className="font-semibold">
                {recruit.name}
              </div>

              <div
                className={
                  recruit.status === "ACTIVE"
                    ? "text-green-400"
                    : "text-yellow-400"
                }
              >
                {recruit.status}
              </div>

              <div className="text-[#AAA]">
                Volume: {recruit.volume}
              </div>

              <div className="text-[#F5C84C]">
                Rewards: {recruit.rewards}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}