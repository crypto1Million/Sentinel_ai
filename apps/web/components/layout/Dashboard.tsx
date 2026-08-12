"use client";

import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";

interface DashboardProps {
  children: React.ReactNode;
}

export default function Dashboard({
  children,
}: DashboardProps) {
  return (
    <div className="flex h-screen bg-[#0b0f14] text-white overflow-hidden">

      <Sidebar />

      <div className="flex flex-col flex-1">

        <Header />

        <main className="flex-1 overflow-auto p-4">

          {children}

        </main>

        <Footer />

      </div>

    </div>
  );
}