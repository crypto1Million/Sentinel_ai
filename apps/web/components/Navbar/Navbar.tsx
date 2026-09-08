"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Search,
  ChevronDown,
  Bell,
  UserRound,
  Wallet,
} from "lucide-react";

const navigation = [
  {
    name: "Discover",
    href: "/discover",
  },
  {
    name: "Arena",
    href: "/arena",
  },
  {
    name: "Tracker",
    href: "/tracker",
  },
  {
    name: "xStocks",
    href: "/xstocks",
  },
  {
    name: "Portfolio",
    href: "/portfolio",
  },
  {
    name: "Apex",
    href: "/apex",
  },
  {
    name: "Recruits",
    href: "/recruits",
  },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 h-16 border-b border-[#292929] bg-[#070707]/95 backdrop-blur">
      <div className="flex h-full items-center px-4 lg:px-6">

        {/* =====================================================
            SENTINEL BRAND
            ===================================================== */}

        <Link
          href="/"
          aria-label="SentinelAI Home"
          className="mr-6 flex shrink-0 items-center gap-2.5"
        >
          <Image
            src="/brand/sentinel%20icon.png"
            alt="SentinelAI"
            width={34}
            height={34}
            priority
            className="h-[34px] w-[34px] object-contain"
          />

          <Image
            src="/brand/sentinel%20wordtext.png"
            alt="SentinelAI"
            width={112}
            height={30}
            priority
            className="h-[30px] w-auto object-contain"
          />
        </Link>

        {/* =====================================================
            PRIMARY NAVIGATION
            ===================================================== */}

        <nav className="hidden min-w-0 flex-1 items-center gap-1 xl:flex">
          {navigation.map((item) => {
            const isActive =
              pathname === item.href ||
              pathname.startsWith(`${item.href}/`);

            return (
              <Link
                key={item.href}
                href={item.href}
                className={[
                  "rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-[#D4AF37]/10 text-[#F5C84C]"
                    : "text-[#8B8B8B] hover:bg-[#171717] hover:text-white",
                ].join(" ")}
              >
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* =====================================================
            RIGHT SIDE
            ===================================================== */}

        <div className="ml-auto flex items-center gap-2">

          {/* Search */}

          <button
            type="button"
            aria-label="Search"
            className="
              hidden
              h-10
              w-10
              items-center
              justify-center
              rounded-lg
              border
              border-[#292929]
              bg-[#101010]
              text-[#8B8B8B]
              transition-colors
              hover:border-[#D4AF37]
              hover:text-[#F5C84C]
              sm:flex
            "
          >
            <Search size={18} />
          </button>

          {/* Chain Selector */}

          <button
            type="button"
            className="
              hidden
              items-center
              gap-2
              rounded-lg
              border
              border-[#292929]
              bg-[#101010]
              px-3
              py-2
              text-sm
              text-white
              transition-colors
              hover:border-[#D4AF37]
              sm:flex
            "
          >
            <span className="h-2 w-2 rounded-full bg-[#39E58C]" />

            <span>
              Solana
            </span>

            <ChevronDown size={14} className="text-[#8B8B8B]" />
          </button>

          {/* Wallet Balance */}

          <div
            className="
              hidden
              items-center
              gap-2
              rounded-lg
              border
              border-[#292929]
              bg-[#101010]
              px-3
              py-2
              md:flex
            "
          >
            <Wallet
              size={15}
              className="text-[#D4AF37]"
            />

            <div className="flex flex-col leading-none">
              <span className="text-[10px] uppercase tracking-wider text-[#8B8B8B]">
                Balance
              </span>

              <span className="mt-1 text-sm font-semibold text-white">
                0 SOL
              </span>
            </div>
          </div>

          {/* Notifications */}

          <button
            type="button"
            aria-label="Notifications"
            className="
              relative
              flex
              h-10
              w-10
              items-center
              justify-center
              rounded-lg
              border
              border-[#292929]
              bg-[#101010]
              text-[#8B8B8B]
              transition-colors
              hover:border-[#D4AF37]
              hover:text-[#F5C84C]
            "
          >
            <Bell size={18} />

            <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-[#F5C84C]" />
          </button>

          {/* Profile */}

          <button
            type="button"
            aria-label="Profile"
            className="
              flex
              h-10
              w-10
              items-center
              justify-center
              rounded-lg
              border
              border-[#292929]
              bg-[#101010]
              text-[#8B8B8B]
              transition-colors
              hover:border-[#D4AF37]
              hover:text-white
            "
          >
            <UserRound size={18} />
          </button>

        </div>
      </div>

      {/* =======================================================
          MOBILE NAVIGATION
          ======================================================= */}

      <div className="border-t border-[#292929] bg-[#070707] xl:hidden">
        <div className="flex gap-1 overflow-x-auto px-3 py-2">
          {navigation.map((item) => {
            const isActive =
              pathname === item.href ||
              pathname.startsWith(`${item.href}/`);

            return (
              <Link
                key={item.href}
                href={item.href}
                className={[
                  "shrink-0 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors",
                  isActive
                    ? "bg-[#D4AF37]/10 text-[#F5C84C]"
                    : "text-[#8B8B8B] hover:bg-[#171717] hover:text-white",
                ].join(" ")}
              >
                {item.name}
              </Link>
            );
          })}
        </div>
      </div>
    </header>
  );
}
