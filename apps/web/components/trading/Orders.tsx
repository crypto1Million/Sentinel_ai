"use client";

import {
  Clock,
  CheckCircle2,
  XCircle,
  Loader2,
  DollarSign,
  TrendingUp,
  TrendingDown,
  Trash2,
  Eye,
  RefreshCw,
  ShieldCheck,
  Zap,
} from "lucide-react";

export interface Order {
  id: string;

  symbol: string;

  type: "MARKET" | "LIMIT" | "STOP" | "DCA";

  side: "BUY" | "SELL";

  status: "PENDING" | "FILLED" | "PARTIAL" | "CANCELLED";

  amount: number;

  filledAmount: number;

  price: number;

  currentPrice: number;

  createdAt: string;

  sentinelScore: number;
}

interface OrdersProps {
  orders: Order[];
}

export default function Orders({
  orders,
}: OrdersProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6">

      {/* Header */}

      <div className="mb-6 flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold">

            Orders

          </h2>

          <p className="text-sm text-zinc-500">

            Active & Historical Orders

          </p>

        </div>

        <RefreshCw
          className="text-cyan-400"
          size={24}
        />

      </div>

      {/* Orders */}

      <div className="space-y-5">

        {orders.map((order) => (

          <div
            key={order.id}
            className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5"
          >

            {/* Top */}

            <div className="flex items-center justify-between">

              <div>

                <div className="flex items-center gap-2">

                  <span className="text-xl font-bold">

                    {order.symbol}

                  </span>

                  <Badge
                    label={order.side}
                    color={
                      order.side === "BUY"
                        ? "green"
                        : "red"
                    }
                  />

                  <Badge
                    label={order.type}
                    color="cyan"
                  />

                </div>

                <p className="mt-1 text-sm text-zinc-500">

                  Created: {order.createdAt}

                </p>

              </div>

              <StatusBadge
                status={order.status}
              />

            </div>

            {/* Metrics */}

            <div className="mt-6 grid gap-4 md:grid-cols-4">

              <Metric
                icon={DollarSign}
                title="Order Price"
                value={`$${order.price}`}
              />

              <Metric
                icon={TrendingUp}
                title="Current Price"
                value={`$${order.currentPrice}`}
              />

              <Metric
                icon={Zap}
                title="Amount"
                value={`${order.amount}`}
              />

              <Metric
                icon={ShieldCheck}
                title="Sentinel Score"
                value={`${order.sentinelScore}/100`}
              />

            </div>

            {/* Fill */}

            <div className="mt-6">

              <div className="mb-2 flex justify-between text-sm">

                <span>

                  Filled

                </span>

                <span>

                  {(
                    (order.filledAmount /
                      order.amount) *
                    100
                  ).toFixed(1)}
                  %

                </span>

              </div>

              <div className="h-2 rounded-full bg-zinc-700">

                <div
                  className="h-full rounded-full bg-cyan-400"
                  style={{
                    width: `${
                      (order.filledAmount /
                        order.amount) *
                      100
                    }%`,
                  }}
                />

              </div>

            </div>

            {/* Actions */}

            <div className="mt-6 flex flex-wrap gap-3">

              <button className="rounded-lg bg-cyan-600 px-4 py-2 hover:bg-cyan-500">

                <Eye
                  className="inline mr-2"
                  size={16}
                />

                Details

              </button>

              <button className="rounded-lg bg-yellow-600 px-4 py-2 hover:bg-yellow-500">

                Edit

              </button>

              <button className="rounded-lg bg-red-600 px-4 py-2 hover:bg-red-500">

                <Trash2
                  className="inline mr-2"
                  size={16}
                />

                Cancel

              </button>

            </div>

          </div>

        ))}

        {orders.length === 0 && (

          <div className="rounded-xl border border-dashed border-zinc-700 p-10 text-center">

            <Clock
              size={48}
              className="mx-auto mb-3 text-zinc-600"
            />

            <h3 className="text-xl font-semibold">

              No Orders

            </h3>

            <p className="mt-2 text-zinc-500">

              Your pending and historical orders will appear here.

            </p>

          </div>

        )}

      </div>

    </div>
  );
}

function Metric({
  title,
  value,
  icon: Icon,
}: {
  title: string;
  value: string;
  icon: React.ElementType;
}) {
  return (
    <div className="rounded-lg bg-[#11161d] p-4">

      <div className="mb-2 flex items-center gap-2">

        <Icon
          size={16}
          className="text-cyan-400"
        />

        <span className="text-sm text-zinc-500">

          {title}

        </span>

      </div>

      <div className="font-semibold">

        {value}

      </div>

    </div>
  );
}

function Badge({
  label,
  color,
}: {
  label: string;
  color: "green" | "red" | "cyan";
}) {
  const colors = {
    green: "bg-green-600",
    red: "bg-red-600",
    cyan: "bg-cyan-600",
  };

  return (
    <span
      className={`${colors[color]} rounded px-2 py-1 text-xs font-semibold`}
    >
      {label}
    </span>
  );
}

function StatusBadge({
  status,
}: {
  status: Order["status"];
}) {
  switch (status) {
    case "FILLED":
      return (
        <div className="flex items-center gap-2 text-green-400">

          <CheckCircle2 size={18} />

          Filled

        </div>
      );

    case "PENDING":
      return (
        <div className="flex items-center gap-2 text-yellow-400">

          <Loader2
            size={18}
            className="animate-spin"
          />

          Pending

        </div>
      );

    case "PARTIAL":
      return (
        <div className="flex items-center gap-2 text-cyan-400">

          <Clock size={18} />

          Partial

        </div>
      );

    case "CANCELLED":
      return (
        <div className="flex items-center gap-2 text-red-400">

          <XCircle size={18} />

          Cancelled

        </div>
      );

    default:
      return null;
  }
}
