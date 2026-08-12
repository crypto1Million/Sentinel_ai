"use client";

import {
  Brain,
  Fish,
  Wallet,
  ShieldAlert,
  Zap,
  Flame,
  Activity,
  DollarSign,
  Users,
  Network,
  TrendingUp,
  Circle,
} from "lucide-react";

const legendItems = [

  {
    label: "Sentinel AI",
    icon: Brain,
    color: "text-cyan-400",
  },

  {
    label: "Whale Wallet",
    icon: Fish,
    color: "text-green-400",
  },

  {
    label: "Wallet DNA",
    icon: Wallet,
    color: "text-yellow-400",
  },

  {
    label: "Rug Radar",
    icon: ShieldAlert,
    color: "text-red-500",
  },

  {
    label: "Jito Bundle",
    icon: Zap,
    color: "text-purple-400",
  },

  {
    label: "Narrative",
    icon: Flame,
    color: "text-orange-400",
  },

  {
    label: "Smart Money",
    icon: Activity,
    color: "text-pink-400",
  },

  {
    label: "Liquidity",
    icon: DollarSign,
    color: "text-blue-400",
  },

  {
    label: "Holder Activity",
    icon: Users,
    color: "text-lime-400",
  },

  {
    label: "Wallet Cluster",
    icon: Network,
    color: "text-indigo-400",
  },

  {
    label: "Capital Flow",
    icon: TrendingUp,
    color: "text-emerald-400",
  },

];

export default function ChartLegend() {

  return (

    <div className="border-t border-zinc-800 bg-[#11161d] px-4 py-3">

      <div className="mb-3 text-sm font-semibold text-zinc-300">

        Chart Legend

      </div>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4 xl:grid-cols-6">

        {

          legendItems.map((item) => {

            const Icon = item.icon;

            return (

              <div

                key={item.label}

                className="flex items-center gap-2 rounded-lg bg-[#1B2330] px-3 py-2"

              >

                <Circle
                  size={8}
                  className={item.color}
                  fill="currentColor"
                />

                <Icon
                  size={15}
                  className={item.color}
                />

                <span className="text-xs">

                  {item.label}

                </span>

              </div>

            );

          })

        }

      </div>

    </div>

  );

}