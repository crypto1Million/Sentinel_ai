id="rug8qa"
"use client";

import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Lock,
  Flame,
  Coins,
  Wallet,
  UserX,
  Activity,
  Brain,
  TrendingDown,
  CheckCircle2,
  XCircle,
  Eye,
} from "lucide-react";

interface RugScoreProps {
  rugScore: number;

  riskLevel: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

  confidence: number;

  liquidityLocked: boolean;

  liquidityBurned: boolean;

  mintAuthority: boolean;

  freezeAuthority: boolean;

  ownershipRenounced: boolean;

  honeypotRisk: number;

  sniperRisk: number;

  insiderRisk: number;

  walletConcentration: number;

  deployerTrust: number;

  aiSummary: string;
}

interface RiskMetricProps {
  title: string;
  value: string;
  icon: React.ElementType;
  color?: string;
}

function RiskMetric({
  title,
  value,
  icon: Icon,
  color = "text-cyan-400",
}: RiskMetricProps) {
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

export default function RugScore({
  rugScore,
  riskLevel,
  confidence,
  liquidityLocked,
  liquidityBurned,
  mintAuthority,
  freezeAuthority,
  ownershipRenounced,
  honeypotRisk,
  sniperRisk,
  insiderRisk,
  walletConcentration,
  deployerTrust,
  aiSummary,
}: RugScoreProps) {

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
            size={28}
            className="text-red-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              Rug Radar™

            </h2>

            <p className="text-sm text-zinc-500">

              AI Rug Detection Engine

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-red-500 px-6 py-4">

          <div className="text-4xl font-black text-black">

            {rugScore}

          </div>

          <div className="text-center text-xs font-semibold text-black">

            /100

          </div>

        </div>

      </div>

      {/* Risk */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex justify-between">

          <div>

            <p className="text-sm text-zinc-500">

              Overall Risk

            </p>

            <div className={`mt-2 text-3xl font-bold ${riskColor}`}>

              {riskLevel}

            </div>

          </div>

          <div className="text-right">

            <p className="text-sm text-zinc-500">

              AI Confidence

            </p>

            <div className="mt-2 text-3xl font-bold text-cyan-400">

              {confidence}%

            </div>

          </div>

        </div>

      </div>

      {/* Security */}

      <div>

        <h3 className="mb-4 font-semibold">

          Smart Contract Security

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <RiskMetric
            title="Liquidity Locked"
            value={liquidityLocked ? "YES" : "NO"}
            icon={Lock}
            color={liquidityLocked ? "text-green-400" : "text-red-400"}
          />

          <RiskMetric
            title="Liquidity Burned"
            value={liquidityBurned ? "YES" : "NO"}
            icon={Flame}
            color={liquidityBurned ? "text-green-400" : "text-red-400"}
          />

          <RiskMetric
            title="Mint Authority"
            value={mintAuthority ? "ACTIVE" : "DISABLED"}
            icon={Coins}
            color={mintAuthority ? "text-red-400" : "text-green-400"}
          />

          <RiskMetric
            title="Freeze Authority"
            value={freezeAuthority ? "ACTIVE" : "DISABLED"}
            icon={Wallet}
            color={freezeAuthority ? "text-red-400" : "text-green-400"}
          />

          <RiskMetric
            title="Ownership"
            value={ownershipRenounced ? "RENOUNCED" : "ACTIVE"}
            icon={UserX}
            color={ownershipRenounced ? "text-green-400" : "text-red-400"}
          />

        </div>

      </div>

      {/* AI Risk Metrics */}

      <div>

        <h3 className="mb-4 font-semibold">

          AI Risk Analysis

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <RiskMetric
            title="Honeypot Risk"
            value={`${honeypotRisk}%`}
            icon={AlertTriangle}
            color="text-red-400"
          />

          <RiskMetric
            title="Sniper Risk"
            value={`${sniperRisk}%`}
            icon={Eye}
            color="text-orange-400"
          />

          <RiskMetric
            title="Insider Risk"
            value={`${insiderRisk}%`}
            icon={ShieldAlert}
            color="text-yellow-400"
          />

          <RiskMetric
            title="Wallet Concentration"
            value={`${walletConcentration}%`}
            icon={Activity}
          />

          <RiskMetric
            title="Deployer Trust"
            value={`${deployerTrust}/100`}
            icon={ShieldCheck}
            color="text-green-400"
          />

        </div>

      </div>

      {/* AI Summary */}

      <div className="rounded-xl border border-red-900 bg-red-950/20 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            className="text-red-400"
            size={20}
          />

          <span className="font-semibold">

            Sentinel Rug Analysis

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiSummary}

        </p>

      </div>

      {/* Verdict */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center gap-3">

          {rugScore <= 30 ? (

            <CheckCircle2
              size={24}
              className="text-green-400"
            />

          ) : rugScore <= 70 ? (

            <AlertTriangle
              size={24}
              className="text-yellow-400"
            />

          ) : (

            <XCircle
              size={24}
              className="text-red-500"
            />

          )}

          <div>

            <div className="font-semibold">

              Sentinel Verdict

            </div>

            <div className="text-sm text-zinc-400">

              {rugScore <= 30
                ? "Low rug probability. Security signals are healthy."
                : rugScore <= 70
                ? "Moderate risk detected. Additional monitoring is recommended."
                : "High rug probability. Multiple high-risk indicators have been identified."}

            </div>

          </div>

        </div>

      </div>

    </div>

  );

}

