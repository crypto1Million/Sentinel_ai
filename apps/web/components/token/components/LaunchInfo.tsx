"use client";

import {
  Rocket,
  CalendarDays,
  Clock3,
  Coins,
  User,
  Globe,
  Timer,
} from "lucide-react";

interface LaunchInfoProps {
  launchDate: string;
  tokenAge: string;
  blockchain: string;
  dex: string;
  pair: string;
  deployer: string;
  initialLiquidity: number;
  currentLiquidity: number;
  launchPrice: number;
}

interface InfoCardProps {
  icon: React.ElementType;
  title: string;
  value: string;
  color?: string;
}

function InfoCard({
  icon: Icon,
  title,
  value,
  color = "text-[#D4AF37]",
}: InfoCardProps) {
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

      <div className="font-semibold text-white">
        {value}
      </div>
    </div>
  );
}

export default function LaunchInfo({
  launchDate,
  tokenAge,
  blockchain,
  dex,
  pair,
  deployer,
  initialLiquidity,
  currentLiquidity,
  launchPrice,
}: LaunchInfoProps) {
  const liquidityGrowth =
    currentLiquidity - initialLiquidity;

  const liquidityGrowthPercent =
    initialLiquidity > 0
      ? (liquidityGrowth / initialLiquidity) * 100
      : 0;

  const shortDeployer =
    deployer.length > 12
      ? `${deployer.slice(0, 6)}...${deployer.slice(-6)}`
      : deployer;

  return (
    <div className="rounded-xl border border-[#292929] bg-[#101010] p-5">
      <div className="mb-6 flex items-center gap-3">
        <Rocket
          className="text-[#D4AF37]"
          size={24}
        />

        <div>
          <h2 className="text-lg font-semibold text-white">
            Launch Information
          </h2>

          <p className="text-xs text-[#8B8B8B]">
            Token deployment overview
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <InfoCard
          icon={CalendarDays}
          title="Launch Date"
          value={launchDate}
        />

        <InfoCard
          icon={Clock3}
          title="Token Age"
          value={tokenAge}
          color="text-yellow-400"
        />

        <InfoCard
          icon={Globe}
          title="Blockchain"
          value={blockchain}
          color="text-blue-400"
        />

        <InfoCard
          icon={Coins}
          title="DEX"
          value={dex}
          color="text-purple-400"
        />

        <InfoCard
          icon={Coins}
          title="Trading Pair"
          value={pair}
          color="text-orange-400"
        />

        <InfoCard
          icon={User}
          title="Deployer"
          value={shortDeployer}
          color="text-[#F5C84C]"
        />
      </div>

      <div className="mt-6 rounded-xl border border-[#292929] bg-[#171717] p-5">
        <div className="mb-4 flex items-center gap-2">
          <Timer
            className="text-[#D4AF37]"
            size={18}
          />

          <span className="font-semibold text-white">
            Launch Statistics
          </span>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Stat
            label="Initial Liquidity"
            value={`$${initialLiquidity.toLocaleString()}`}
          />

          <Stat
            label="Current Liquidity"
            value={`$${currentLiquidity.toLocaleString()}`}
          />

          <Stat
            label="Launch Price"
            value={`$${launchPrice}`}
          />
        </div>
      </div>

      <div className="mt-6 rounded-xl border border-[#292929] bg-[#171717] p-5">
        <div className="mb-2 flex items-center justify-between">
          <span className="text-sm text-[#8B8B8B]">
            Liquidity Growth
          </span>

          <span
            className={
              liquidityGrowth >= 0
                ? "font-semibold text-green-400"
                : "font-semibold text-red-400"
            }
          >
            {liquidityGrowth >= 0 ? "+" : ""}
            {liquidityGrowthPercent.toFixed(1)}%
          </span>
        </div>

        <div className="h-3 overflow-hidden rounded-full bg-[#070707]">
          <div
            className={
              liquidityGrowth >= 0
                ? "h-full rounded-full bg-[#D4AF37]"
                : "h-full rounded-full bg-red-500"
            }
            style={{
              width: `${Math.min(
                Math.abs(liquidityGrowthPercent),
                100
              )}%`,
            }}
          />
        </div>
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>
      <div className="text-sm text-[#8B8B8B]">
        {label}
      </div>

      <div className="mt-1 text-lg font-semibold text-white">
        {value}
      </div>
    </div>
  );
}
