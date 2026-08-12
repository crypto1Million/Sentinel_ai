"use client";

import {
  Flame,
  Brain,
  Sparkles,
  TrendingUp,
  Globe,
  MessageCircle,
  Hash,
  Newspaper,
  Activity,
  Rocket,
  Users,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";

interface NarrativeScoreProps {
  narrativeScore: number;

  confidence: number;

  dominantNarrative: string;

  narrativeStrength: number;

  trendVelocity: number;

  socialMomentum: number;

  twitterMentions: number;

  telegramGrowth: number;

  mindshare: number;

  smartMoneyAlignment: number;

  aiTrendPrediction: number;

  sentimentScore: number;

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

export default function NarrativeScore({
  narrativeScore,
  confidence,
  dominantNarrative,
  narrativeStrength,
  trendVelocity,
  socialMomentum,
  twitterMentions,
  telegramGrowth,
  mindshare,
  smartMoneyAlignment,
  aiTrendPrediction,
  sentimentScore,
  aiSummary,
}: NarrativeScoreProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div className="flex items-center gap-3">

          <Flame
            size={28}
            className="text-orange-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              Narrative Score

            </h2>

            <p className="text-sm text-zinc-500">

              AI Narrative Intelligence

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-orange-500 px-6 py-4">

          <div className="text-4xl font-black text-black">

            {narrativeScore}

          </div>

          <div className="text-center text-xs font-semibold text-black">

            /100

          </div>

        </div>

      </div>

      {/* Narrative */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center justify-between">

          <div>

            <p className="text-sm text-zinc-500">

              Dominant Narrative

            </p>

            <div className="mt-2 text-2xl font-bold text-orange-400">

              {dominantNarrative}

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

      {/* Metrics */}

      <div>

        <h3 className="mb-4 font-semibold">

          Narrative Intelligence

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">

          <MetricCard
            title="Narrative Strength"
            value={`${narrativeStrength}/100`}
            icon={Rocket}
            color="text-orange-400"
          />

          <MetricCard
            title="Trend Velocity"
            value={`${trendVelocity}/100`}
            icon={TrendingUp}
            color="text-green-400"
          />

          <MetricCard
            title="Social Momentum"
            value={`${socialMomentum}/100`}
            icon={Activity}
          />

          <MetricCard
            title="Twitter Mentions"
            value={twitterMentions.toLocaleString()}
            icon={Hash}
            color="text-blue-400"
          />

          <MetricCard
            title="Telegram Growth"
            value={`${telegramGrowth}%`}
            icon={MessageCircle}
            color="text-cyan-400"
          />

          <MetricCard
            title="Mindshare"
            value={`${mindshare}%`}
            icon={Globe}
          />

          <MetricCard
            title="Smart Money Alignment"
            value={`${smartMoneyAlignment}/100`}
            icon={Brain}
            color="text-green-400"
          />

          <MetricCard
            title="AI Trend Prediction"
            value={`${aiTrendPrediction}%`}
            icon={Sparkles}
            color="text-purple-400"
          />

          <MetricCard
            title="Sentiment Score"
            value={`${sentimentScore}/100`}
            icon={Users}
            color="text-yellow-400"
          />

        </div>

      </div>

      {/* AI Summary */}

      <div className="rounded-xl border border-orange-700 bg-orange-950/20 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            size={20}
            className="text-orange-400"
          />

          <span className="font-semibold">

            Sentinel Narrative Analysis

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiSummary}

        </p>

      </div>

      {/* Verdict */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex items-center gap-3">

          {narrativeScore >= 80 ? (
            <CheckCircle2
              className="text-green-400"
              size={24}
            />
          ) : (
            <AlertTriangle
              className="text-yellow-400"
              size={24}
            />
          )}

          <div>

            <div className="font-semibold">

              Narrative Verdict

            </div>

            <div className="text-sm text-zinc-400">

              {narrativeScore >= 80
                ? "This narrative is rapidly gaining traction across social platforms and aligns with current market attention."
                : narrativeScore >= 60
                ? "Narrative is emerging but requires continued momentum."
                : "Weak narrative with limited market attention."}

            </div>

          </div>

        </div>

      </div>

      {/* Sources */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="mb-4 flex items-center gap-2">

          <Newspaper
            size={20}
            className="text-cyan-400"
          />

          <span className="font-semibold">

            AI Data Sources

          </span>

        </div>

        <div className="grid gap-2 text-sm text-zinc-400 md:grid-cols-2">

          <div>• X (Twitter)</div>
          <div>• Telegram</div>
          <div>• DexScreener</div>
          <div>• Pump.fun</div>
          <div>• Smart Money Wallets</div>
          <div>• KOL Tracking</div>
          <div>• Holder Growth</div>
          <div>• Trading Volume</div>

        </div>

      </div>

    </div>
  );
}
