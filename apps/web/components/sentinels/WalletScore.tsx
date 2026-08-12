id="rug8qa"
"use client";

import {
  Wallet,
  Brain,
  Fish,
  Users,
  Shield,
  Activity,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle2,
  Network,
  DollarSign,
} from "lucide-react";

interface WalletScoreProps {
  walletScore: number;

  confidence: number;

  smartMoneyScore: number;

  whaleScore: number;

  freshWalletScore: number;

  insiderScore: number;

  clusterScore: number;

  walletGrowth: number;

  avgWalletPnL: number;

  convictionScore: number;

  holdingStrength: number;

  aiSummary: string;
}

interface MetricCardProps {
  title: string;

  value: string;

  icon: React.ElementType;

  color?: string;
}

function MetricCard({
  title,
  value,
  icon: Icon,
  color = "text-cyan-400",
}: MetricCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-4">

      <div className="mb-2 flex items-center gap-2">

        <Icon
          size={18}
          className={color}
        />

        <span className="text-sm text-zinc-400">

          {title}

        </span>

      </div>

      <div className="text-2xl font-bold">

        {value}

      </div>

    </div>
  );
}

export default function WalletScore({
  walletScore,

  confidence,

  smartMoneyScore,

  whaleScore,

  freshWalletScore,

  insiderScore,

  clusterScore,

  walletGrowth,

  avgWalletPnL,

  convictionScore,

  holdingStrength,

  aiSummary,
}: WalletScoreProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div className="flex items-center gap-3">

          <Wallet
            size={28}
            className="text-cyan-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              Wallet Score

            </h2>

            <p className="text-sm text-zinc-500">

              Wallet DNA Intelligence Engine

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-cyan-500 px-6 py-4">

          <div className="text-4xl font-black text-black">

            {walletScore}

          </div>

          <div className="text-center text-xs font-semibold text-black">

            /100

          </div>

        </div>

      </div>

      {/* Confidence */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center justify-between">

          <div>

            <p className="text-sm text-zinc-500">

              AI Confidence

            </p>

            <div className="mt-2 text-3xl font-bold text-cyan-400">

              {confidence}%

            </div>

          </div>

          <div>

            {walletScore >= 80 ? (
              <CheckCircle2
                className="text-green-400"
                size={42}
              />
            ) : (
              <AlertTriangle
                className="text-yellow-400"
                size={42}
              />
            )}

          </div>

        </div>

      </div>

      {/* Wallet Metrics */}

      <div>

        <h3 className="mb-4 font-semibold">

          Wallet Intelligence

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <MetricCard
            title="Smart Money"
            value={`${smartMoneyScore}/100`}
            icon={Brain}
            color="text-green-400"
          />

          <MetricCard
            title="Whales"
            value={`${whaleScore}/100`}
            icon={Fish}
            color="text-blue-400"
          />

          <MetricCard
            title="Fresh Wallets"
            value={`${freshWalletScore}/100`}
            icon={Users}
            color="text-yellow-400"
          />

          <MetricCard
            title="Insiders"
            value={`${insiderScore}/100`}
            icon={Shield}
            color="text-red-400"
          />

          <MetricCard
            title="Wallet Clusters"
            value={`${clusterScore}/100`}
            icon={Network}
            color="text-purple-400"
          />

          <MetricCard
            title="Wallet Growth"
            value={`${walletGrowth}%`}
            icon={TrendingUp}
            color="text-green-400"
          />

        </div>

      </div>

      {/* Performance */}

      <div>

        <h3 className="mb-4 font-semibold">

          Historical Performance

        </h3>

        <div className="grid gap-4 md:grid-cols-3">

          <MetricCard
            title="Average Wallet PnL"
            value={`${avgWalletPnL}%`}
            icon={DollarSign}
            color={
              avgWalletPnL >= 0
                ? "text-green-400"
                : "text-red-400"
            }
          />

          <MetricCard
            title="Conviction Score"
            value={`${convictionScore}/100`}
            icon={Activity}
          />

          <MetricCard
            title="Holding Strength"
            value={`${holdingStrength}/100`}
            icon={TrendingUp}
          />

        </div>

      </div>

      {/* AI Summary */}

      <div className="rounded-xl border border-cyan-900 bg-cyan-950/30 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            size={20}
            className="text-cyan-400"
          />

          <span className="font-semibold">

            Sentinel Wallet Analysis

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiSummary}

        </p>

      </div>

      {/* Verdict */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center gap-3">

          {walletScore >= 80 ? (
            <TrendingUp
              className="text-green-400"
              size={24}
            />
          ) : (
            <TrendingDown
              className="text-yellow-400"
              size={24}
            />
          )}

          <div>

            <div className="font-semibold">

              Wallet Verdict

            </div>

            <div className="text-sm text-zinc-400">

              {walletScore >= 80
                ? "High-quality wallets dominate the holder base with strong historical profitability."
                : walletScore >= 60
                ? "Mixed wallet quality. Monitor Smart Money accumulation."
                : "Low-quality holder distribution with elevated risk."}

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
