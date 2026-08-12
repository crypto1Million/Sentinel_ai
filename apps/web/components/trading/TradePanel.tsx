"use client";

import { useState } from "react";
import {
  ArrowUpCircle,
  ArrowDownCircle,
  Settings2,
  Zap,
  Wallet,
  ShieldCheck,
  RefreshCcw,
  TrendingUp,
  AlertTriangle,
} from "lucide-react";

interface TradePanelProps {
  tokenSymbol: string;
  tokenName: string;
  tokenPrice: number;
  walletBalance: number;
  tokenBalance: number;
  slippage: number;
  priorityFee: number;
  sentinelScore: number;
}

export default function TradePanel({
  tokenSymbol,
  tokenName,
  tokenPrice,
  walletBalance,
  tokenBalance,
  slippage,
  priorityFee,
  sentinelScore,
}: TradePanelProps) {
  const [mode, setMode] = useState<"BUY" | "SELL">("BUY");
  const [amount, setAmount] = useState("");

  const quickButtons =
    mode === "BUY"
      ? ["0.1", "0.25", "0.5", "1", "2", "MAX"]
      : ["25%", "50%", "75%", "100%"];

  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-6">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold">

            Trade Panel

          </h2>

          <p className="text-sm text-zinc-500">

            Jupiter + Jito Execution Engine

          </p>

        </div>

        <ShieldCheck className="text-cyan-400" size={28} />

      </div>

      {/* Buy Sell */}

      <div className="grid grid-cols-2 gap-3">

        <button
          onClick={() => setMode("BUY")}
          className={`rounded-xl p-4 font-semibold transition ${
            mode === "BUY"
              ? "bg-green-500 text-black"
              : "bg-[#1B2330]"
          }`}
        >
          <ArrowUpCircle className="mx-auto mb-2" />

          BUY

        </button>

        <button
          onClick={() => setMode("SELL")}
          className={`rounded-xl p-4 font-semibold transition ${
            mode === "SELL"
              ? "bg-red-500 text-black"
              : "bg-[#1B2330]"
          }`}
        >
          <ArrowDownCircle className="mx-auto mb-2" />

          SELL

        </button>

      </div>

      {/* Token */}

      <div className="rounded-xl bg-[#1B2330] p-4">

        <div className="flex justify-between">

          <span className="text-zinc-400">

            Token

          </span>

          <span className="font-semibold">

            {tokenName} ({tokenSymbol})

          </span>

        </div>

        <div className="mt-3 flex justify-between">

          <span className="text-zinc-400">

            Price

          </span>

          <span>

            ${tokenPrice}

          </span>

        </div>

      </div>

      {/* Amount */}

      <div>

        <label className="text-sm text-zinc-400">

          Amount

        </label>

        <input
          type="number"
          placeholder="0.00"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="mt-2 w-full rounded-xl border border-zinc-700 bg-[#1B2330] p-4 outline-none"
        />

      </div>

      {/* Quick Amount */}

      <div className="grid grid-cols-3 gap-3">

        {quickButtons.map((item) => (

          <button
            key={item}
            className="rounded-lg bg-[#1B2330] p-3 hover:bg-cyan-700 transition"
          >

            {item}

          </button>

        ))}

      </div>

      {/* Wallet */}

      <div className="rounded-xl bg-[#1B2330] p-4 space-y-3">

        <div className="flex justify-between">

          <span className="text-zinc-400">

            SOL Balance

          </span>

          <span>

            {walletBalance}

          </span>

        </div>

        <div className="flex justify-between">

          <span className="text-zinc-400">

            Token Balance

          </span>

          <span>

            {tokenBalance}

          </span>

        </div>

      </div>

      {/* Trade Settings */}

      <div className="rounded-xl bg-[#1B2330] p-4 space-y-4">

        <div className="flex items-center gap-2 font-semibold">

          <Settings2 size={18} />

          Trade Settings

        </div>

        <div className="flex justify-between">

          <span>

            Slippage

          </span>

          <span>

            {slippage}%

          </span>

        </div>

        <div className="flex justify-between">

          <span>

            Priority Fee

          </span>

          <span>

            {priorityFee} SOL

          </span>

        </div>

      </div>

      {/* Sentinel */}

      <div className="rounded-xl border border-cyan-800 bg-cyan-950/20 p-5">

        <div className="flex justify-between">

          <span>

            Sentinel Score

          </span>

          <span className="font-bold text-cyan-400">

            {sentinelScore}/100

          </span>

        </div>

        <div className="mt-4 h-2 rounded-full bg-zinc-800">

          <div
            className="h-full rounded-full bg-cyan-400"
            style={{
              width: `${sentinelScore}%`,
            }}
          />

        </div>

      </div>

      {/* Execute */}

      <button
        className={`w-full rounded-xl p-5 font-bold text-lg ${
          mode === "BUY"
            ? "bg-green-500 text-black hover:bg-green-400"
            : "bg-red-500 text-black hover:bg-red-400"
        } transition`}
      >
        {mode === "BUY" ? (
          <div className="flex justify-center gap-2">

            <Zap />

            Buy Token

          </div>
        ) : (
          <div className="flex justify-center gap-2">

            <RefreshCcw />

            Sell Token

          </div>
        )}
      </button>

      {/* Risk */}

      <div className="rounded-xl bg-[#1B2330] p-4">

        <div className="mb-3 flex items-center gap-2">

          <AlertTriangle
            className="text-yellow-400"
            size={18}
          />

          <span className="font-semibold">

            Trade Warning

          </span>

        </div>

        <p className="text-sm text-zinc-400">

          Sentinel recommends checking Wallet DNA,
          Rug Radar and Narrative Score before placing
          large trades.

        </p>

      </div>

      {/* Footer */}

      <div className="flex items-center justify-between text-sm text-zinc-500">

        <div className="flex items-center gap-2">

          <Wallet size={16} />

          Connected Wallet

        </div>

        <div className="flex items-center gap-2">

          <TrendingUp size={16} />

          Jupiter Ready

        </div>

      </div>

    </div>
  );
}

