"use client";

import {
  Target,
  TrendingUp,
  TrendingDown,
  Brain,
  Rocket,
  Coins,
  Wallet,
  Activity,
  BarChart3,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";

interface OpportunityScoreProps {
  score: number;

  confidence: number;

  rating: "Strong Buy" | "Buy" | "Neutral" | "Avoid";

  upsidePotential: number;

  riskReward: number;

  expectedROI: number;

  smartMoneyScore: number;

  narrativeStrength: number;

  momentumScore: number;

  liquidityScore: number;

  walletGrowth: number;

  volumeGrowth: number;

  marketCap: number;

  aiSummary: string;
}

interface MetricProps {
  title: string;
  value: string;
  icon: React.ElementType;
  color?: string;
}

function Metric({
  title,
  value,
  icon: Icon,
  color = "text-cyan-400",
}: MetricProps) {
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

export default function OpportunityScore({

  score,

  confidence,

  rating,

  upsidePotential,

  riskReward,

  expectedROI,

  smartMoneyScore,

  narrativeStrength,

  momentumScore,

  liquidityScore,

  walletGrowth,

  volumeGrowth,

  marketCap,

  aiSummary,

}: OpportunityScoreProps) {

  const ratingColor =
    rating === "Strong Buy"
      ? "text-green-400"
      : rating === "Buy"
      ? "text-cyan-400"
      : rating === "Neutral"
      ? "text-yellow-400"
      : "text-red-400";

  return (

    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div className="flex items-center gap-3">

          <Target
            size={28}
            className="text-cyan-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              Opportunity Score

            </h2>

            <p className="text-sm text-zinc-500">

              AI Opportunity Analysis

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-cyan-500 px-6 py-4">

          <div className="text-4xl font-black text-black">

            {score}

          </div>

          <div className="text-center text-xs font-semibold text-black">

            /100

          </div>

        </div>

      </div>

      {/* Rating */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex justify-between">

          <div>

            <p className="text-sm text-zinc-500">

              AI Rating

            </p>

            <div
              className={`mt-2 text-2xl font-bold ${ratingColor}`}
            >

              {rating}

            </div>

          </div>

          <div className="text-right">

            <p className="text-sm text-zinc-500">

              Confidence

            </p>

            <div className="mt-2 text-3xl font-bold text-cyan-400">

              {confidence}%

            </div>

          </div>

        </div>

      </div>

      {/* Core Metrics */}

      <div>

        <h3 className="mb-4 font-semibold">

          Opportunity Metrics

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <Metric
            title="Upside Potential"
            value={`${upsidePotential}x`}
            icon={Rocket}
            color="text-green-400"
          />

          <Metric
            title="Risk / Reward"
            value={`${riskReward}:1`}
            icon={TrendingUp}
            color="text-cyan-400"
          />

          <Metric
            title="Expected ROI"
            value={`${expectedROI}%`}
            icon={BarChart3}
            color="text-green-400"
          />

          <Metric
            title="Smart Money"
            value={`${smartMoneyScore}/100`}
            icon={Wallet}
          />

          <Metric
            title="Narrative"
            value={`${narrativeStrength}/100`}
            icon={Sparkles}
            color="text-purple-400"
          />

          <Metric
            title="Momentum"
            value={`${momentumScore}/100`}
            icon={TrendingUp}
            color="text-green-400"
          />

          <Metric
            title="Liquidity"
            value={`${liquidityScore}/100`}
            icon={Coins}
          />

          <Metric
            title="Wallet Growth"
            value={`${walletGrowth}%`}
            icon={Activity}
          />

          <Metric
            title="Volume Growth"
            value={`${volumeGrowth}%`}
            icon={TrendingUp}
            color="text-green-400"
          />

        </div>

      </div>

      {/* Market Cap */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center justify-between">

          <div>

            <p className="text-sm text-zinc-500">

              Current Market Cap

            </p>

            <div className="mt-2 text-3xl font-bold">

              ${marketCap.toLocaleString()}

            </div>

          </div>

          <TrendingUp
            size={48}
            className="text-cyan-400"
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

            Sentinel AI Analysis

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiSummary}

        </p>

      </div>

      {/* Verdict */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center gap-3">

          {score >= 80 ? (

            <CheckCircle2
              size={24}
              className="text-green-400"
            />

          ) : (

            <AlertTriangle
              size={24}
              className="text-yellow-400"
            />

          )}

          <div>

            <div className="font-semibold">

              Sentinel Verdict

            </div>

            <div className="text-sm text-zinc-400">

              {score >= 80
                ? "Exceptional opportunity based on AI, Wallet DNA and Market Intelligence."
                : score >= 60
                ? "Promising opportunity, monitor before entry."
                : "Low opportunity score. Consider waiting for confirmation."}

            </div>

          </div>

        </div>

      </div>

    </div>

  );

}
