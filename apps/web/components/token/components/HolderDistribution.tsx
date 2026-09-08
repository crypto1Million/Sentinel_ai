"use client";

import type { ElementType } from "react";
import {
  PieChart,
  Users,
  Wallet,
  Fish,
  Brain,
  Shield,
  Flame,
  Coins,
  Building2,
  TrendingUp,
} from "lucide-react";

interface HolderDistributionProps {
  totalHolders: number;
  top10Percent: number;
  top25Percent: number;
  smartMoneyPercent: number;
  whalePercent: number;
  freshWalletPercent: number;
  insiderPercent: number;
  sniperPercent: number;
  deployerPercent: number;
  lpPercent: number;
  burnedPercent: number;
  exchangePercent: number;
  othersPercent: number;
}

interface HolderCardProps {
  title: string;
  value: number;
  icon: ElementType;
  color?: string;
}

function HolderCard({
  title,
  value,
  icon: Icon,
  color = "text-cyan-400",
}: HolderCardProps) {
  const safeValue = Number.isFinite(value) ? value : 0;

  return (
    <div className="rounded-xl border border-[#292929] bg-[#171717] p-4">
      <div className="mb-3 flex items-center gap-2">
        <Icon size={18} className={color} />

        <span className="text-sm text-[#8B8B8B]">
          {title}
        </span>
      </div>

      <div className="text-2xl font-semibold text-white">
        {safeValue.toFixed(2)}%
      </div>

      <div className="mt-3 h-2 overflow-hidden rounded-full bg-[#070707]">
        <div
          className="h-full rounded-full bg-[#D4AF37]"
          style={{
            width: `${Math.max(0, Math.min(safeValue, 100))}%`,
          }}
        />
      </div>
    </div>
  );
}

export default function HolderDistribution({
  totalHolders,
  top10Percent,
  top25Percent,
  smartMoneyPercent,
  whalePercent,
  freshWalletPercent,
  insiderPercent,
  sniperPercent,
  deployerPercent,
  lpPercent,
  burnedPercent,
  exchangePercent,
  othersPercent,
}: HolderDistributionProps) {
  return (
    <div className="space-y-8 rounded-xl border border-[#292929] bg-[#101010] p-6">
      {/* Header */}

      <div className="flex items-center gap-3">
        <PieChart
          className="text-[#D4AF37]"
          size={24}
        />

        <div>
          <h2 className="text-xl font-bold text-white">
            Holder Distribution
          </h2>

          <p className="text-sm text-[#8B8B8B]">
            Wallet ownership breakdown
          </p>
        </div>
      </div>

      {/* Total Holders */}

      <div className="rounded-xl border border-[#292929] bg-[#171717] p-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Users
              size={22}
              className="text-[#D4AF37]"
            />

            <span className="font-medium text-white">
              Total Holders
            </span>
          </div>

          <div className="text-3xl font-bold text-white">
            {totalHolders.toLocaleString()}
          </div>
        </div>
      </div>

      {/* Holder Concentration */}

      <div>
        <h3 className="mb-4 font-semibold text-white">
          Holder Concentration
        </h3>

        <div className="grid gap-4 md:grid-cols-2">
          <HolderCard
            title="Top 10 Holders"
            value={top10Percent}
            icon={Users}
          />

          <HolderCard
            title="Top 25 Holders"
            value={top25Percent}
            icon={Users}
          />
        </div>
      </div>

      {/* Wallet Intelligence */}

      <div>
        <h3 className="mb-4 font-semibold text-white">
          Wallet Intelligence
        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <HolderCard
            title="Smart Money"
            value={smartMoneyPercent}
            icon={Brain}
            color="text-green-400"
          />

          <HolderCard
            title="Whales"
            value={whalePercent}
            icon={Fish}
            color="text-blue-400"
          />

          <HolderCard
            title="Fresh Wallets"
            value={freshWalletPercent}
            icon={Wallet}
            color="text-yellow-400"
          />

          <HolderCard
            title="Insiders"
            value={insiderPercent}
            icon={Shield}
            color="text-red-400"
          />

          <HolderCard
            title="Snipers"
            value={sniperPercent}
            icon={TrendingUp}
            color="text-purple-400"
          />
        </div>
      </div>

      {/* Token Allocation */}

      <div>
        <h3 className="mb-4 font-semibold text-white">
          Token Allocation
        </h3>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <HolderCard
            title="Developer"
            value={deployerPercent}
            icon={Shield}
            color="text-orange-400"
          />

          <HolderCard
            title="Liquidity Pool"
            value={lpPercent}
            icon={Coins}
            color="text-[#D4AF37]"
          />

          <HolderCard
            title="Burned"
            value={burnedPercent}
            icon={Flame}
            color="text-red-500"
          />

          <HolderCard
            title="Exchange Wallets"
            value={exchangePercent}
            icon={Building2}
            color="text-indigo-400"
          />

          <HolderCard
            title="Others"
            value={othersPercent}
            icon={Users}
            color="text-zinc-300"
          />
        </div>
      </div>

      {/* AI Summary */}

      <div className="rounded-xl border border-[#8C6D1F] bg-[#171717] p-5">
        <div className="mb-3 flex items-center gap-2">
          <Brain
            className="text-[#D4AF37]"
            size={20}
          />

          <span className="font-semibold text-white">
            Sentinel AI Summary
          </span>
        </div>

        <ul className="space-y-2 text-sm text-zinc-300">
          <li>
            • Top 10 wallets own <strong>{top10Percent}%</strong>
          </li>

          <li>
            • Smart Money controls{" "}
            <strong>{smartMoneyPercent}%</strong>
          </li>

          <li>
            • Whale ownership is{" "}
            <strong>{whalePercent}%</strong>
          </li>

          <li>
            • Developer owns{" "}
            <strong>{deployerPercent}%</strong>
          </li>

          <li>
            • LP allocation is{" "}
            <strong>{lpPercent}%</strong>
          </li>
        </ul>
      </div>
    </div>
  );
}
