"use client";

import {
  Brain,
  Sparkles,
  ShieldCheck,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Wallet,
  Flame,
  Coins,
  Activity,
  ChevronRight,
  Clock3,
} from "lucide-react";

interface AIReason {
  title: string;
  description: string;
  impact: "positive" | "negative" | "neutral";
}

interface AIExplanationProps {
  confidence: number;

  summary: string;

  prediction: string;

  recommendation: "BUY" | "WATCH" | "AVOID";

  lastUpdated: string;

  reasons: AIReason[];

  strengths: string[];

  weaknesses: string[];

  nextUpdateETA?: string;
}

export default function AIExplanation({
  confidence,
  summary,
  prediction,
  recommendation,
  lastUpdated,
  reasons,
  strengths,
  weaknesses,
  nextUpdateETA,
}: AIExplanationProps) {
  const recommendationColor =
    recommendation === "BUY"
      ? "text-green-400"
      : recommendation === "WATCH"
      ? "text-yellow-400"
      : "text-red-400";

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

              AI Explanation

            </h2>

            <p className="text-sm text-zinc-500">

              Sentinel reasoning engine

            </p>

          </div>

        </div>

        <div className="rounded-xl bg-cyan-500 px-6 py-4">

          <div className="text-3xl font-black text-black">

            {confidence}%

          </div>

          <div className="text-xs font-semibold text-black">

            Confidence

          </div>

        </div>

      </div>

      {/* Recommendation */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="flex justify-between items-center">

          <div>

            <p className="text-sm text-zinc-500">

              AI Recommendation

            </p>

            <div
              className={`mt-2 text-2xl font-bold ${recommendationColor}`}
            >

              {recommendation}

            </div>

          </div>

          <ChevronRight
            className="text-cyan-400"
            size={28}
          />

        </div>

      </div>

      {/* Summary */}

      <div className="rounded-xl border border-cyan-900 bg-cyan-950/20 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Sparkles
            className="text-cyan-400"
            size={20}
          />

          <span className="font-semibold">

            AI Summary

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {summary}

        </p>

      </div>

      {/* Why */}

      <div>

        <h3 className="mb-4 font-semibold">

          Why did Sentinel reach this conclusion?

        </h3>

        <div className="space-y-4">

          {reasons.map((reason, index) => {

            const Icon =
              reason.impact === "positive"
                ? TrendingUp
                : reason.impact === "negative"
                ? TrendingDown
                : Activity;

            const color =
              reason.impact === "positive"
                ? "text-green-400"
                : reason.impact === "negative"
                ? "text-red-400"
                : "text-yellow-400";

            return (
              <div
                key={index}
                className="rounded-xl border border-zinc-800 bg-[#1B2330] p-4"
              >

                <div className="mb-2 flex items-center gap-3">

                  <Icon
                    size={18}
                    className={color}
                  />

                  <h4 className="font-semibold">

                    {reason.title}

                  </h4>

                </div>

                <p className="text-sm text-zinc-400">

                  {reason.description}

                </p>

              </div>
            );
          })}

        </div>

      </div>

      {/* Strengths */}

      <div>

        <h3 className="mb-4 flex items-center gap-2 font-semibold">

          <ShieldCheck
            className="text-green-400"
            size={20}
          />

          Strengths

        </h3>

        <div className="space-y-2">

          {strengths.map((item, index) => (
            <div
              key={index}
              className="rounded-lg bg-green-950/20 border border-green-900 p-3 text-sm text-green-300"
            >
              • {item}
            </div>
          ))}

        </div>

      </div>

      {/* Weaknesses */}

      <div>

        <h3 className="mb-4 flex items-center gap-2 font-semibold">

          <AlertTriangle
            className="text-yellow-400"
            size={20}
          />

          Weaknesses

        </h3>

        <div className="space-y-2">

          {weaknesses.map((item, index) => (
            <div
              key={index}
              className="rounded-lg bg-yellow-950/20 border border-yellow-900 p-3 text-sm text-yellow-300"
            >
              • {item}
            </div>
          ))}

        </div>

      </div>

      {/* Prediction */}

      <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            className="text-cyan-400"
            size={20}
          />

          <span className="font-semibold">

            AI Prediction

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {prediction}

        </p>

      </div>

      {/* Engines Used */}

      <div>

        <h3 className="mb-4 font-semibold">

          AI Engines Used

        </h3>

        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">

          <Engine title="Wallet DNA" icon={Wallet} />

          <Engine title="Rug Radar" icon={ShieldCheck} />

          <Engine title="Narrative Engine" icon={Flame} />

          <Engine title="Market Intelligence" icon={Coins} />

        </div>

      </div>

      {/* Footer */}

      <div className="flex justify-between text-sm text-zinc-500">

        <div className="flex items-center gap-2">

          <Clock3 size={16} />

          Updated: {lastUpdated}

        </div>

        {nextUpdateETA && (

          <div>

            Next Scan: {nextUpdateETA}

          </div>

        )}

      </div>

    </div>
  );
}

function Engine({
  title,
  icon: Icon,
}: {
  title: string;
  icon: React.ElementType;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-[#1B2330] p-4">

      <div className="flex items-center gap-3">

        <Icon
          size={18}
          className="text-cyan-400"
        />

        <span className="font-medium">

          {title}

        </span>

      </div>

    </div>
  );
}

