"use client";

import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  CheckCircle2,
  Lock,
  Coins,
  Wallet,
  Users,
  Activity,
  TrendingDown,
  TrendingUp,
  Brain,
  Eye,
  Flame,
} from "lucide-react";

interface RiskMetricsProps {
  contractRisk: number;

  liquidityRisk: number;

  holderRisk: number;

  deployerRisk: number;

  mevRisk: number;

  whaleRisk: number;

  exitLiquidityRisk: number;

  insiderRisk: number;

  honeypotRisk: number;

  sniperRisk: number;

  rugProbability: number;

  liquidityLocked: boolean;

  ownershipRenounced: boolean;

  mintDisabled: boolean;

  freezeDisabled: boolean;
}

export default function RiskMetrics({
  contractRisk,
  liquidityRisk,
  holderRisk,
  deployerRisk,
  mevRisk,
  whaleRisk,
  exitLiquidityRisk,
  insiderRisk,
  honeypotRisk,
  sniperRisk,
  rugProbability,
  liquidityLocked,
  ownershipRenounced,
  mintDisabled,
  freezeDisabled,
}: RiskMetricsProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center gap-3">

        <ShieldAlert
          size={28}
          className="text-red-400"
        />

        <div>

          <h2 className="text-2xl font-bold">

            Risk Metrics

          </h2>

          <p className="text-sm text-zinc-500">

            Multi-engine security analysis

          </p>

        </div>

      </div>

      {/* Main Scores */}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">

        <RiskCard
          title="Contract"
          value={contractRisk}
          icon={ShieldAlert}
        />

        <RiskCard
          title="Liquidity"
          value={liquidityRisk}
          icon={Activity}
        />

        <RiskCard
          title="Holder"
          value={holderRisk}
          icon={Users}
        />

        <RiskCard
          title="Deployer"
          value={deployerRisk}
          icon={Wallet}
        />

        <RiskCard
          title="MEV"
          value={mevRisk}
          icon={TrendingDown}
        />

      </div>

      {/* Advanced */}

      <div>

        <h3 className="mb-4 font-semibold">

          Advanced Detection

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <RiskItem
            title="Whale Dump Risk"
            value={`${whaleRisk}%`}
            icon={TrendingDown}
          />

          <RiskItem
            title="Exit Liquidity"
            value={`${exitLiquidityRisk}%`}
            icon={Flame}
          />

          <RiskItem
            title="Insider Wallets"
            value={`${insiderRisk}%`}
            icon={Eye}
          />

          <RiskItem
            title="Honeypot"
            value={`${honeypotRisk}%`}
            icon={AlertTriangle}
          />

          <RiskItem
            title="Sniper"
            value={`${sniperRisk}%`}
            icon={Brain}
          />

          <RiskItem
            title="Rug Probability"
            value={`${rugProbability}%`}
            icon={ShieldAlert}
          />

        </div>

      </div>

      {/* Contract Checks */}

      <div>

        <h3 className="mb-4 font-semibold">

          Smart Contract Verification

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <BooleanCheck
            title="Liquidity Locked"
            value={liquidityLocked}
            icon={Lock}
          />

          <BooleanCheck
            title="Ownership Renounced"
            value={ownershipRenounced}
            icon={ShieldCheck}
          />

          <BooleanCheck
            title="Mint Disabled"
            value={mintDisabled}
            icon={Coins}
          />

          <BooleanCheck
            title="Freeze Disabled"
            value={freezeDisabled}
            icon={Wallet}
          />

        </div>

      </div>

    </div>
  );
}

function RiskCard({
  title,
  value,
  icon: Icon,
}: {
  title: string;
  value: number;
  icon: React.ElementType;
}) {
  const color =
    value <= 30
      ? "text-green-400"
      : value <= 70
      ? "text-yellow-400"
      : "text-red-400";

  return (
    <div className="rounded-xl bg-[#1B2330] p-5">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          size={18}
          className={color}
        />

        <span className="text-sm text-zinc-400">

          {title}

        </span>

      </div>

      <div className={`text-3xl font-bold ${color}`}>

        {value}

      </div>

      <div className="mt-3 h-2 rounded-full bg-zinc-700">

        <div
          className={`h-full rounded-full ${
            value <= 30
              ? "bg-green-500"
              : value <= 70
              ? "bg-yellow-500"
              : "bg-red-500"
          }`}
          style={{
            width: `${value}%`,
          }}
        />

      </div>

    </div>
  );
}

function RiskItem({
  title,
  value,
  icon: Icon,
}: {
  title: string;
  value: string;
  icon: React.ElementType;
}) {
  return (
    <div className="rounded-xl bg-[#1B2330] p-4">

      <div className="mb-2 flex items-center gap-2">

        <Icon
          className="text-red-400"
          size={18}
        />

        <span className="text-sm text-zinc-400">

          {title}

        </span>

      </div>

      <div className="text-xl font-bold">

        {value}

      </div>

    </div>
  );
}

function BooleanCheck({
  title,
  value,
  icon: Icon,
}: {
  title: string;
  value: boolean;
  icon: React.ElementType;
}) {
  return (
    <div className="rounded-xl bg-[#1B2330] p-5">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          size={18}
          className={
            value
              ? "text-green-400"
              : "text-red-400"
          }
        />

        <span className="text-sm text-zinc-400">

          {title}

        </span>

      </div>

      <div className="flex items-center gap-2">

        {value ? (
          <>
            <CheckCircle2 className="text-green-400" />
            <span className="text-green-400 font-semibold">
              PASS
            </span>
          </>
        ) : (
          <>
            <AlertTriangle className="text-red-400" />
            <span className="text-red-400 font-semibold">
              FAIL
            </span>
          </>
        )}

      </div>

    </div>
  );
}
