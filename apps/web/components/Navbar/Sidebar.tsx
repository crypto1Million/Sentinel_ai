"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Compass,
  Dna,
  BarChart3,
  BriefcaseBusiness,
  Settings,
  Activity,
  ShieldCheck,
  Brain,
} from "lucide-react";

const navigation = [
  {
    name: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Discover",
    href: "/discover",
    icon: Compass,
  },
  {
    name: "Wallet DNA",
    href: "/wallets",
    icon: Dna,
  },
  {
    name: "Narratives",
    href: "/narratives",
    icon: Brain,
  },
  {
    name: "Portfolio",
    href: "/portfolio",
    icon: BriefcaseBusiness,
  },
  {
    name: "Activity",
    href: "/activity",
    icon: Activity,
  },
  {
    name: "Security",
    href: "/security",
    icon: ShieldCheck,
  },
  {
    name: "Analytics",
    href: "/analytics",
    icon: BarChart3,
  },
  {
    name: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-full w-64 flex-col border-r border-[#292929] bg-[#101010]">
      {/* Sidebar Header */}
      <div className="border-b border-[#292929] px-5 py-5">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#8C6D1F] bg-[#171717]">
            <ShieldCheck
              size={20}
              className="text-[#D4AF37]"
            />
          </div>

          <div>
            <div className="text-sm font-semibold text-white">
              SentinelAI
            </div>

            <div className="text-[11px] text-[#8B8B8B]">
              Intelligence Terminal
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const Icon = item.icon;

          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname === item.href ||
                pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.name}
              href={item.href}
              className={[
                "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-all",
                isActive
                  ? "border border-[#8C6D1F] bg-[#171717] text-[#F5C84C]"
                  : "border border-transparent text-[#8B8B8B] hover:border-[#292929] hover:bg-[#171717] hover:text-white",
              ].join(" ")}
            >
              <Icon
                size={18}
                className={
                  isActive
                    ? "text-[#F5C84C]"
                    : "text-[#8B8B8B] group-hover:text-white"
                }
              />

              <span>{item.name}</span>

              {isActive && (
                <span className="ml-auto h-1.5 w-1.5 rounded-full bg-[#F5C84C]" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Bottom Status */}
      <div className="border-t border-[#292929] p-3">
        <div className="rounded-lg border border-[#292929] bg-[#171717] px-3 py-3">
          <div className="mb-2 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-[#39E58C]" />

            <span className="text-xs font-medium text-[#39E58C]">
              Sentinel Online
            </span>
          </div>

          <div className="text-[11px] text-[#8B8B8B]">
            Real-time intelligence active
          </div>
        </div>
      </div>
    </aside>
  );
}
