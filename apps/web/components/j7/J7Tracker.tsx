"use client";

import {
  Brain,
  Activity,
  Wallet,
  Users,
  TrendingUp,
  TrendingDown,
  Fish,
  Shield,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Network,
  Sparkles,
  ArrowUpRight,
  ArrowDownRight,
  Eye,
} from "lucide-react";

export interface J7Wallet {
  id: string;

  address: string;

  label: string;

  score: number;

  pnl: number;

  winRate: number;

  lastAction: "BUY" | "SELL";

  token: string;

  amount: number;

  timestamp: string;
}

interface J7TrackerProps {
  score: number;

  confidence: number;

  wallets: J7Wallet[];

  smartMoneyCount: number;

  whaleCount: number;

  activeWallets: number;

  aiSummary: string;
}

export default function J7Tracker({
  score,
  confidence,
  wallets,
  smartMoneyCount,
  whaleCount,
  activeWallets,
  aiSummary,
}: J7TrackerProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div className="flex items-center gap-3">

          <Brain
            size={30}
            className="text-cyan-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              J7 Tracker™

            </h2>

            <p className="text-sm text-zinc-500">

              Proprietary Wallet Intelligence Engine

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-cyan-500 px-6 py-4">

          <div className="text-4xl font-black text-black">

            {score}

          </div>

          <div className="text-xs font-semibold text-black">

            /100

          </div>

        </div>

      </div>

      {/* Overview */}

      <div className="grid gap-4 md:grid-cols-4">

        <Metric
          title="Confidence"
          value={`${confidence}%`}
          icon={Shield}
          color="text-cyan-400"
        />

        <Metric
          title="Smart Wallets"
          value={smartMoneyCount.toString()}
          icon={Wallet}
          color="text-green-400"
        />

        <Metric
          title="Whales"
          value={whaleCount.toString()}
          icon={Fish}
          color="text-blue-400"
        />

        <Metric
          title="Active Wallets"
          value={activeWallets.toString()}
          icon={Activity}
          color="text-yellow-400"
        />

      </div>

      {/* AI Summary */}

      <div className="rounded-xl border border-cyan-900 bg-cyan-950/20 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Sparkles
            className="text-cyan-400"
            size={18}
          />

          <span className="font-semibold">

            Sentinel AI Wallet Summary

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiSummary}

        </p>

      </div>

      {/* Wallet Table */}

      <div>

        <h3 className="mb-4 text-lg font-semibold">

          Live Smart Wallet Activity

        </h3>

        <div className="overflow-x-auto rounded-xl border border-zinc-800">

          <table className="w-full">

            <thead className="bg-[#1B2330]">

              <tr className="text-left">

                <th className="p-4">Wallet</th>

                <th className="p-4">Score</th>

                <th className="p-4">Win Rate</th>

                <th className="p-4">PnL</th>

                <th className="p-4">Action</th>

                <th className="p-4">Token</th>

                <th className="p-4">Time</th>

              </tr>

            </thead>

            <tbody>

              {wallets.map((wallet) => (

                <tr
                  key={wallet.id}
                  className="border-t border-zinc-800 hover:bg-[#1B2330]"
                >

                  <td className="p-4">

                    <div>

                      <div className="font-semibold">

                        {wallet.label}

                      </div>

                      <div className="text-xs text-zinc-500">

                        {wallet.address}

                      </div>

                    </div>

                  </td>

                  <td className="p-4">

                    <span className="font-bold text-cyan-400">

                      {wallet.score}

                    </span>

                  </td>

                  <td className="p-4">

                    {wallet.winRate}%

                  </td>

                  <td
                    className={`p-4 font-semibold ${
                      wallet.pnl >= 0
                        ? "text-green-400"
                        : "text-red-400"
                    }`}
                  >

                    {wallet.pnl >= 0 ? "+" : ""}

                    {wallet.pnl}%

                  </td>

                  <td className="p-4">

                    {wallet.lastAction === "BUY" ? (

                      <span className="flex items-center gap-1 text-green-400">

                        <ArrowUpRight size={16} />

                        BUY

                      </span>

                    ) : (

                      <span className="flex items-center gap-1 text-red-400">

                        <ArrowDownRight size={16} />

                        SELL

                      </span>

                    )}

                  </td>

                  <td className="p-4">

                    {wallet.token}

                  </td>

                  <td className="p-4 text-zinc-500">

                    {wallet.timestamp}

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

      {/* Footer */}

      <div className="grid gap-4 md:grid-cols-3">

        <FooterCard
          icon={Users}
          title="Wallet Clusters"
          value="Connected"
        />

        <FooterCard
          icon={Network}
          title="Funding Graph"
          value="Live"
        />

        <FooterCard
          icon={Eye}
          title="Replay Ready"
          value="Enabled"
        />

      </div>

    </div>
  );
}

function Metric({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string;
  value: string;
  icon: React.ElementType;
  color: string;
}) {
  return (
    <div className="rounded-xl bg-[#1B2330] p-4">

      <div className="mb-2 flex items-center gap-2">

        <Icon
          className={color}
          size={18}
        />

        <span className="text-sm text-zinc-500">

          {title}

        </span>

      </div>

      <div className="text-2xl font-bold">

        {value}

      </div>

    </div>
  );
}

function FooterCard({
  icon: Icon,
  title,
  value,
}: {
  icon: React.ElementType;
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-xl bg-[#1B2330] p-5">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          className="text-cyan-400"
          size={18}
        />

        <span className="font-medium">

          {title}

        </span>

      </div>

      <div className="text-lg font-bold">

        {value}

      </div>

    </div>
  );
}