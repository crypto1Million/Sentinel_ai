"use client";

import { useEffect, useRef } from "react";

interface TradingViewWidgetProps {
  symbol: string;
  timeframe: string;
}

declare global {
  interface Window {
    TradingView: any;
  }
}

export default function TradingViewWidget({
  symbol,
  timeframe,
}: TradingViewWidgetProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Clear previous chart
    containerRef.current.innerHTML = "";

    // Prevent duplicate script
    const existing = document.getElementById("tv-widget-script");

    const initializeChart = () => {
      if (!window.TradingView) return;

      new window.TradingView.widget({
        autosize: true,

        symbol,

        interval: timeframe,

        timezone: "Etc/UTC",

        theme: "dark",

        style: "1",

        locale: "en",

        hide_side_toolbar: false,

        allow_symbol_change: false,

        withdateranges: false,

        details: false,

        hotlist: false,

        calendar: false,

        studies: [],

        container: containerRef.current!,
      });
    };

    if (window.TradingView) {
      initializeChart();
      return;
    }

    if (!existing) {
      const script = document.createElement("script");

      script.id = "tv-widget-script";

      script.src =
        "https://s3.tradingview.com/tv.js";

      script.async = true;

      script.onload = initializeChart;

      document.body.appendChild(script);
    }
  }, [symbol, timeframe]);

  return (
    <div
      ref={containerRef}
      className="h-full w-full"
    />
  );
}