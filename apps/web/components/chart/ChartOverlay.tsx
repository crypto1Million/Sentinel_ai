"use client";

import { useState } from "react";

import {
    Brain,
    ShieldAlert,
    Wallet,
    Waves,
    Users,
    Zap,
    Network,
    Activity,
    Eye,
    EyeOff
} from "lucide-react";

export default function ChartOverlay() {

    const [visible, setVisible] = useState(true);

    const overlays = [

        {
            name: "Sentinel AI",
            icon: Brain,
            color: "text-cyan-400"
        },

        {
            name: "Rug Radar",
            icon: ShieldAlert,
            color: "text-red-500"
        },

        {
            name: "Wallet DNA",
            icon: Wallet,
            color: "text-green-400"
        },

        {
            name: "Liquidity",
            icon: Waves,
            color: "text-blue-400"
        },

        {
            name: "Holder Analysis",
            icon: Users,
            color: "text-yellow-400"
        },

        {
            name: "Jito Bundles",
            icon: Zap,
            color: "text-purple-400"
        },

        {
            name: "Wallet Graph",
            icon: Network,
            color: "text-pink-400"
        },

        {
            name: "Market Intelligence",
            icon: Activity,
            color: "text-orange-400"
        }

    ];

    return (

        <>

            {/* Overlay Toggle */}

            <button

                onClick={() => setVisible(!visible)}

                className="

                absolute

                top-4

                right-4

                z-50

                rounded-lg

                bg-[#0F1722]

                border

                border-zinc-700

                p-2

                "

            >

                {

                    visible

                        ? <Eye size={18}/>

                        : <EyeOff size={18}/>

                }

            </button>

            {

                visible && (

                    <div

                        className="

                        absolute

                        top-16

                        right-4

                        w-64

                        rounded-xl

                        border

                        border-zinc-800

                        bg-[#11161d]

                        shadow-2xl

                        z-40

                        "

                    >

                        <div className="

                            border-b

                            border-zinc-800

                            px-4

                            py-3

                            font-semibold

                            "

                        >

                            Active Overlays

                        </div>

                        <div className="p-3 space-y-3">

                            {

                                overlays.map((overlay) => (

                                    <div

                                        key={overlay.name}

                                        className="

                                        flex

                                        items-center

                                        justify-between

                                        "

                                    >

                                        <div className="flex items-center gap-3">

                                            <overlay.icon

                                                size={18}

                                                className={overlay.color}

                                            />

                                            <span>

                                                {overlay.name}

                                            </span>

                                        </div>

                                        <input

                                            type="checkbox"

                                            defaultChecked

                                        />

                                    </div>

                                ))

                            }

                        </div>

                    </div>

                )

            }

        </>

    );

}