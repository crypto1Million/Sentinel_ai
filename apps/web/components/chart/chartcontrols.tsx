"use client";

import {
  Eye,
  EyeOff,
  RotateCcw,
  Maximize2,
  Minimize2,
  Play,
  Pause,
  SkipForward,
  SkipBack,
  RefreshCw,
  ZoomIn,
  ZoomOut,
  MousePointer2,
} from "lucide-react";

interface ChartControlsProps {
  showMarkers: boolean;
  showOverlay: boolean;

  onToggleMarkers: () => void;
  onToggleOverlay: () => void;
}

export default function ChartControls({

  showMarkers,

  showOverlay,

  onToggleMarkers,

  onToggleOverlay,

}: ChartControlsProps) {

  return (

    <div className="flex items-center justify-between border-t border-zinc-800 bg-[#0F1722] px-4 py-2">

      {/* Left */}

      <div className="flex items-center gap-2">

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <SkipBack size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <Play size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <Pause size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <SkipForward size={16} />
        </button>

      </div>

      {/* Middle */}

      <div className="flex items-center gap-2">

        <button
          onClick={onToggleMarkers}
          className="rounded bg-[#1B2330] px-3 py-2 hover:bg-[#263244]"
        >
          {showMarkers ? (
            <Eye size={16} />
          ) : (
            <EyeOff size={16} />
          )}
        </button>

        <button
          onClick={onToggleOverlay}
          className="rounded bg-[#1B2330] px-3 py-2 hover:bg-[#263244]"
        >
          Overlay
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <ZoomIn size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <ZoomOut size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <RotateCcw size={16} />
        </button>

      </div>

      {/* Right */}

      <div className="flex items-center gap-2">

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <MousePointer2 size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <RefreshCw size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <Maximize2 size={16} />
        </button>

        <button className="rounded bg-[#1B2330] p-2 hover:bg-[#263244]">
          <Minimize2 size={16} />
        </button>

      </div>

    </div>

  );

}