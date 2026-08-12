"use client";

import {
  Wallet,
  DollarSign,
  TrendingUp,
  TrendingDown,
  PieChart,
  Coins,
  Target,
  Activity,
  ShieldCheck,
  Brain,
  RefreshCw,
  ArrowUpRight,
} from "lucide-react";

export interface PortfolioHolding {
  id: string;

  symbol: string;

  name: string;

  quantity: number;

  averageEntry: number;

  currentPrice: number;

  currentValue: number;

  pnl: number;

  pnlPercent: number;

  sentinelScore: number;

  allocation: number;
}

interface PortfolioPanelProps {
  totalValue: number;

  dailyPnL: number;

  dailyPnLPercent: number;

  unrealizedPnL: number;

  realizedPnL: number;

  holdings: PortfolioHolding[];
}

export default function PortfolioPanel({
  totalValue,
  dailyPnL,
  dailyPnLPercent,
  unrealizedPnL,
  realizedPnL,
  holdings,
}: PortfolioPanelProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div className="flex items-center gap-3">

          <Wallet
            size={30}
            className="text-cyan-400"
          />

          <div>

            <h2 className="text-2xl font-bold">

              Portfolio

            </h2>

            <p className="text-sm text-zinc-500">

              Complete portfolio analytics

            </p>

          </div>

        </div>

        <RefreshCw
          className="text-cyan-400"
          size={24}
        />

      </div>

      {/* Summary */}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

        <SummaryCard
          title="Portfolio Value"
          value={`$${totalValue.toLocaleString()}`}
          icon={DollarSign}
          color="text-cyan-400"
        />

        <SummaryCard
          title="Daily PnL"
          value={`${dailyPnL >= 0 ? "+" : ""}$${dailyPnL.toFixed(2)}`}
          subtitle={`${dailyPnLPercent.toFixed(2)}%`}
          icon={dailyPnL >= 0 ? TrendingUp : TrendingDown}
          color={dailyPnL >= 0 ? "text-green-400" : "text-red-400"}
        />

        <SummaryCard
          title="Unrealized"
          value={`$${unrealizedPnL.toFixed(2)}`}
          icon={Activity}
          color="text-yellow-400"
        />

        <SummaryCard
          title="Realized"
          value={`$${realizedPnL.toFixed(2)}`}
          icon={Target}
          color="text-green-400"
        />

      </div>

      {/* Holdings */}

      <div>

        <h3 className="mb-5 text-xl font-semibold">

          Holdings

        </h3>

        <div className="overflow-x-auto rounded-xl border border-zinc-800">

          <table className="w-full">

            <thead className="bg-[#1B2330]">

              <tr>

                <th className="p-4 text-left">Token</th>

                <th className="p-4 text-left">Quantity</th>

                <th className="p-4 text-left">Entry</th>

                <th className="p-4 text-left">Current</th>

                <th className="p-4 text-left">Value</th>

                <th className="p-4 text-left">PnL</th>

                <th className="p-4 text-left">Allocation</th>

                <th className="p-4 text-left">Sentinel</th>

              </tr>

            </thead>

            <tbody>

              {holdings.map((holding) => (

                <tr
                  key={holding.id}
                  className="border-t border-zinc-800 hover:bg-[#1B2330]"
                >

                  <td className="p-4">

                    <div>

                      <div className="font-bold">

                        {holding.symbol}

                      </div>

                      <div className="text-sm text-zinc-500">

                        {holding.name}

                      </div>

                    </div>

                  </td>

                  <td className="p-4">

                    {holding.quantity}

                  </td>

                  <td className="p-4">

                    ${holding.averageEntry}

                  </td>

                  <td className="p-4">

                    ${holding.currentPrice}

                  </td>

                  <td className="p-4 font-semibold">

                    ${holding.currentValue.toLocaleString()}

                  </td>

                  <td
                    className={`p-4 font-semibold ${
                      holding.pnl >= 0
                        ? "text-green-400"
                        : "text-red-400"
                    }`}
                  >

                    {holding.pnl >= 0 ? "+" : ""}

                    ${holding.pnl.toFixed(2)}

                    <br />

                    <span className="text-xs">

                      {holding.pnlPercent.toFixed(2)}%

                    </span>

                  </td>

                  <td className="p-4">

                    {holding.allocation}%

                  </td>

                  <td className="p-4">

                    <div className="flex items-center gap-2">

                      <ShieldCheck
                        className="text-cyan-400"
                        size={16}
                      />

                      {holding.sentinelScore}

                    </div>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

      {/* Portfolio Intelligence */}

      <div className="grid gap-4 md:grid-cols-3">

        <InfoCard
          icon={PieChart}
          title="Diversification"
          value="Excellent"
        />

        <InfoCard
          icon={Brain}
          title="AI Portfolio Rating"
          value="92 / 100"
        />

        <InfoCard
          icon={Coins}
          title="Active Holdings"
          value={holdings.length.toString()}
        />

      </div>

      {/* AI */}

      <div className="rounded-xl border border-cyan-900 bg-cyan-950/20 p-5">

        <div className="mb-3 flex items-center gap-2">

          <Brain
            size={20}
            className="text-cyan-400"
          />

          <span className="font-semibold">

            Sentinel Portfolio Insight

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          Your portfolio maintains healthy diversification with strong exposure to
          high-scoring assets. Sentinel currently identifies low systemic risk,
          positive smart-money participation, and favorable liquidity conditions.

        </p>

      </div>

    </div>
  );
}

function SummaryCard({
  title,
  value,
  subtitle,
  icon: Icon,
  color,
}: any) {
  return (
    <div className="rounded-xl bg-[#1B2330] p-5">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          className={color}
          size={18}
        />

        <span className="text-sm text-zinc-500">

          {title}

        </span>

      </div>

      <div className={`text-2xl font-bold ${color}`}>

        {value}

      </div>

      {subtitle && (
        <div className="mt-1 text-sm text-zinc-400">

          {subtitle}

        </div>
      )}

    </div>
  );
}

function InfoCard({
  title,
  value,
  icon: Icon,
}: any) {
  return (
    <div className="rounded-xl bg-[#1B2330] p-5">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          className="text-cyan-400"
          size={18}
        />

        <span className="text-sm text-zinc-500">

          {title}

        </span>

      </div>

      <div className="text-xl font-bold">

        {value}

      </div>

    </div>
  );
}
