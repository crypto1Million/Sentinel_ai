"use client";

import { useEffect, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";

import api from "@/services/api";

import SentinelScoreCard, {
  type SentinelScoreResponse,
} from "@/components/sentinels/SentinelScoreCard";

export default function TokenDetailPage() {
  const params = useParams<{ mint: string }>();
  const searchParams = useSearchParams();

  const mint = params.mint;
  const chain = searchParams.get("chain") || "solana";

  const [score, setScore] =
    useState<SentinelScoreResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadScore() {
      setLoading(true);
      setError(null);

      try {
        const response = await api.get<SentinelScoreResponse>(
          `/scores/${encodeURIComponent(mint)}`,
          {
            params: { chain },
          }
        );

        if (!cancelled) {
          setScore(response.data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to retrieve Sentinel Score."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    if (mint) {
      void loadScore();
    }

    return () => {
      cancelled = true;
    };
  }, [mint, chain]);

  return (
    <div className="mx-auto max-w-6xl space-y-6">

      <div>
        <p className="text-xs uppercase tracking-widest text-[#D4AF37]">
          SENTINEL INTELLIGENCE
        </p>

        <h1 className="mt-2 text-3xl font-bold text-white">
          Token Analysis
        </h1>

        <p className="mt-2 break-all font-mono text-xs text-zinc-500">
          {mint} · {chain}
        </p>
      </div>

      {loading && (
        <p className="text-sm text-zinc-400">
          Calculating Sentinel Score...
        </p>
      )}

      {error && (
        <div className="rounded-xl border border-red-900 bg-red-950/20 p-5 text-red-300">
          {error}
        </div>
      )}

      {!loading && score && (
        <SentinelScoreCard data={score} />
      )}

    </div>
  );
}