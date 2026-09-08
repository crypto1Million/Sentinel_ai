"use client";

import type { ElementType } from "react";

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
  TrendingUp,
  Eye,
  Skull,
  CheckCircle2,
  XCircle,
} from "lucide-react";

export interface RugRadarProps {
  rugScore: number;
  rugProbability: number;
  confidence: number;

  riskLevel:
    | "LOW"
    | "MEDIUM"
    | "HIGH"
    | "CRITICAL";

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

interface MetricProps {
  icon: ElementType;
  title: string;
  value: string;
  color?: string;
}

function Metric({
  icon: Icon,
  title,
  value,
  color = "text-white",
}: MetricProps) {
  return (
    <div className="rounded-xl border border-[#292929] bg-[#171717] p-4">
      <div className="mb-3 flex items-center gap-2">
        <Icon
          size={18}
          className={color}
        />

        <span className="text-sm text-[#8B8B8B]">
          {title}
        </span>
      </div>

      <div className="text-xl font-semibold text-white">
        {value}
      </div>
    </div>
  );
}

interface BooleanMetricProps {
  title: string;
  value: boolean;
  icon: ElementType;
}

function BooleanMetric({
  title,
  value,
  icon: Icon,
}: BooleanMetricProps) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-[#292929] bg-[#171717] p-4">
      <div className="flex items-center gap-3">
        <Icon
          size={18}
          className={
            value
              ? "text-[#D4AF37]"
              : "text-red-400"
          }
        />

        <span className="text-sm text-[#8B8B8B]">
          {title}
        </span>
      </div>

      <div className="flex items-center gap-2">
        {value ? (
          <>
            <CheckCircle2
              size={18}
              className="text-[#D4AF37]"
            />

            <span className="text-sm font-medium text-[#F5C84C]">
              Safe
            </span>
          </>
        ) : (
          <>
            <XCircle
              size={18}
              className="text-red-400"
            />

            <span className="text-sm font-medium text-red-400">
              Risk
            </span>
          </>
        )}
      </div>
    </div>
  );
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

  const safeProbability = Math.max(
    0,
    Math.min(
      Number.isFinite(rugProbability)
        ? rugProbability
        : 0,
      100
    )
  );

  return (
    <section className="space-y-8 rounded-2xl border border-red-900/70 bg-[#101010] p-6">
      {/* Header */}

      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <ShieldAlert
            size={30}
            className="text-red-400"
          />

          <div>
            <h2 className="text-2xl font-bold text-white">
              Rug Radar
            </h2>

            <p className="text-sm text-[#8B8B8B]">
              Sentinel security intelligence
            </p>
          </div>
        </div>

        <div className="rounded-xl bg-red-500 px-5 py-3">
          <div className="text-3xl font-black text-black">
            {rugScore}
          </div>

          <div className="text-xs font-semibold text-black">
            /100 Risk
          </div>
        </div>
      </div>

      {/* Overall Risk */}

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
          color="text-[#F5C84C]"
        />

        <Metric
          icon={Skull}
          title="Rug Probability"
          value={`${rugProbability}%`}
          color="text-red-400"
        />
      </div>

      {/* Contract Security */}

      <div>
        <h3 className="mb-4 font-semibold text-white">
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

      {/* AI Risk Metrics */}

      <div>
        <h3 className="mb-4 font-semibold text-white">
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
            value={insiderWallets.toLocaleString()}
            color="text-red-400"
          />

          <Metric
            icon={ShieldCheck}
            title="Deployer Trust"
            value={`${deployerTrust}/100`}
            color="text-[#F5C84C]"
          />

          <Metric
            icon={TrendingUp}
            title="Smart Money"
            value={`${smartMoneyExposure}%`}
            color="text-green-400"
          />
        </div>
      </div>

      {/* Rug Probability */}

      <div className="rounded-xl border border-[#292929] bg-[#171717] p-5">
        <div className="mb-2 flex items-center justify-between">
          <span className="text-sm text-[#8B8B8B]">
            Overall Rug Risk
          </span>

          <span className="font-semibold text-red-400">
            {safeProbability.toFixed(1)}%
          </span>
        </div>

        <div className="h-3 overflow-hidden rounded-full bg-[#070707]">
          <div
            className="h-full rounded-full bg-red-500"
            style={{
              width: `${safeProbability}%`,
            }}
          />
        </div>
      </div>

      {/* AI Explanation */}

      <div className="rounded-xl border border-red-900/70 bg-red-950/20 p-5">
        <div className="mb-3 flex items-center gap-2">
          <Brain
            size={20}
            className="text-red-400"
          />

          <span className="font-semibold text-white">
            Sentinel AI Explanation
          </span>
        </div>

        <p className="leading-7 text-zinc-300">
          {aiSummary}
        </p>
      </div>
    </section>
  );
}