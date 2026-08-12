"use client";

import {
  Brain,
  ShieldAlert,
  Wallet,
  Fish,
  Zap,
  Flame,
  Activity,
  DollarSign,
} from "lucide-react";

interface Marker {

  id: number;

  x: number;

  y: number;

  label: string;

  color: string;

  icon: any;

}

const markers: Marker[] = [

  {
    id: 1,
    x: 15,
    y: 20,
    label: "AI Buy",
    color: "bg-cyan-500",
    icon: Brain,
  },

  {
    id: 2,
    x: 32,
    y: 42,
    label: "Whale Buy",
    color: "bg-green-500",
    icon: Fish,
  },

  {
    id: 3,
    x: 47,
    y: 30,
    label: "Bundle",
    color: "bg-purple-500",
    icon: Zap,
  },

  {
    id: 4,
    x: 61,
    y: 60,
    label: "Wallet DNA",
    color: "bg-yellow-500",
    icon: Wallet,
  },

  {
    id: 5,
    x: 76,
    y: 18,
    label: "Rug Risk",
    color: "bg-red-500",
    icon: ShieldAlert,
  },

  {
    id: 6,
    x: 83,
    y: 48,
    label: "Narrative",
    color: "bg-orange-500",
    icon: Flame,
  },

  {
    id: 7,
    x: 90,
    y: 32,
    label: "Liquidity",
    color: "bg-blue-500",
    icon: DollarSign,
  },

  {
    id: 8,
    x: 95,
    y: 72,
    label: "Smart Money",
    color: "bg-pink-500",
    icon: Activity,
  },

];

export default function ChartMarkers() {

  return (

    <>

      {

        markers.map((marker) => {

          const Icon = marker.icon;

          return (

            <div

              key={marker.id}

              className="absolute group z-30"

              style={{

                left: `${marker.x}%`,

                top: `${marker.y}%`,

              }}

            >

              <div

                className={`

                  h-8

                  w-8

                  rounded-full

                  ${marker.color}

                  flex

                  items-center

                  justify-center

                  shadow-lg

                  cursor-pointer

                  hover:scale-110

                  transition

                `}

              >

                <Icon size={16} />

              </div>

              {/* Tooltip */}

              <div

                className="

                  absolute

                  left-1/2

                  -translate-x-1/2

                  mt-2

                  hidden

                  whitespace-nowrap

                  rounded-lg

                  bg-black

                  px-3

                  py-2

                  text-xs

                  group-hover:block

                "

              >

                {marker.label}

              </div>

            </div>

          );

        })

      }

    </>

  );

}