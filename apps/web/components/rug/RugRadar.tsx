"use client";

import {
  ShieldAlert,
  AlertTriangle,
  ShieldCheck,
  Brain,
  Lock,
  Flame,
  Coins,
  Wallet,
  Users,
  TrendingDown,
  TrendingUp,
  Activity,
  Eye,
  Skull,
  CheckCircle2,
  XCircle,
  BooleanMetric,
  Metric,
} from "lucide-react";

export interface RugRadarProps {
  rugScore: number;

  rugProbability: number;

  confidence: number;

  riskLevel: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

  liquidityLocked: boolean;

  liquidityBurned: boolean;

  ownershipRenounced: boolean;

  mintAuthority: boolean;

  freezeAuthority: boolean;

  holderConcentration: number;

  insiderWallets: number;

  deployerTrust: number;

  smartMoneyExposure: number;

  aiSummary: string;
}

export default function RugRadar({
  rugScore,
  rugProbability,
  confidence,
  riskLevel,
  liquidityLocked,
  liquidityBurned,
  ownershipRenounced,
  mintAuthority,
  freezeAuthority,
  holderConcentration,
  insiderWallets,
  deployerTrust,
  smartMoneyExposure,
  aiSummary,
}: RugRadarProps) {
  const riskColor =
    riskLevel === "LOW"
      ? "text-green-400"
      : riskLevel === "MEDIUM"
      ? "text-yellow-400"
      : riskLevel === "HIGH"
      ? "text-orange-400"
      : "text-red-500";

  return (
    <div className="rounded-2xl border border-red-900 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div className="flex items-center gap-3">

          <ShieldAlert
            className="text-red-400"
            size={30}
          />

          <div>

            <h2 className="text-2xl font-bold">

              Rug Radar™

            </h2>

            <p className="text-sm text-zinc-500">

              Sentinel Security Intelligence

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-red-500 px-6 py-4">

          <div className="text-4xl font-black text-black">

            {rugScore}

          </div>

          <div className="text-xs font-semibold text-black">

            /100

          </div>

        </div>

      </div>

      {/* Overall */}

      <div className="grid gap-4 md:grid-cols-3">

        <Metric
          icon={AlertTriangle}
          title="Risk Level"
          value={riskLevel}
          color={riskColor}
        />

        <Metric
          icon={Brain}
          title="AI Confidence"
          value={`${confidence}%`}
          color="text-cyan-400"
        />

        <Metric
          icon={Skull}
          title="Rug Probability"
          value={`${rugProbability}%`}
          color="text-red-400"
        />

      </div>

      {/* Contract */}

      <div>

        <h3 className="mb-4 font-semibold">

          Contract Security

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <BooleanMetric
            title="Liquidity Locked"
            value={liquidityLocked}
            icon={Lock}
          />

          <BooleanMetric
            title="Liquidity Burned"
            value={liquidityBurned}
            icon={Flame}
          />

          <BooleanMetric
            title="Ownership Renounced"
            value={ownershipRenounced}
            icon={ShieldCheck}
          />

          <BooleanMetric
            title="Mint Authority Disabled"
            value={!mintAuthority}
            icon={Coins}
          />

          <BooleanMetric
            title="Freeze Authority Disabled"
            value={!freezeAuthority}
            icon={Wallet}
          />

        </div>

      </div>

      {/* AI */}

      <div>

        <h3 className="mb-4 font-semibold">

          AI Risk Metrics

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <Metric
            icon={Users}
            title="Holder Concentration"
            value={`${holderConcentration}%`}
            color="text-orange-400"
          />

          <Metric
            icon={Eye}
            title="Insider Wallets"
            value={insiderWallets.toString()}
            color="text-red-400"
          />

          <Metric
            icon={ShieldCheck}
            title="Deployer Trust"
            value={`${deployerTrust}/100`}
            color="text-green-400"
          />

          <Metric
            icon={TrendingUp}
            title="Smart Money"
            value={`${smartMoneyExposure}%`}
            color="text-cyan-400"
          />

        </div>

      </div>

      {/* Progress */}

      <div>

        <div className="mb-2 flex justify-between">

          <span>

            Overall Rug Risk

          </span>

          <span>

            {rugProbability}%

          </span>

        </div>

        <div className="h-3 rounded-full bg-zinc-800">

          <div
            className="h-full rounded-full bg-red-500"
            style={{
              width: `${rugProbability}%`,
            }}
          />

        </div>

      </div>

      {/* AI */}

      <div className="rounded-xl border border-red-900 bg-red-950/20 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            className="text-red-400"
            size={20}
          />

          <span className="font-semibold">

            Sentinel AI Explanation

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiExplanation}

        </p>

        </div>

        {/* AI Summary */}

        <div className="rounded-xl border border-cyan-900 bg-cyan-950/20 p-5">