"use client";

import { useState } from "react";

import TradingToolbar from "./TradingToolbar";
import TradingViewWidget from "./TradingViewWidget";
import ChartControls from "./ChartControls";
import ChartOverlay from "./ChartOverlay";
import ChartMarkers from "./ChartMarkers";
import ChartLegend from "./ChartLegend";

export default function TradingChart() {
  const [symbol, setSymbol] = useState("SOL");
  const [timeframe, setTimeframe] = useState("1m");

  const [showMarkers, setShowMarkers] = useState(true);
  const [showOverlay, setShowOverlay] = useState(true);

  return (
    <div className="flex flex-col w-full h-full rounded-xl overflow-hidden border border-zinc-800 bg-[#11161d]">

      {/* Toolbar */}

      <TradingToolbar
        symbol={symbol}
        timeframe={timeframe}
        onSymbolChange={setSymbol}
        onTimeframeChange={setTimeframe}
      />

      {/* Chart */}

      <div className="relative flex-1">

        <TradingViewWidget
          symbol={symbol}
          timeframe={timeframe}
        />

        {showOverlay && (
          <ChartOverlay />
        )}

        {showMarkers && (
          <ChartMarkers />
        )}

      </div>

      {/* Bottom Controls */}

      <ChartControls
        showMarkers={showMarkers}
        showOverlay={showOverlay}
        onToggleMarkers={() =>
          setShowMarkers((v) => !v)
        }
        onToggleOverlay={() =>
          setShowOverlay((v) => !v)
        }
      />

      {/* Legend */}

      <ChartLegend />

    </div>
  );
}