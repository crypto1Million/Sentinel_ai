"use client";

import { RefreshCw, Search, Camera, Download } from "lucide-react";

interface TradingToolbarProps {
  symbol: string;
  timeframe: string;
  onSymbolChange: (symbol: string) => void;
  onTimeframeChange: (timeframe: string) => void;
}

const TIMEFRAMES = [
  "1s",
  "5s",
  "15s",
  "30s",
  "1m",
  "3m",
  "5m",
  "15m",
  "1H",
  "4H",
  "1D"
];

export default function TradingToolbar({

  symbol,

  timeframe,

  onSymbolChange,

  onTimeframeChange

}: TradingToolbarProps) {

  return (

    <div className="flex items-center justify-between h-14 px-4 border-b border-zinc-800 bg-[#0F1722]">

      {/* Left */}

      <div className="flex items-center gap-4">

        <div className="text-lg font-bold text-cyan-400">

          Chart

        </div>

        <div className="relative">

          <Search
            size={16}
            className="absolute left-3 top-3 text-gray-400"
          />

          <input

            value={symbol}

            onChange={(e) =>
              onSymbolChange(e.target.value)
            }

            placeholder="Search Token..."

            className="

            pl-9

            pr-3

            py-2

            rounded-lg

            bg-[#1B2330]

            border

            border-zinc-700

            outline-none

            w-60

            "

          />

        </div>

      </div>

      {/* Middle */}

      <div className="flex items-center gap-2">

        {

          TIMEFRAMES.map((tf) => (

            <button

              key={tf}

              onClick={() =>

                onTimeframeChange(tf)

              }

              className={`

              px-3

              py-1.5

              rounded

              text-sm

              transition

              ${

                timeframe === tf

                  ? "bg-cyan-500 text-black font-semibold"

                  : "bg-[#1B2330] hover:bg-[#263244]"

              }

              `}

            >

              {tf}

            </button>

          ))

        }

      </div>

      {/* Right */}

      <div className="flex items-center gap-2">

        <button

          className="

          p-2

          rounded-lg

          bg-[#1B2330]

          hover:bg-[#263244]

          "

        >

          <RefreshCw size={18} />

        </button>

        <button

          className="

          p-2

          rounded-lg

          bg-[#1B2330]

          hover:bg-[#263244]

          "

        >

          <Camera size={18} />

        </button>

        <button

          className="

          p-2

          rounded-lg

          bg-[#1B2330]

          hover:bg-[#263244]

          "

        >

          <Download size={18} />

        </button>

      </div>

    </div>

  );

}
