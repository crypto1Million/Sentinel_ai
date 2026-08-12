"use client";

import {
  Bell,
  Search,
  Settings,
  Wallet,
  User
} from "lucide-react";

export default function Header() {
  return (
    <header className="h-16 border-b border-zinc-800 bg-[#11161d]">

      <div className="flex h-full items-center justify-between px-6">

        <div className="flex items-center gap-6">

          <h1 className="text-2xl font-bold text-cyan-400">

            Sentinel AI

          </h1>

          <div className="relative">

            <Search
              className="absolute left-3 top-3"
              size={18}
            />

            <input
              placeholder="Search Token / Wallet / Deployer..."
              className="
                w-96
                rounded-lg
                bg-[#1b2330]
                py-2
                pl-10
                pr-4
                outline-none
              "
            />

          </div>

        </div>

        <div className="flex items-center gap-5">

          <Wallet size={22} />

          <Bell size={22} />

          <Settings size={22} />

          <User size={22} />

        </div>

      </div>

    </header>
  );
}