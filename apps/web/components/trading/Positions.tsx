id="positions7x"
"use client";

import {
  ArrowUpRight,
  ArrowDownRight,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Target,
  ShieldCheck,
  XCircle,
  RefreshCw,
  Wallet,
  Activity,
} from "lucide-react";

export interface Position {
  id: string;

  symbol: string;

  name: string;

  side: "LONG" | "SHORT";

  quantity: number;

  avgEntry: number;

  currentPrice: number;

  invested: number;

  currentValue: number;

  unrealizedPnL: number;

  unrealizedPnLPercent: number;

  stopLoss?: number;

  takeProfit?: number;

  sentinelScore: number;
}

interface PositionsProps {
  positions: Position[];
}

export default function Positions({
  positions,
}: PositionsProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6">

      {/* Header */}

      <div className="mb-6 flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold">

            Open Positions

          </h2>

          <p className="text-sm text-zinc-500">

            Live portfolio monitoring

          </p>

        </div>

        <Wallet
          size={30}
          className="text-cyan-400"
        />

      </div>

      {/* Positions */}

      <div className="space-y-6">

        {positions.map((position) => {

          const pnlPositive =
            position.unrealizedPnL >= 0;

          return (

            <div
              key={position.id}
              className="rounded-xl border border-zinc-800 bg-[#1B2330] p-5"
            >

              {/* Top */}

              <div className="flex items-center justify-between">

                <div>

                  <div className="flex items-center gap-2">

                    <h3 className="text-xl font-bold">

                      {position.symbol}

                    </h3>

                    <span className="rounded bg-zinc-700 px-2 py-1 text-xs">

                      {position.side}

                    </span>

                  </div>

                  <p className="text-sm text-zinc-500">

                    {position.name}

                  </p>

                </div>

                <div
                  className={`text-right ${
                    pnlPositive
                      ? "text-green-400"
                      : "text-red-400"
                  }`}
                >

                  <div className="text-2xl font-bold">

                    {pnlPositive ? "+" : ""}$
                    {position.unrealizedPnL.toFixed(2)}

                  </div>

                  <div>

                    ({position.unrealizedPnLPercent.toFixed(2)}%)

                  </div>

                </div>

              </div>

              {/* Grid */}

              <div className="mt-6 grid gap-4 md:grid-cols-4">

                <Metric
                  icon={DollarSign}
                  title="Entry"
                  value={`$${position.avgEntry}`}
                />

                <Metric
                  icon={TrendingUp}
                  title="Current"
                  value={`$${position.currentPrice}`}
                />

                <Metric
                  icon={Activity}
                  title="Quantity"
                  value={position.quantity.toString()}
                />

                <Metric
                  icon={Wallet}
                  title="Value"
                  value={`$${position.currentValue.toFixed(2)}`}
                />

              </div>

              {/* Risk */}

              <div className="mt-6 grid gap-4 md:grid-cols-3">

                <Metric
                  icon={ArrowDownRight}
                  title="Stop Loss"
                  value={
                    position.stopLoss
                      ? `$${position.stopLoss}`
                      : "--"
                  }
                />

                <Metric
                  icon={ArrowUpRight}
                  title="Take Profit"
                  value={
                    position.takeProfit
                      ? `$${position.takeProfit}`
                      : "--"
                  }
                />

                <Metric
                  icon={ShieldCheck}
                  title="Sentinel Score"
                  value={`${position.sentinelScore}/100`}
                />

              </div>

              {/* Score */}

              <div className="mt-5">

                <div className="mb-2 flex justify-between text-sm">

                  <span>

                    Position Health

                  </span>

                  <span>

                    {position.sentinelScore}%

                  </span>

                </div>

                <div className="h-2 rounded-full bg-zinc-700">

                  <div
                    className="h-full rounded-full bg-cyan-400"
                    style={{
                      width: `${position.sentinelScore}%`,
                    }}
                  />

                </div>

              </div>

              {/* Actions */}

              <div className="mt-6 flex flex-wrap gap-3">

                <button className="rounded-lg bg-cyan-600 px-4 py-2 hover:bg-cyan-500">

                  Increase

                </button>

                <button className="rounded-lg bg-yellow-600 px-4 py-2 hover:bg-yellow-500">

                  Reduce

                </button>

                <button className="rounded-lg bg-blue-600 px-4 py-2 hover:bg-blue-500">

                  Edit SL/TP

                </button>

                <button className="rounded-lg bg-zinc-700 px-4 py-2 hover:bg-zinc-600">

                  Replay

                </button>

                <button className="rounded-lg bg-red-600 px-4 py-2 hover:bg-red-500">

                  Close Position

                </button>

              </div>

            </div>

          );

        })}

        {positions.length === 0 && (

          <div className="rounded-xl border border-dashed border-zinc-700 p-10 text-center">

            <XCircle
              size={50}
              className="mx-auto mb-3 text-zinc-600"
            />

            <h3 className="text-xl font-semibold">

              No Open Positions

            </h3>

            <p className="mt-2 text-zinc-500">

              Your active trades will appear here.

            </p>

          </div>

        )}

      </div>

      {/* Footer */}

      <div className="mt-8 flex items-center justify-between text-sm text-zinc-500">

        <div className="flex items-center gap-2">

          <RefreshCw size={16} />

          Auto Refresh

        </div>

        <div>

          Updates every block

        </div>

      </div>

    </div>
  );
}

interface MetricProps {
  icon: React.ElementType;

  title: string;

  value: string;
}

function Metric({
  icon: Icon,
  title,
  value,
}: MetricProps) {
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
