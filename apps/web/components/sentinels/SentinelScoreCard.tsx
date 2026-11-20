"use client";

import Image from "next/image";

export interface PillarScore {
  score: number | null;
  coverage_pct: number;
  confidence_pct: number;
  notes?: string[];
  details?: Record<string, unknown>;
}

export interface SentinelScoreResponse {
  mint: string;
  chain: string;

  model_name: string;
  model_version: string;

  potential_score: number | null;
  potential_status: string;
  potential_grade: string | null;

  rug_risk_score: number | null;
  rug_risk_status: string;
  rug_risk_coverage_pct: number;
  rug_risk_confidence_pct: number;

  data_coverage_pct: number;
  confidence_pct: number;

  pillars: Record<string, PillarScore>;

  risk_flags: string[];

  risk_components: {
    name: string;
    risk_score: number | null;
    weight: number;
  }[];

  rug_hard_veto: boolean;
  interpretation: string;
  scored_at: string;
}

const PILLAR_LABELS: Record<string, string> = {
  developer_history: "Developer History",
  developer_wallet: "Developer Wallet",
  narrative: "Narrative",
  initial_money_flow: "Initial Money Flow",
  funding_provenance: "Funding Provenance",
  developer_social: "Developer Social",
};

function formatScore(value: number | null | undefined) {
  return typeof value === "number"
    ? value.toFixed(1)
    : "N/A";
}

function ScorePanel({
  title,
  value,
  description,
}: {
  title: string;
  value: number | null;
  description: string;
}) {
  const tone =
    value === null
      ? "text-zinc-400"
      : value >= 70
      ? "text-emerald-400"
      : value >= 40
      ? "text-yellow-400"
      : "text-red-400";

  return (
    <div className="rounded-xl border border-zinc-800 bg-[#151B23] p-5">

      <p className="text-sm text-zinc-400">
        {title}
      </p>

      <p className={`mt-2 text-3xl font-bold ${tone}`}>
        {formatScore(value)}
        {value !== null && "/100"}
      </p>

      <p className="mt-2 text-xs text-zinc-500">
        {description}
      </p>

    </div>
  );
}

export default function SentinelScoreCard({
  data,
}: {
  data: SentinelScoreResponse;
}) {
  const pillars = Object.entries(data.pillars || {});

  return (
    <div className="space-y-6 rounded-2xl border border-cyan-900 bg-[#0B1118] p-6">

      {/* HEADER */}

      <div className="flex items-center gap-3">

        <Image
          src="/brand/sentinel-mark.svg"
          alt="Sentinel"
          width={32}
          height={32}
        />

        <div>
          <h2 className="text-2xl font-bold text-white">
            Sentinel Score™
          </h2>

          <p className="text-sm text-zinc-500">
            Evidence-based Token Intelligence
          </p>
        </div>

      </div>

      {/* PRIMARY SCORES */}

      <div className="grid gap-4 sm:grid-cols-2">

        <ScorePanel
          title="Potential Score"
          value={data.potential_score}
          description={`Status: ${data.potential_status} • Grade: ${data.potential_grade ?? "N/A"}`}
        />

        <ScorePanel
          title="Independent Rug Risk"
          value={data.rug_risk_score}
          description={`Status: ${data.rug_risk_status}`}
        />

      </div>

      {/* CONFIDENCE */}

      <div className="grid gap-4 sm:grid-cols-2">

        <ScorePanel
          title="Data Coverage"
          value={data.data_coverage_pct}
          description="Percentage of available scoring evidence"
        />

        <ScorePanel
          title="Scoring Confidence"
          value={data.confidence_pct}
          description="Confidence based on available evidence"
        />

      </div>

      {/* SIX PILLARS */}

      <section>

        <h3 className="mb-4 text-lg font-semibold text-white">
          Intelligence Pillars
        </h3>

        <div className="grid gap-4 md:grid-cols-2">

          {pillars.map(([key, pillar]) => {
            const value = pillar.score ?? 0;

            return (
              <div
                key={key}
                className="rounded-xl border border-zinc-800 bg-[#151B23] p-4"
              >

                <div className="mb-3 flex items-center justify-between gap-3">

                  <span className="text-sm text-zinc-300">
                    {PILLAR_LABELS[key] ?? key}
                  </span>

                  <span className="font-bold text-white">
                    {formatScore(pillar.score)}
                  </span>

                </div>

                <div className="h-2 overflow-hidden rounded-full bg-zinc-800">

                  <div
                    className="h-full rounded-full bg-cyan-500"
                    style={{
                      width: `${Math.max(0, Math.min(100, value))}%`,
                    }}
                  />

                </div>

                <div className="mt-3 flex justify-between text-xs text-zinc-500">

                  <span>
                    Coverage: {pillar.coverage_pct}%
                  </span>

                  <span>
                    Confidence: {pillar.confidence_pct}%
                  </span>

                </div>

              </div>
            );
          })}

        </div>

      </section>

      {/* RISK FLAGS */}

      <section className="rounded-xl border border-red-900/50 bg-red-950/20 p-5">

        <h3 className="font-semibold text-white">
          Rug Risk Evidence
        </h3>

        <p className="mt-2 text-sm text-zinc-400">
          Hard veto: {data.rug_hard_veto ? "Triggered" : "Not triggered"}
        </p>

        {data.risk_flags.length > 0 ? (
          <ul className="mt-4 space-y-2">
            {data.risk_flags.map((flag, index) => (
              <li
                key={`${flag}-${index}`}
                className="text-sm text-red-300"
              >
                • {flag}
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-4 text-sm text-zinc-500">
            No risk flags reported by the current scoring response.
          </p>
        )}

      </section>

      {/* INTERPRETATION */}

      <section className="rounded-xl border border-zinc-800 bg-[#11161D] p-5">

        <h3 className="font-semibold text-white">
          Model Interpretation
        </h3>

        <p className="mt-3 text-sm leading-7 text-zinc-400">
          {data.interpretation}
        </p>

        <p className="mt-4 text-xs text-zinc-600">
          Model: {data.model_name} · Version: {data.model_version}
        </p>

      </section>

    </div>
  );
}
