"use client";

import {
  AlertTriangle,
  ShieldAlert,
  Bell,
  BellRing,
  Brain,
  Activity,
  Wallet,
  TrendingUp,
  TrendingDown,
  Flame,
  Eye,
  Clock,
  CheckCircle2,
  XCircle,
  Info,
} from "lucide-react";

export interface AlertItem {
  id: string;

  type:
    | "RUG"
    | "WHALE"
    | "SMART_MONEY"
    | "MEV"
    | "JITO"
    | "LIQUIDITY"
    | "NARRATIVE"
    | "PRICE"
    | "SYSTEM";

  severity:
    | "LOW"
    | "MEDIUM"
    | "HIGH"
    | "CRITICAL";

  title: string;

  description: string;

  timestamp: string;

  acknowledged: boolean;
}

interface AlertsPanelProps {
  alerts: AlertItem[];
}

export default function AlertsPanel({
  alerts,
}: AlertsPanelProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6">

      {/* Header */}

      <div className="mb-8 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <BellRing
            size={28}
            className="text-cyan-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              Alerts Center

            </h2>

            <p className="text-sm text-zinc-500">

              Live Sentinel Intelligence

            </p>

          </div>

        </div>

        <div className="rounded-lg bg-cyan-500 px-4 py-2 font-bold text-black">

          {alerts.length} Alerts

        </div>

      </div>

      {/* Alerts */}

      <div className="space-y-5">

        {alerts.map((alert) => (

          <div
            key={alert.id}
            className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5 transition hover:border-cyan-600"
          >

            <div className="flex items-start justify-between">

              <div className="flex gap-4">

                <AlertIcon
                  type={alert.type}
                />

                <div>

                  <div className="flex items-center gap-3">

                    <h3 className="font-bold text-lg">

                      {alert.title}

                    </h3>

                    <SeverityBadge
                      severity={alert.severity}
                    />

                  </div>

                  <p className="mt-2 text-zinc-400">

                    {alert.description}

                  </p>

                  <div className="mt-4 flex items-center gap-2 text-sm text-zinc-500">

                    <Clock size={15} />

                    {alert.timestamp}

                  </div>

                </div>

              </div>

              <div>

                {alert.acknowledged ? (

                  <CheckCircle2
                    className="text-green-400"
                    size={24}
                  />

                ) : (

                  <Bell
                    className="text-yellow-400"
                    size={22}
                  />

                )}

              </div>

            </div>

          </div>

        ))}

        {alerts.length === 0 && (

          <div className="rounded-xl border border-dashed border-zinc-700 p-10 text-center">

            <CheckCircle2
              size={50}
              className="mx-auto mb-3 text-green-400"
            />

            <h3 className="text-xl font-semibold">

              No Active Alerts

            </h3>

            <p className="mt-2 text-zinc-500">

              Sentinel has not detected any risks or important events.

            </p>

          </div>

        )}

      </div>

    </div>
  );
}

function AlertIcon({
  type,
}: {
  type: AlertItem["type"];
}) {
  switch (type) {
    case "RUG":
      return (
        <ShieldAlert
          className="text-red-400"
          size={24}
        />
      );

    case "WHALE":
      return (
        <Wallet
          className="text-blue-400"
          size={24}
        />
      );

    case "SMART_MONEY":
      return (
        <Brain
          className="text-cyan-400"
          size={24}
        />
      );

    case "MEV":
      return (
        <Activity
          className="text-orange-400"
          size={24}
        />
      );

    case "JITO":
      return (
        <Flame
          className="text-purple-400"
          size={24}
        />
      );

    case "LIQUIDITY":
      return (
        <TrendingDown
          className="text-red-400"
          size={24}
        />
      );

    case "NARRATIVE":
      return (
        <TrendingUp
          className="text-green-400"
          size={24}
        />
      );

    case "PRICE":
      return (
        <Eye
          className="text-yellow-400"
          size={24}
        />
      );

    default:
      return (
        <Info
          className="text-zinc-400"
          size={24}
        />
      );
  }
}

function SeverityBadge({
  severity,
}: {
  severity: AlertItem["severity"];
}) {
  const styles = {
    LOW: "bg-green-600",
    MEDIUM: "bg-yellow-500 text-black",
    HIGH: "bg-orange-500",
    CRITICAL: "bg-red-600",
  };

  return (
    <span
      className={`rounded px-3 py-1 text-xs font-bold ${styles[severity]}`}
    >
      {severity}
    </span>
  );
}
