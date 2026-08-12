"use client";

import {
  DollarSign,
  TrendingUp,
  TrendingDown,
  Activity,
  Users,
  Wallet,
  Coins,
  BarChart3,
  PieChart,
  ArrowUpRight,
  ArrowDownRight,
  Shield,
  Fish,
  Brain,
  Flame,
  Zap,
  Clock3,
} from "lucide-react";

interface TokenMetricsProps {
  price: number;

  marketCap: number;

  fdv: number;

  liquidity: number;

  volume5m: number;
  volume1h: number;
  volume24h: number;

  buys: number;
  sells: number;

  buyVolume: number;
  sellVolume: number;

  holders: number;

  uniqueBuyers: number;
  uniqueSellers: number;

  smartMoneyPercent: number;

  freshWalletPercent: number;

  whalePercent: number;

  insiderPercent: number;

  sniperPercent: number;

  bundledPercent: number;

  top10Percent: number;

  top25Percent: number;

  devHolding: number;

  lpLockedPercent: number;

  lpBurnedPercent: number;

  ath: number;

  atl: number;

  change5m: number;

  change1h: number;

  change24h: number;
}

interface MetricCardProps {

  title: string;

  value: string;

  icon: React.ElementType;

  color?: string;

}

function MetricCard({

  title,

  value,

  icon: Icon,

  color = "text-cyan-400",

}: MetricCardProps) {

  return (

    <div className="rounded-xl border border-zinc-800 bg-[#1B2330] p-4">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          size={18}
          className={color}
        />

        <span className="text-sm text-zinc-400">

          {title}

        </span>

      </div>

      <div className="text-xl font-semibold">

        {value}

      </div>

    </div>

  );

}

export default function TokenMetrics({

  price,

  marketCap,

  fdv,

  liquidity,

  volume5m,

  volume1h,

  volume24h,

  buys,

  sells,

  buyVolume,

  sellVolume,

  holders,

  uniqueBuyers,

  uniqueSellers,

  smartMoneyPercent,

  freshWalletPercent,

  whalePercent,

  insiderPercent,

  sniperPercent,

  bundledPercent,

  top10Percent,

  top25Percent,

  devHolding,

  lpLockedPercent,

  lpBurnedPercent,

  ath,

  atl,

  change5m,

  change1h,

  change24h,

}: TokenMetricsProps) {

  return (

    <div className="rounded-xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      <div>

        <h2 className="text-xl font-bold">

          Token Metrics

        </h2>

        <p className="text-zinc-500 text-sm">

          Live on-chain statistics and market intelligence

        </p>

      </div>

      {/* Core */}

      <div>

        <h3 className="mb-4 font-semibold">

          Market Overview

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <MetricCard
            title="Price"
            value={`$${price}`}
            icon={DollarSign}
          />

          <MetricCard
            title="Market Cap"
            value={`$${marketCap.toLocaleString()}`}
            icon={BarChart3}
          />

          <MetricCard
            title="FDV"
            value={`$${fdv.toLocaleString()}`}
            icon={PieChart}
          />

          <MetricCard
            title="Liquidity"
            value={`$${liquidity.toLocaleString()}`}
            icon={Coins}
          />

        </div>

      </div>

      {/* Volume */}

      <div>

        <h3 className="mb-4 font-semibold">

          Volume

        </h3>

        <div className="grid gap-4 md:grid-cols-3">

          <MetricCard
            title="5m"
            value={`$${volume5m.toLocaleString()}`}
            icon={Clock3}
          />

          <MetricCard
            title="1H"
            value={`$${volume1h.toLocaleString()}`}
            icon={Activity}
          />

          <MetricCard
            title="24H"
            value={`$${volume24h.toLocaleString()}`}
            icon={TrendingUp}
          />

        </div>

      </div>

      {/* Trades */}

      <div>

        <h3 className="mb-4 font-semibold">

          Trading Activity

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <MetricCard
            title="Buys"
            value={buys.toLocaleString()}
            icon={ArrowUpRight}
            color="text-green-400"
          />

          <MetricCard
            title="Sells"
            value={sells.toLocaleString()}
            icon={ArrowDownRight}
            color="text-red-400"
          />

          <MetricCard
            title="Buy Volume"
            value={`$${buyVolume.toLocaleString()}`}
            icon={TrendingUp}
            color="text-green-400"
          />

          <MetricCard
            title="Sell Volume"
            value={`$${sellVolume.toLocaleString()}`}
            icon={TrendingDown}
            color="text-red-400"
          />

        </div>

      </div>

      {/* Holders */}

      <div>

        <h3 className="mb-4 font-semibold">

          Holder Statistics

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <MetricCard
            title="Holders"
            value={holders.toLocaleString()}
            icon={Users}
          />

          <MetricCard
            title="Unique Buyers"
            value={uniqueBuyers.toLocaleString()}
            icon={Wallet}
          />

          <MetricCard
            title="Unique Sellers"
            value={uniqueSellers.toLocaleString()}
            icon={Wallet}
          />

          <MetricCard
            title="Developer Holding"
            value={`${devHolding}%`}
            icon={Shield}
          />

        </div>

      </div>

      {/* Wallet Intelligence */}

      <div>

        <h3 className="mb-4 font-semibold">

          Wallet Intelligence

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

          <MetricCard
            title="Smart Money"
            value={`${smartMoneyPercent}%`}
            icon={Brain}
          />

          <MetricCard
            title="Fresh Wallets"
            value={`${freshWalletPercent}%`}
            icon={Users}
          />

          <MetricCard
            title="Whales"
            value={`${whalePercent}%`}
            icon={Fish}
          />

          <MetricCard
            title="Insiders"
            value={`${insiderPercent}%`}
            icon={Shield}
          />

          <MetricCard
            title="Snipers"
            value={`${sniperPercent}%`}
            icon={Zap}
          />

          <MetricCard
            title="Bundled"
            value={`${bundledPercent}%`}
            icon={Coins}
          />

          <MetricCard
            title="Top 10"
            value={`${top10Percent}%`}
            icon={Users}
          />

          <MetricCard
            title="Top 25"
            value={`${top25Percent}%`}
            icon={Users}
          />

        </div>

      </div>

      {/* Liquidity */}

      <div>

        <h3 className="mb-4 font-semibold">

          Liquidity Security

        </h3>

        <div className="grid gap-4 md:grid-cols-2">

          <MetricCard
            title="LP Locked"
            value={`${lpLockedPercent}%`}
            icon={Shield}
            color="text-green-400"
          />

          <MetricCard
            title="LP Burned"
            value={`${lpBurnedPercent}%`}
            icon={Flame}
            color="text-orange-400"
          />

        </div>

      </div>

      {/* Price */}

      <div>

        <h3 className="mb-4 font-semibold">

          Price Statistics

        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">

          <MetricCard
            title="ATH"
            value={`$${ath}`}
            icon={TrendingUp}
          />

          <MetricCard
            title="ATL"
            value={`$${atl}`}
            icon={TrendingDown}
          />

          <MetricCard
            title="5m"
            value={`${change5m}%`}
            icon={Activity}
          />

          <MetricCard
            title="1H"
            value={`${change1h}%`}
            icon={Activity}
          />

          <MetricCard
            title="24H"
            value={`${change24h}%`}
            icon={Activity}
          />

        </div>

      </div>

    </div>

  );

}
```
