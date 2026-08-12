"use client";

import Link from "next/link";

import {

    LayoutDashboard,

    Search,

    TrendingUp,

    Wallet,

    Brain,

    Shield,

    Radar,

    Activity,

    History,

    Bell,

    PieChart,

    Settings

} from "lucide-react";

const items = [

    {
        icon: LayoutDashboard,
        label: "Dashboard",
        href: "/"
    },

    {
        icon: Search,
        label: "Discover",
        href: "/discover"
    },

    {
        icon: TrendingUp,
        label: "Trading",
        href: "/trading"
    },

    {
        icon: Wallet,
        label: "Wallets",
        href: "/wallets"
    },

    {
        icon: Brain,
        label: "AI"
    },

    {
        icon: Shield,
        label: "Rug Radar"
    },

    {
        icon: Radar,
        label: "J7 Tracker"
    },

    {
        icon: Activity,
        label: "Portfolio"
    },

    {
        icon: History,
        label: "Replay"
    },

    {
        icon: Bell,
        label: "Alerts"
    },

    {
        icon: PieChart,
        label: "Analytics"
    },

    {
        icon: Settings,
        label: "Settings",
        href: "/settings"
    }

];

export default function Sidebar() {

    return (

        <aside
            className="
            w-64
            bg-[#11161d]
            border-r
            border-zinc-800
            flex
            flex-col
        "
        >

            <div className="text-center py-6">

                <h2 className="text-3xl font-bold text-cyan-400">

                    Sentinel

                </h2>

            </div>

            <nav className="flex-1 px-3 space-y-2">

                {

                    items.map((item) => (

                        <Link

                            key={item.label}

                            href={item.href ?? "#"}

                            className="
                                flex
                                items-center
                                gap-3
                                rounded-lg
                                px-4
                                py-3
                                hover:bg-[#1c2532]
                                transition
                            "

                        >

                            <item.icon size={20} />

                            <span>

                                {item.label}

                            </span>

                        </Link>

                    ))

                }

            </nav>

        </aside>

    );

}