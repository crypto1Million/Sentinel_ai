"use client";

import {
  Droplets,
  Lock,
  Flame,
  TrendingUp,
  TrendingDown,
  Shield,
  AlertTriangle,
  Activity,
  DollarSign,
  ArrowUpRight,
  ArrowDownRight,
  BarChart3,
  Brain,
} from "lucide-react";

interface LiquidityPanelProps {
  currentLiquidity: number;

  initialLiquidity: number;

  liquidityLocked: number;

  liquidityBurned: number;

  liquidityAdded24h: number;

  liquidityRemoved24h: number;

  buyWall: number;

  sellWall: number;

  liquidityHealth: number;

  exitLiquidityScore: number;

  migrationDetected: boolean;

  liquidityProviders: number;

  lpHolders: number;

  topLPHolder: number;

  rugRisk: number;
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

      <div className="text-xl font-semibold">

        {value}

      </div>

    </div>
  );
}

export default function LiquidityPanel({

  currentLiquidity,

  initialLiquidity,

  liquidityLocked,

  liquidityBurned,

  liquidityAdded24h,

  liquidityRemoved24h,

  buyWall,

  sellWall,

  liquidityHealth,

  exitLiquidityScore,

  migrationDetected,

  liquidityProviders,

  lpHolders,

  topLPHolder,

  rugRisk,

}: LiquidityPanelProps) {

  const growth =
    (
      ((currentLiquidity - initialLiquidity) /
        initialLiquidity) *
      100
    ).toFixed(1);

  return (

    <div className="rounded-xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div>

        <div className="flex items-center gap-3">

          <Droplets
            size={24}
            className="text-cyan-400"
          />

          <div>

            <h2 className="text-xl font-bold">

              Liquidity Analysis

            </h2>

            <p className="text-sm text-zinc-500">

              Real-time liquidity intelligence

            </p>

          </div>

        </div>

      </div>

      {/* Core */}

      <div>

        <h3 className="mb-4 font-semibold">

          Liquidity Overview

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <MetricCard
            title="Current Liquidity"
            value={`$${currentLiquidity.toLocaleString()}`}
            icon={DollarSign}
          />

          <MetricCard
            title="Initial Liquidity"
            value={`$${initialLiquidity.toLocaleString()}`}
            icon={BarChart3}
          />

          <MetricCard
            title="Growth"
            value={`${growth}%`}
            icon={TrendingUp}
            color="text-green-400"
          />

          <MetricCard
            title="Providers"
            value={liquidityProviders.toLocaleString()}
            icon={Activity}
          />

        </div>

      </div>

      {/* Security */}

      <div>

        <h3 className="mb-4 font-semibold">

          LP Security

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <MetricCard
            title="Locked"
            value={`${liquidityLocked}%`}
            icon={Lock}
            color="text-green-400"
          />

          <MetricCard
            title="Burned"
            value={`${liquidityBurned}%`}
            icon={Flame}
            color="text-orange-400"
          />

          <MetricCard
            title="LP Holders"
            value={lpHolders.toLocaleString()}
            icon={Activity}
          />

          <MetricCard
            title="Largest LP"
            value={`${topLPHolder}%`}
            icon={Shield}
          />

        </div>

      </div>

      {/* Flow */}

      <div>

        <h3 className="mb-4 font-semibold">

          Liquidity Flow (24H)

        </h3>

        <div className="grid gap-4 md:grid-cols-2">

          <MetricCard
            title="Liquidity Added"
            value={`+$${liquidityAdded24h.toLocaleString()}`}
            icon={ArrowUpRight}
            color="text-green-400"
          />

          <MetricCard
            title="Liquidity Removed"
            value={`-$${liquidityRemoved24h.toLocaleString()}`}
            icon={ArrowDownRight}
            color="text-red-400"
          />

        </div>

      </div>

      {/* Order Walls */}

      <div>

        <h3 className="mb-4 font-semibold">

          Market Depth

        </h3>

        <div className="grid gap-4 md:grid-cols-2">

          <MetricCard
            title="Buy Wall"
            value={`$${buyWall.toLocaleString()}`}
            icon={TrendingUp}
            color="text-green-400"
          />

          <MetricCard
            title="Sell Wall"
            value={`$${sellWall.toLocaleString()}`}
            icon={TrendingDown}
            color="text-red-400"
          />

        </div>

      </div>

      {/* Scores */}

      <div>

        <h3 className="mb-4 font-semibold">

          Sentinel Liquidity Scores

        </h3>

        <div className="grid gap-4 md:grid-cols-3">

          <MetricCard
            title="Liquidity Health"
            value={`${liquidityHealth}/100`}
            icon={Shield}
          />

          <MetricCard
            title="Exit Liquidity"
            value={`${exitLiquidityScore}/100`}
            icon={AlertTriangle}
            color="text-yellow-400"
          />

          <MetricCard
            title="Rug Probability"
            value={`${rugRisk}%`}
            icon={Brain}
            color="text-red-400"
          />

        </div>

      </div>

      {/* Migration */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center gap-3">

          {migrationDetected ? (

            <AlertTriangle
              className="text-yellow-400"
              size={22}
            />

          ) : (

            <Shield
              className="text-green-400"
              size={22}
            />

          )}

          <div>

            <div className="font-semibold">

              Liquidity Migration

            </div>

            <div className="text-sm text-zinc-400">

              {migrationDetected
                ? "Migration activity detected."
                : "No migration detected."}

            </div>

          </div>

        </div>

      </div>

      {/* AI Summary */}

      <div className="rounded-xl border border-cyan-700 bg-cyan-950/30 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            size={20}
            className="text-cyan-400"
          />

          <span className="font-semibold">

            Sentinel AI Analysis

          </span>

        </div>

        <ul className="space-y-2 text-sm text-zinc-300">

          <li>

            • Liquidity Health Score:{" "}
            <strong>{liquidityHealth}/100</strong>

          </li>

          <li>

            • Exit Liquidity Score:{" "}
            <strong>{exitLiquidityScore}/100</strong>

          </li>

          <li>

            • LP Locked:{" "}
            <strong>{liquidityLocked}%</strong>

          </li>

          <li>

            • LP Burned:{" "}
            <strong>{liquidityBurned}%</strong>

          </li>

          <li>

            • Rug Probability:{" "}
            <strong>{rugRisk}%</strong>

          </li>

        </ul>

      </div>

    </div>

  );

}
 