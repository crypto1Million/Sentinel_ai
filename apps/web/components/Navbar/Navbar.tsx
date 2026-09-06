"use client";

import Image from "next/image";
import Link from "next/link";

export default function Navbar() {
  return (
    <header className="h-16 border-b border-zinc-800 bg-[#0B0F14]">
      <div className="flex h-full items-center justify-between px-6">

        {/* SentinelAI Brand */}
        <Link
          href="/"
          className="flex items-center"
          aria-label="SentinelAI Home"
        >
          <Image
            src="/branding/sentinel-logo.svg"
            alt="SentinelAI"
            width={150}
            height={36}
            priority
          />
        </Link>

        {/* Right Side */}
        <div className="flex items-center gap-4">

          <div className="text-sm text-zinc-400">
            Solana
          </div>

          <button className="rounded-lg border border-zinc-800 bg-[#11161D] px-4 py-2 text-sm text-zinc-300 hover:bg-[#1B2330]">
            Connect Wallet
          </button>

        </div>

      </div>
    </header>
  );
}