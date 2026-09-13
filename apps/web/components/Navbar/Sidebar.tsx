"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Compass,
  Swords,
  Radio,
  WalletCards,
  Trophy,
  Users,
  BarChart3,
  Bell,
  Settings,
  Activity,
  ChevronRight,
} from "lucide-react";

interface SidebarItem {
  label: string;
  href: string;
  icon: React.ElementType;
}

const mainNavigation: SidebarItem[] = [
  {
    label: "Discover",
    href: "/discover",
    icon: Compass,
  },
  {
    label: "Arena",
    href: "/arena",
    icon: Swords,
  },
  {
    label: "Tracker",
    href: "/tracker",
    icon: Radio,
  },
  {
    label: "xStocks",
    href: "/xstocks",
    icon: BarChart3,
  },
  {
    label: "Portfolio",
    href: "/portfolio",
    icon: WalletCards,
  },
  {
    label: "Apex",
    href: "/apex",
    icon: Trophy,
  },
  {
    label: "Recruits",
    href: "/recruits",
    icon: Users,
  },
];

const secondaryNavigation: SidebarItem[] = [
  {
    label: "Analytics",
    href: "/analytics",
    icon: Activity,
  },
  {
    label: "Alerts",
    href: "/alerts",
    icon: Bell,
  },
  {
    label: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  const isActive = (href: string) => {
    if (href === "/") {
      return pathname === "/";
    }

    return pathname === href || pathname.startsWith(`${href}/`);
  };

  return (
    <aside className="fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-[#292929] bg-[#070707]">
      {/* Brand */}
      <div className="border-b border-[#292929] px-5 py-5">
        <Link
          href="/"
          className="group flex items-center gap-3"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-[#3A321C] bg-[#101010]">
            <span className="text-lg font-black text-[#D4AF37]">
              S
            </span>
          </div>

          <div className="min-w-0">
            <div className="truncate text-lg font-bold tracking-tight text-white">
              SentinelAI
            </div>

            <div className="text-[10px] font-medium uppercase tracking-[0.18em] text-[#8B8B8B]">
              Intelligence Terminal
            </div>
          </div>
        </Link>
      </div>

      {/* Main navigation */}
      <div className="flex-1 overflow-y-auto px-3 py-5">
        <div className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#666]">
          Terminal
        </div>

        <nav className="space-y-1">
          {mainNavigation.map((item) => {
            const active = isActive(item.href);
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={[
                  "group flex items-center justify-between rounded-lg px-3 py-2.5 transition-all",
                  active
                    ? "border border-[#4A3C17] bg-[#17130A] text-[#F5C84C]"
                    : "border border-transparent text-[#A1A1A1] hover:border-[#292929] hover:bg-[#101010] hover:text-white",
                ].join(" ")}
              >
                <div className="flex items-center gap-3">
                  <Icon
                    size={18}
                    strokeWidth={1.8}
                    className={
                      active
                        ? "text-[#F5C84C]"
                        : "text-[#777] group-hover:text-[#D4AF37]"
                    }
                  />

                  <span className="text-sm font-medium">
                    {item.label}
                  </span>
                </div>

                {active && (
                  <ChevronRight
                    size={15}
                    className="text-[#D4AF37]"
                  />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Intelligence */}
        <div className="mb-3 mt-8 px-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-[#666]">
          Intelligence
        </div>

        <nav className="space-y-1">
          {secondaryNavigation.map((item) => {
            const active = isActive(item.href);
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={[
                  "group flex items-center justify-between rounded-lg px-3 py-2.5 transition-all",
                  active
                    ? "border border-[#4A3C17] bg-[#17130A] text-[#F5C84C]"
                    : "border border-transparent text-[#A1A1A1] hover:border-[#292929] hover:bg-[#101010] hover:text-white",
                ].join(" ")}
              >
                <div className="flex items-center gap-3">
                  <Icon
                    size={18}
                    strokeWidth={1.8}
                    className={
                      active
                        ? "text-[#F5C84C]"
                        : "text-[#777] group-hover:text-[#D4AF37]"
                    }
                  />

                  <span className="text-sm font-medium">
                    {item.label}
                  </span>
                </div>

                {active && (
                  <ChevronRight
                    size={15}
                    className="text-[#D4AF37]"
                  />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Status */}
      <div className="border-t border-[#292929] p-4">
        <div className="rounded-lg border border-[#292929] bg-[#101010] p-3">
          <div className="mb-2 flex items-center gap-2">
            <span className="relative flex h-2.5 w-2.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-60" />
              <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-green-400" />
            </span>

            <span className="text-xs font-medium text-white">
              Sentinel Systems
            </span>
          </div>

          <div className="text-[11px] text-[#777]">
            All intelligence engines operational
          </div>
        </div>
      </div>
    </aside>
  );
}
