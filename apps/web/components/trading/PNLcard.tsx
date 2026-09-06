"use client";

import {
  Clock3,
  TrendingDown,
  TrendingUp,
  Wallet,
} from "lucide-react";

interface PNLCardProps {
  tokenName: string;
  tokenSymbol: string;

  pnlSol: number;
  pnlUsd?: number | null;
  roiPercent: number;

  entryMarketCap?: number | null;
  exitMarketCap?: number | null;

  positionSizeSol: number;
  durationSeconds?: number | null;

  tokenImageUrl?: string | null;
  traderHandle?: string | null;

  cardType?: "profit" | "major_win" | "huge_win" | "loss";
}

function formatUsd(value?: number | null) {
  if (value == null) return null;

  const sign = value >= 0 ? "+" : "-";

  return `${sign}$${Math.abs(value).toLocaleString(
    "en-US",
    {
      maximumFractionDigits: 2,
    }
  )}`;
}

function formatSol(value: number) {
  const sign = value >= 0 ? "+" : "-";

  return `${sign}${Math.abs(value).toFixed(4)} SOL`;
}

function formatPercent(value: number) {
  const sign = value >= 0 ? "+" : "-";

  return `${sign}${Math.abs(value).toFixed(2)}%`;
}

function formatDuration(
  seconds?: number | null
) {
  if (seconds == null) return "—";

  const hours = Math.floor(
    seconds / 3600
  );

  const minutes = Math.floor(
    (seconds % 3600) / 60
  );

  const remainingSeconds =
    seconds % 60;

  if (hours > 0) {
    return `${hours}h ${minutes}m ${remainingSeconds}s`;
  }

  if (minutes > 0) {
    return `${minutes}m ${remainingSeconds}s`;
  }

  return `${remainingSeconds}s`;
}

export default function PNLCard({
  tokenName,
  tokenSymbol,

  pnlSol,
  pnlUsd,
  roiPercent,

  entryMarketCap,
  exitMarketCap,

  positionSizeSol,
  durationSeconds,

  tokenImageUrl,
  traderHandle,

  cardType = "profit",
}: PNLCardProps) {

  const isProfit = pnlSol >= 0;

  return (
    <div className="relative overflow-hidden rounded-3xl border border-zinc-800 bg-[#0B0F14] shadow-2xl">

      {tokenImageUrl && (
        <div
          className="absolute inset-0 bg-cover bg-center opacity-20"
          style={{
            backgroundImage:
              `url(${tokenImageUrl})`,
          }}
        />
      )}

      <div className="absolute inset-0 bg-gradient-to-br from-[#0B0F14]/90 via-[#0B0F14]/95 to-[#111923]/95" />

      <div className="relative z-10 p-6 sm:p-8">

        {/* Branding */}

        <div className="mb-6 flex items-center justify-between">

          <div>
            <div className="text-sm font-bold tracking-[0.2em] text-cyan-400">
              SENTINEL AI
            </div>

            <div className="mt-1 text-xs text-zinc-500">
              TRADE PERFORMANCE
            </div>
          </div>

          <div className="rounded-full border border-zinc-700 bg-black/40 px-3 py-1 text-xs text-zinc-400">
            {cardType.replace("_", " ").toUpperCase()}
          </div>

        </div>

        {/* Token */}

        <div className="mb-8 flex items-center gap-4">

          {tokenImageUrl ? (
            <img
              src={tokenImageUrl}
              alt={tokenName}
              className="h-16 w-16 rounded-2xl object-cover ring-1 ring-zinc-700"
            />
          ) : (
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-zinc-800 text-xl font-bold">
              {tokenSymbol.slice(0, 2)}
            </div>
          )}

          <div>
            <div className="text-xl font-semibold text-white">
              {tokenName}
            </div>

            <div className="text-sm text-zinc-500">
              ${tokenSymbol}
            </div>
          </div>

        </div>

        {/* PNL */}

        <div className="mb-8">

          <div
            className={
              isProfit
                ? "text-5xl font-black tracking-tight text-green-400"
                : "text-5xl font-black tracking-tight text-red-400"
            }
          >
            {pnlUsd != null
              ? formatUsd(pnlUsd)
              : formatSol(pnlSol)}
          </div>

          <div className="mt-2 flex items-center gap-3">

            {isProfit ? (
              <TrendingUp
                size={18}
                className="text-green-400"
              />
            ) : (
              <TrendingDown
                size={18}
                className="text-red-400"
              />
            )}

            <span
              className={
                isProfit
                  ? "font-semibold text-green-400"
                  : "font-semibold text-red-400"
              }
            >
              {formatSol(pnlSol)}
            </span>

            <span className="text-zinc-600">
              •
            </span>

            <span
              className={
                isProfit
                  ? "font-semibold text-green-400"
                  : "font-semibold text-red-400"
              }
            >
              {formatPercent(roiPercent)}
            </span>

          </div>

        </div>

        {/* Stats */}

        <div className="grid grid-cols-2 gap-3">

          <div className="rounded-2xl border border-zinc-800 bg-black/30 p-4">

            <div className="mb-1 text-xs uppercase tracking-wider text-zinc-500">
              Position
            </div>

            <div className="flex items-center gap-2 text-sm font-semibold text-white">
              <Wallet
                size={15}
                className="text-cyan-400"
              />
              {positionSizeSol.toFixed(4)} SOL
            </div>

          </div>

          <div className="rounded-2xl border border-zinc-800 bg-black/30 p-4">

            <div className="mb-1 text-xs uppercase tracking-wider text-zinc-500">
              Duration
            </div>

            <div className="flex items-center gap-2 text-sm font-semibold text-white">
              <Clock3
                size={15}
                className="text-cyan-400"
              />
              {formatDuration(durationSeconds)}
            </div>

          </div>

          {entryMarketCap != null && (
            <div className="rounded-2xl border border-zinc-800 bg-black/30 p-4">

              <div className="mb-1 text-xs uppercase tracking-wider text-zinc-500">
                Entry MC
              </div>

              <div className="text-sm font-semibold text-white">
                ${entryMarketCap.toLocaleString()}
              </div>

            </div>
          )}

          {exitMarketCap != null && (
            <div className="rounded-2xl border border-zinc-800 bg-black/30 p-4">

              <div className="mb-1 text-xs uppercase tracking-wider text-zinc-500">
                Exit MC
              </div>

              <div className="text-sm font-semibold text-white">
                ${exitMarketCap.toLocaleString()}
              </div>

            </div>
          )}

        </div>

        {/* Footer */}

        {traderHandle && (
          <div className="mt-6 text-sm text-zinc-500">
            @{traderHandle}
          </div>
        )}

        <div className="mt-6 border-t border-zinc-800 pt-4 text-xs text-zinc-600">
          Powered by Sentinel AI
        </div>

      </div>

    </div>
  );
}