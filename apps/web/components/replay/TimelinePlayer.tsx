"use client";

import { useEffect, useState } from "react";

import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  Clock,
  Calendar,
  Activity,
  Brain,
  ShieldAlert,
  Wallet,
  Coins,
  TrendingUp,
  TrendingDown,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

export interface ReplayEvent {
  id: string;

  timestamp: string;

  title: string;

  description: string;

  type:
    | "PRICE"
    | "TRADE"
    | "WALLET"
    | "RUG"
    | "MEV"
    | "LIQUIDITY"
    | "AI";

  value?: string;
}

interface TimelinePlayerProps {
  events: ReplayEvent[];

  currentIndex: number;

  isPlaying: boolean;

  playbackSpeed: number;

  onPlay(): void;

  onPause(): void;

  onNext(): void;

  onPrevious(): void;

  onRestart(): void;

  onSeek(index: number): void;
}

export default function TimelinePlayer({
  events,
  currentIndex,
  isPlaying,
  playbackSpeed,
  onPlay,
  onPause,
  onNext,
  onPrevious,
  onRestart,
  onSeek,
}: TimelinePlayerProps) {
  const currentEvent = events[currentIndex];

  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6 space-y-8">

      {/* Header */}

      <div className="flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold">

            Replay Timeline

          </h2>

          <p className="text-sm text-zinc-500">

            Historical Market Replay Engine

          </p>

        </div>

        <Clock
          className="text-cyan-400"
          size={30}
        />

      </div>

      {/* Controls */}

      <div className="flex flex-wrap items-center gap-3">

        <button
          onClick={onRestart}
          className="rounded-lg bg-zinc-800 p-3 hover:bg-zinc-700"
        >
          <RotateCcw size={18} />
        </button>

        <button
          onClick={onPrevious}
          className="rounded-lg bg-zinc-800 p-3 hover:bg-zinc-700"
        >
          <SkipBack size={18} />
        </button>

        <button
          onClick={isPlaying ? onPause : onPlay}
          className="rounded-xl bg-cyan-500 px-6 py-3 font-bold text-black hover:bg-cyan-400"
        >
          {isPlaying ? <Pause /> : <Play />}
        </button>

        <button
          onClick={onNext}
          className="rounded-lg bg-zinc-800 p-3 hover:bg-zinc-700"
        >
          <SkipForward size={18} />
        </button>

        <div className="ml-auto rounded-lg bg-[#1B2330] px-4 py-2">

          {playbackSpeed}x Speed

        </div>

      </div>

      {/* Timeline */}

      <div>

        <div className="mb-3 flex justify-between text-sm text-zinc-500">

          <span>

            Timeline

          </span>

          <span>

            {currentIndex + 1} / {events.length}

          </span>

        </div>

        <input
          type="range"
          min={0}
          max={Math.max(events.length - 1, 0)}
          value={currentIndex}
          onChange={(e) =>
            onSeek(Number(e.target.value))
          }
          className="w-full accent-cyan-500"
        />

      </div>

      {/* Current Event */}

      {currentEvent && (

        <div className="rounded-xl border border-cyan-800 bg-[#1B2330] p-6">

          <div className="mb-5 flex items-center gap-3">

            <EventIcon type={currentEvent.type} />

            <div>

              <h3 className="text-xl font-bold">

                {currentEvent.title}

              </h3>

              <p className="text-sm text-zinc-500">

                {currentEvent.timestamp}

              </p>

            </div>

          </div>

          <p className="leading-7 text-zinc-300">

            {currentEvent.description}

          </p>

          {currentEvent.value && (

            <div className="mt-5 rounded-lg bg-zinc-900 p-4 font-semibold text-cyan-400">

              {currentEvent.value}

            </div>

          )}

        </div>

      )}

      {/* Event List */}

      <div>

        <h3 className="mb-4 font-semibold">

          Timeline Events

        </h3>

        <div className="space-y-3 max-h-96 overflow-y-auto">

          {events.map((event, index) => (

            <button
              key={event.id}
              onClick={() => onSeek(index)}
              className={`w-full rounded-xl border p-4 text-left transition ${
                currentIndex === index
                  ? "border-cyan-500 bg-cyan-950/20"
                  : "border-zinc-800 bg-[#1B2330] hover:border-zinc-700"
              }`}
            >

              <div className="flex items-center gap-3">

                <EventIcon type={event.type} />

                <div className="flex-1">

                  <div className="font-semibold">

                    {event.title}

                  </div>

                  <div className="text-sm text-zinc-500">

                    {event.timestamp}

                  </div>

                </div>

                {currentIndex === index && (

                  <ChevronRight className="text-cyan-400" />

                )}

              </div>

            </button>

          ))}

        </div>

      </div>

      {/* Footer */}

      <div className="rounded-xl bg-[#1B2330] p-5">

        <div className="flex items-center gap-2">

          <Brain
            size={18}
            className="text-cyan-400"
          />

          <span className="font-semibold">

            Sentinel Replay AI

          </span>

        </div>

        <p className="mt-3 text-zinc-400 leading-7">

          Replay reconstructs historical token activity using blocks,
          wallet movements, liquidity updates, MEV events,
          Jito bundles, Sentinel scores and AI intelligence to
          understand exactly how a token evolved over time.

        </p>

      </div>

    </div>
  );
}

function EventIcon({
  type,
}: {
  type: ReplayEvent["type"];
}) {
  switch (type) {
    case "PRICE":
      return <TrendingUp className="text-green-400" />;

    case "TRADE":
      return <Coins className="text-cyan-400" />;

    case "WALLET":
      return <Wallet className="text-blue-400" />;

    case "RUG":
      return <ShieldAlert className="text-red-400" />;

    case "MEV":
      return <Activity className="text-yellow-400" />;

    case "LIQUIDITY":
      return <TrendingDown className="text-orange-400" />;

    case "AI":
      return <Brain className="text-purple-400" />;

    default:
      return <Calendar />;
  }
}
