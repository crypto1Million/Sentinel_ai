"use client";

import {
  Activity,
  Brain,
  Wallet,
  Fish,
  TrendingUp,
  TrendingDown,
  Repeat,
  ShieldAlert,
  Flame,
  Network,
  PlayCircle,
  Radio,
  Award,
  Target,
  DollarSign,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react";

export interface WalletActivityEvent {
  id: string;

  wallet: string;

  label: string;

  avatar?: string;

  type:
    | "WHALE_BUY"
    | "WHALE_SELL"
    | "SMART_BUY"
    | "SMART_SELL"
    | "DNA_UPDATE"
    | "FUNDING"
    | "JITO"
    | "MEV"
    | "COPY"
    | "ROI"
    | "RANK"
    | "CONVICTION"
    | "INSIDER"
    | "DEPLOYER";

  token: string;

  amount: number;

  pnl: number;

  roi: number;

  conviction: number;

  timestamp: string;

  description: string;
}

interface WalletActivityProps {
  activities: WalletActivityEvent[];

  websocketConnected: boolean;
}

export default function WalletActivity({
  activities,
  websocketConnected,
}: WalletActivityProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6">

      {/* Header */}

      <div className="mb-8 flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold">

            Wallet Activity

          </h2>

          <p className="text-sm text-zinc-500">

            Live Wallet DNA Intelligence Feed

          </p>

        </div>

        <div className="flex items-center gap-3">

          <div
            className={`flex items-center gap-2 rounded-lg px-3 py-2 ${
              websocketConnected
                ? "bg-green-500/20 text-green-400"
                : "bg-red-500/20 text-red-400"
            }`}
          >
            <Radio size={16} />

            {websocketConnected
              ? "LIVE"
              : "OFFLINE"}
          </div>

        </div>

      </div>

      {/* Feed */}

      <div className="space-y-5">

        {activities.map((activity) => (

          <div
            key={activity.id}
            className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5 hover:border-cyan-500 transition"
          >

            <div className="flex justify-between">

              <div className="flex gap-4">

                <EventIcon
                  type={activity.type}
                />

                <div>

                  <div className="flex items-center gap-3">

                    <span className="font-bold">

                      {activity.label}

                    </span>

                    <TypeBadge
                      type={activity.type}
                    />

                  </div>

                  <div className="mt-2 text-zinc-400">

                    {activity.description}

                  </div>

                  <div className="mt-4 grid gap-3 md:grid-cols-4">

                    <MiniMetric
                      label="Token"
                      value={activity.token}
                    />

                    <MiniMetric
                      label="Amount"
                      value={`$${activity.amount.toLocaleString()}`}
                    />

                    <MiniMetric
                      label="ROI"
                      value={`${activity.roi}%`}
                    />

                    <MiniMetric
                      label="Conviction"
                      value={`${activity.conviction}/100`}
                    />

                  </div>

                </div>

              </div>

              <div className="text-right">

                <div
                  className={`text-xl font-bold ${
                    activity.pnl >= 0
                      ? "text-green-400"
                      : "text-red-400"
                  }`}
                >

                  {activity.pnl >= 0 ? "+" : ""}

                  {activity.pnl}%

                </div>

                <div className="mt-3 text-sm text-zinc-500">

                  {activity.timestamp}

                </div>

                <button className="mt-5 rounded-lg bg-cyan-600 px-4 py-2 hover:bg-cyan-500">

                  <PlayCircle
                    className="mr-2 inline"
                    size={16}
                  />

                  Replay

                </button>

              </div>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

function MiniMetric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-lg bg-[#11161d] p-3">

      <div className="text-xs text-zinc-500">

        {label}

      </div>

      <div className="mt-1 font-semibold">

        {value}

      </div>

    </div>
  );
}

function EventIcon({
  type,
}: {
  type: WalletActivityEvent["type"];
}) {
  switch (type) {
    case "WHALE_BUY":
      return (
        <Fish className="text-green-400" />
      );

    case "WHALE_SELL":
      return (
        <Fish className="text-red-400" />
      );

    case "SMART_BUY":
      return (
        <Brain className="text-cyan-400" />
      );

    case "SMART_SELL":
      return (
        <Brain className="text-orange-400" />
      );

    case "DNA_UPDATE":
      return (
        <Activity className="text-purple-400" />
      );

    case "FUNDING":
      return (
        <DollarSign className="text-blue-400" />
      );

    case "JITO":
      return (
        <Flame className="text-orange-400" />
      );

    case "MEV":
      return (
        <Network className="text-yellow-400" />
      );

    case "COPY":
      return (
        <Repeat className="text-cyan-400" />
      );

    case "ROI":
      return (
        <TrendingUp className="text-green-400" />
      );

    case "RANK":
      return (
        <Award className="text-yellow-400" />
      );

    case "CONVICTION":
      return (
        <Target className="text-pink-400" />
      );

    case "INSIDER":
      return (
        <ShieldAlert className="text-red-400" />
      );

    case "DEPLOYER":
      return (
        <Wallet className="text-purple-400" />
      );

    default:
      return <Activity />;
  }
}

function TypeBadge({
  type,
}: {
  type: WalletActivityEvent["type"];
}) {
  return (
    <span className="rounded bg-cyan-700 px-2 py-1 text-xs font-semibold">

      {type.replaceAll("_", " ")}

    </span>
  );
}
