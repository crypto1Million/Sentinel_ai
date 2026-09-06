"use client";

import Image from "next/image";
import Link from "next/link";

import {
  LayoutDashboard,
  Search,
  Wallet,
  BarChart3,
  ShieldCheck,
  Brain,
  Settings,
} from "lucide-react";

const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Discover",
    href: "/discover",
    icon: Search,
  },
  {
    name: "Portfolio",
    href: "/portfolio",
    icon: Wallet,
  },
  {
    name: "Markets",
    href: "/markets",
    icon: BarChart3,
  },
  {
    name: "Rug Radar",
    href: "/rug-radar",
    icon: ShieldCheck,
  },
  {
    name: "AI Intelligence",
    href: "/intelligence",
    icon: Brain,
  },
  {
    name: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="flex h-screen w-64 flex-col border-r border-zinc-800 bg-[#0B0F14]">

      {/* Logo */}
      <div className="flex h-16 items-center border-b border-zinc-800 px-5">
        <Link href="/">
          <Image
            src="/branding/sentinel-logo.svg"
            alt="SentinelAI"
            width={145}
            height={34}
            priority
          />
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 p-4">

        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className="
                flex items-center gap-3
                rounded-lg
                px-3 py-2.5
                text-sm text-zinc-400
                transition
                hover:bg-[#151B23]
                hover:text-white
              "
            >
              <Icon size={18} />

              <span>
                {item.name}
              </span>
            </Link>
          );
        })}

      </nav>

      {/* Bottom Status */}
      <div className="border-t border-zinc-800 p-4">
        <div className="flex items-center gap-2 text-xs text-green-400">
          <span className="h-2 w-2 rounded-full bg-green-400" />
          SentinelAI Online
        </div>
      </div>

    </aside>
  );
}