"use client";

import type { ElementType } from "react";

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
  icon: ElementType;
  color?: string;
}

function MetricCard({
  title,
  value,
  icon: Icon,
  color = "text-[#D4AF37]",
}: MetricCardProps) {
  return (
    <div className="rounded-xl border border-[#292929] bg-[#171717] p-4">
      <div className="mb-3 flex items-center gap-2">
        <Icon
          size={18}
          className={color}
        />

        <span className="text-sm text-[#8B8B8B]">
          {title}
        </span>
      </div>

      <div className="text-xl font-semibold text-white">
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
    <div className="space-y-8 rounded-xl border border-[#292929] bg-[#101010] p-6">
      <div>
        <h2 className="text-xl font-bold text-white">
          Token Metrics
        </h2>

        <p className="text-sm text-[#8B8B8B]">
          Live on-chain statistics and market intelligence
        </p>
      </div>

      <MetricsSection title="Market Overview">
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
      </MetricsSection>

      <MetricsSection
        title="Volume"
        columns="md:grid-cols-3"
      >
        <MetricCard
          title="5m Volume"
          value={`$${volume5m.toLocaleString()}`}
          icon={Clock3}
        />

        <MetricCard
          title="1H Volume"
          value={`$${volume1h.toLocaleString()}`}
          icon={Activity}
        />

        <MetricCard
          title="24H Volume"
          value={`$${volume24h.toLocaleString()}`}
          icon={TrendingUp}
        />
      </MetricsSection>

      <MetricsSection title="Trading Activity">
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
      </MetricsSection>

      <MetricsSection title="Holder Statistics">
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
      </MetricsSection>

      <MetricsSection title="Wallet Intelligence">
        <MetricCard
          title="Smart Money"
          value={`${smartMoneyPercent}%`}
          icon={Brain}
          color="text-green-400"
        />

        <MetricCard
          title="Fresh Wallets"
          value={`${freshWalletPercent}%`}
          icon={Users}
          color="text-yellow-400"
        />

        <MetricCard
          title="Whales"
          value={`${whalePercent}%`}
          icon={Fish}
          color="text-blue-400"
        />

        <MetricCard
          title="Insiders"
          value={`${insiderPercent}%`}
          icon={Shield}
          color="text-red-400"
        />

        <MetricCard
          title="Snipers"
          value={`${sniperPercent}%`}
          icon={Zap}
          color="text-purple-400"
        />

        <MetricCard
          title="Bundled"
          value={`${bundledPercent}%`}
          icon={Coins}
          color="text-orange-400"
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
      </MetricsSection>

      <MetricsSection
        title="Liquidity Security"
        columns="md:grid-cols-2"
      >
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
      </MetricsSection>

      <MetricsSection
        title="Price Statistics"
        columns="md:grid-cols-2 xl:grid-cols-5"
      >
        <MetricCard
          title="ATH"
          value={`$${ath}`}
          icon={TrendingUp}
          color="text-green-400"
        />

        <MetricCard
          title="ATL"
          value={`$${atl}`}
          icon={TrendingDown}
          color="text-red-400"
        />

        <MetricCard
          title="5m Change"
          value={`${change5m}%`}
          icon={Activity}
          color={
            change5m >= 0
              ? "text-green-400"
              : "text-red-400"
          }
        />

        <MetricCard
          title="1H Change"
          value={`${change1h}%`}
          icon={Activity}
          color={
            change1h >= 0
              ? "text-green-400"
              : "text-red-400"
          }
        />

        <MetricCard
          title="24H Change"
          value={`${change24h}%`}
          icon={Activity}
          color={
            change24h >= 0
              ? "text-green-400"
              : "text-red-400"
          }
        />
      </MetricsSection>
    </div>
  );
}

function MetricsSection({
  title,
  children,
  columns = "md:grid-cols-2 xl:grid-cols-4",
}: {
  title: string;
  children: React.ReactNode;
  columns?: string;
}) {
  return (
    <div>
      <h3 className="mb-4 font-semibold text-white">
        {title}
      </h3>

      <div className={`grid gap-4 ${columns}`}>
        {children}
      </div>
    </div>
  );
}