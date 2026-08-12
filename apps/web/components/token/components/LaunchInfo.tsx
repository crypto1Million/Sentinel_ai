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
  color = "text-cyan-400",
}: InfoCardProps) {
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
      ? (
          (liquidityGrowth / initialLiquidity) *
          100
        ).toFixed(1)
      : "0";

  return (
    <div className="rounded-xl border border-zinc-800 bg-[#11161d] p-5">

      <div className="mb-6 flex items-center gap-3">

        <Rocket
          className="text-cyan-400"
          size={24}
        />

        <div>

          <h2 className="text-lg font-semibold">
            Launch Information
          </h2>

          <p className="text-xs text-zinc-500">
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
          color="text-green-400"
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
          value={`${deployer.slice(0, 6)}...${deployer.slice(-6)}`}
          color="text-pink-400"
        />

      </div>

      <div className="mt-6 rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="mb-4 flex items-center gap-2">

          <Timer
            className="text-cyan-400"
            size={18}
          />

          <span className="font-semibold">
            Launch Statistics
          </span>

        </div>

        <div className="grid gap-4 md:grid-cols-3">

          <div>

            <div className="text-sm text-zinc-500">
              Initial Liquidity
            </div>

            <div className="mt-1 text-lg font-semibold">
              $
              {initialLiquidity.toLocaleString()}
            </div>

          </div>

          <div>

            <div className="text-sm text-zinc-500">
              Current Liquidity
            </div>

            <div className="mt-1 text-lg font-semibold">
              $
              {currentLiquidity.toLocaleString()}
            </div>

          </div>

          <div>

            <div className="text-sm text-zinc-500">
              Launch Price
            </div>

            <div className="mt-1 text-lg font-semibold">
              ${launchPrice}
            </div>

          </div>

        </div>

      </div>

      <div className="mt-6 rounded-xl border border-zinc-800 bg-[#1B2330] p-5">

        <div className="mb-2 flex items-center justify-between">

          <span className="text-sm text-zinc-400">
            Liquidity Growth
          </span>

          <span
            className={`font-semibold ${
              liquidityGrowth >= 0
                ? "text-green-400"
                : "text-red-400"
            }`}
          >
            {liquidityGrowth >= 0 ? "+" : ""}
            {liquidityGrowthPercent}%
          </span>

        </div>

        <div className="h-3 overflow-hidden rounded-full bg-zinc-800">

          <div
            className="h-full rounded-full bg-cyan-500"
            style={{
              width: `${Math.min(
                Number(liquidityGrowthPercent),
                100
              )}%`,
            }}
          />

        </div>

      </div>

    </div>
  );
}
```
