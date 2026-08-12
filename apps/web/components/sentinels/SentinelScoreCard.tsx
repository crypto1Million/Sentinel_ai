"use client";

import {
  ShieldCheck,
  Brain,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Target,
  Activity,
  BarChart3,
  Wallet,
  Fish,
  Flame,
  Sparkles,
  ChevronRight,
} from "lucide-react";

interface SentinelScoreCardProps {
  sentinelScore: number;

  confidence: number;

  recommendation: "BUY" | "WATCH" | "AVOID";

  opportunityScore: number;

  walletScore: number;

  narrativeScore: number;

  rugScore: number;

  momentumScore: number;

  liquidityScore: number;

  holderScore: number;

  aiSummary: string;

  updatedAt: string;
}

interface ScoreCardProps {
  title: string;

  score: number;

  icon: React.ElementType;

  color: string;
}

function ScoreCard({
  title,
  score,
  icon: Icon,
  color,
}: ScoreCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-4">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          size={18}
          className={color}
        />

        <span className="text-sm text-zinc-400">
          {title}
        </span>

      </div>

      <div className="text-2xl font-bold">

        {score}

      </div>

      <div className="mt-3 h-2 overflow-hidden rounded-full bg-zinc-800">

        <div
          className="h-full rounded-full bg-cyan-500"
          style={{
            width: `${score}%`,
          }}
        />

      </div>

    </div>
  );
}

export default function SentinelScoreCard({
  sentinelScore,

  confidence,

  recommendation,

  opportunityScore,

  walletScore,

  narrativeScore,

  rugScore,

  momentumScore,

  liquidityScore,

  holderScore,

  aiSummary,

  updatedAt,
}: SentinelScoreCardProps) {
  const recommendationColor =
    recommendation === "BUY"
      ? "text-green-400"
      : recommendation === "WATCH"
      ? "text-yellow-400"
      : "text-red-400";

  const RecommendationIcon =
    recommendation === "BUY"
      ? TrendingUp
      : recommendation === "WATCH"
      ? Activity
      : TrendingDown;

  return (
    <div className="rounded-2xl border border-cyan-900 bg-[#0B1118] p-6 shadow-xl">

      {/* Header */}

      <div className="mb-8 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <ShieldCheck
            size={28}
            className="text-cyan-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              Sentinel Score™

            </h2>

            <p className="text-sm text-zinc-500">

              AI-powered Token Intelligence

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-cyan-500 px-6 py-4 text-center">

          <div className="text-4xl font-black text-black">

            {sentinelScore}

          </div>

          <div className="text-xs font-semibold text-black">

            /100

          </div>

        </div>

      </div>

      {/* Recommendation */}

      <div className="mb-8 rounded-xl border border-zinc-800 bg-[#11161d] p-5">

        <div className="flex items-center justify-between">

          <div>

            <p className="text-sm text-zinc-500">

              AI Recommendation

            </p>

            <div
              className={`mt-2 flex items-center gap-2 text-2xl font-bold ${recommendationColor}`}
            >
              <RecommendationIcon size={24} />

              {recommendation}

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

      {/* Scores */}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

        <ScoreCard
          title="Opportunity"
          score={opportunityScore}
          icon={Target}
          color="text-green-400"
        />

        <ScoreCard
          title="Wallet DNA"
          score={walletScore}
          icon={Wallet}
          color="text-blue-400"
        />

        <ScoreCard
          title="Narrative"
          score={narrativeScore}
          icon={Sparkles}
          color="text-purple-400"
        />

        <ScoreCard
          title="Rug Radar"
          score={rugScore}
          icon={AlertTriangle}
          color="text-red-400"
        />

        <ScoreCard
          title="Momentum"
          score={momentumScore}
          icon={TrendingUp}
          color="text-green-400"
        />

        <ScoreCard
          title="Liquidity"
          score={liquidityScore}
          icon={BarChart3}
          color="text-cyan-400"
        />

        <ScoreCard
          title="Holder Quality"
          score={holderScore}
          icon={Fish}
          color="text-yellow-400"
        />

      </div>

      {/* AI Summary */}

      <div className="mt-8 rounded-xl border border-cyan-900 bg-cyan-950/30 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            size={20}
            className="text-cyan-400"
          />

          <span className="font-semibold">

            Sentinel AI Summary

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiSummary}

        </p>

      </div>

      {/* Footer */}

      <div className="mt-8 flex items-center justify-between text-sm text-zinc-500">

        <span>

          Updated: {updatedAt}

        </span>

        <button className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300">

          View Full Analysis

          <ChevronRight size={18} />

        </button>

      </div>

    </div>
  );
}
