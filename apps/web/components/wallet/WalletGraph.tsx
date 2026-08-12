"use client";

import {
  Brain,
  Network,
  Wallet,
  Fish,
  Crown,
  Coins,
  UserCog,
  Flame,
  Zap,
  Repeat,
  PlayCircle,
  ShieldAlert,
  ZoomIn,
  ZoomOut,
  Move,
  RotateCcw,
  Sparkles,
  Eye,
  Layers,
} from "lucide-react";

export interface WalletNode {
  id: string;
  label: string;

  type:
    | "wallet"
    | "whale"
    | "smart"
    | "holder"
    | "deployer"
    | "jito"
    | "mev";

  risk: number;

  balance: number;
}

export interface WalletEdge {
  from: string;

  to: string;

  amount: number;

  label: string;
}

interface WalletGraphProps {
  nodes: WalletNode[];

  edges: WalletEdge[];

  aiExplanation: string;
}

export default function WalletGraph({
  nodes,
  edges,
  aiExplanation,
}: WalletGraphProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-[#11161d] p-6">

      {/* Header */}

      <div className="mb-8 flex items-center justify-between">

        <div>

          <h2 className="text-2xl font-bold">

            Wallet Graph

          </h2>

          <p className="text-sm text-zinc-500">

            Wallet DNA Relationship Engine

          </p>

        </div>

        <Network
          size={32}
          className="text-cyan-400"
        />

      </div>

      {/* Toolbar */}

      <div className="mb-6 flex flex-wrap gap-3">

        <ToolbarButton
          icon={ZoomIn}
          label="Zoom In"
        />

        <ToolbarButton
          icon={ZoomOut}
          label="Zoom Out"
        />

        <ToolbarButton
          icon={Move}
          label="Pan"
        />

        <ToolbarButton
          icon={RotateCcw}
          label="Reset"
        />

        <ToolbarButton
          icon={PlayCircle}
          label="Replay"
        />

      </div>

      {/* Graph Canvas */}

      <div className="relative mb-8 flex h-[520px] items-center justify-center overflow-hidden rounded-xl border border-zinc-800 bg-[#0B1118]">

        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.08),transparent_70%)]" />

        <div className="text-center">

          <Network
            size={90}
            className="mx-auto text-cyan-500"
          />

          <h3 className="mt-5 text-2xl font-bold">

            Interactive Wallet Graph

          </h3>

          <p className="mt-2 max-w-xl text-zinc-500">

            React Flow / Cytoscape graph renders here with
            draggable nodes, animated money flow, AI overlays,
            replay synchronization and Wallet DNA clusters.

          </p>

        </div>

      </div>

      {/* Statistics */}

      <div className="mb-8 grid gap-4 md:grid-cols-2 xl:grid-cols-5">

        <Metric
          icon={Wallet}
          title="Wallets"
          value={nodes.filter(n => n.type === "wallet").length}
        />

        <Metric
          icon={Fish}
          title="Whales"
          value={nodes.filter(n => n.type === "whale").length}
        />

        <Metric
          icon={Crown}
          title="Smart Money"
          value={nodes.filter(n => n.type === "smart").length}
        />

        <Metric
          icon={Coins}
          title="Transfers"
          value={edges.length}
        />

        <Metric
          icon={ShieldAlert}
          title="Risk Nodes"
          value={nodes.filter(n => n.risk >= 70).length}
        />

      </div>

      {/* Layers */}

      <div className="mb-8">

        <h3 className="mb-4 text-lg font-semibold">

          Graph Layers

        </h3>

        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">

          <LayerItem icon={Wallet} title="Wallet Relationships" />

          <LayerItem icon={Coins} title="Funding Graph" />

          <LayerItem icon={Brain} title="Wallet DNA Clusters" />

          <LayerItem icon={Crown} title="Smart Money Clusters" />

          <LayerItem icon={Fish} title="Whale Clusters" />

          <LayerItem icon={UserCog} title="Deployer Connections" />

          <LayerItem icon={Flame} title="Jito Searchers" />

          <LayerItem icon={Zap} title="MEV Searchers" />

          <LayerItem icon={Repeat} title="Capital Flow Animation" />

          <LayerItem icon={PlayCircle} title="Historical Playback" />

          <LayerItem icon={ShieldAlert} title="Risk Coloring" />

          <LayerItem icon={Eye} title="AI Overlays" />

        </div>

      </div>

      {/* AI */}

      <div className="rounded-xl border border-cyan-900 bg-cyan-950/20 p-6">

        <div className="mb-4 flex items-center gap-2">

          <Sparkles
            className="text-cyan-400"
            size={18}
          />

          <span className="font-semibold">

            Sentinel AI Graph Analysis

          </span>

        </div>

        <p className="leading-7 text-zinc-300">

          {aiExplanation}

        </p>

      </div>

    </div>
  );
}

function ToolbarButton({
  icon: Icon,
  label,
}: {
  icon: React.ElementType;
  label: string;
}) {
  return (
    <button className="flex items-center gap-2 rounded-lg bg-[#1B2330] px-4 py-2 hover:bg-cyan-700">

      <Icon size={16} />

      {label}

    </button>
  );
}

function Metric({
  icon: Icon,
  title,
  value,
}: {
  icon: React.ElementType;
  title: string;
  value: number;
}) {
  return (
    <div className="rounded-xl bg-[#1B2330] p-5">

      <div className="mb-3 flex items-center gap-2">

        <Icon
          size={18}
          className="text-cyan-400"
        />

        <span className="text-sm text-zinc-500">

          {title}

        </span>

      </div>

      <div className="text-3xl font-bold">

        {value}

      </div>

    </div>
  );
}

function LayerItem({
  icon: Icon,
  title,
}: {
  icon: React.ElementType;
  title: string;
}) {
  return (
    <div className="flex items-center gap-3 rounded-xl bg-[#1B2330] p-4">

      <Icon
        size={18}
        className="text-cyan-400"
      />

      <span>{title}</span>

    </div>
  );
}
