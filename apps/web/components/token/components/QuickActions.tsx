"use client";

import {
  Star,
  Bell,
  Eye,
  EyeOff,
  Share2,
  Copy,
  ExternalLink,
  Bookmark,
  Wallet,
  Brain,
  Shield,
  Play,
  Flag,
} from "lucide-react";

import { useState } from "react";

interface QuickActionsProps {
  contract: string;

  explorerUrl?: string;

  dexUrl?: string;

  onAIAnalysis?: () => void;

  onReplay?: () => void;

  onWalletDNA?: () => void;

  onRugRadar?: () => void;
}

export default function QuickActions({
  contract,
  explorerUrl,
  dexUrl,
  onAIAnalysis,
  onReplay,
  onWalletDNA,
  onRugRadar,
}: QuickActionsProps) {
  const [favorite, setFavorite] = useState(false);

  const [watching, setWatching] = useState(true);

  const [copied, setCopied] = useState(false);

  async function copyContract() {
    await navigator.clipboard.writeText(contract);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1500);
  }

  return (
    <div className="rounded-xl border border-zinc-800 bg-[#11161d] p-5">

      <div className="mb-6">

        <h2 className="text-lg font-semibold">

          Quick Actions

        </h2>

        <p className="text-xs text-zinc-500">

          Token shortcuts and Sentinel tools

        </p>

      </div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">

        <ActionButton
          icon={Star}
          title={favorite ? "Favorited" : "Favorite"}
          color={favorite ? "text-yellow-400" : ""}
          onClick={() => setFavorite(!favorite)}
        />

        <ActionButton
          icon={watching ? Eye : EyeOff}
          title={watching ? "Watching" : "Watchlist"}
          color={watching ? "text-cyan-400" : ""}
          onClick={() => setWatching(!watching)}
        />

        <ActionButton
          icon={Copy}
          title={copied ? "Copied" : "Copy Contract"}
          onClick={copyContract}
        />

        {explorerUrl && (
          <a
            href={explorerUrl}
            target="_blank"
            className="rounded-lg border border-zinc-700 bg-[#1B2330] p-4 hover:bg-[#263244]"
          >
            <div className="flex items-center gap-3">

              <ExternalLink size={20} />

              <span>Explorer</span>

            </div>
          </a>
        )}

        {dexUrl && (
          <a
            href={dexUrl}
            target="_blank"
            className="rounded-lg border border-zinc-700 bg-[#1B2330] p-4 hover:bg-[#263244]"
          >
            <div className="flex items-center gap-3">

              <Share2 size={20} />

              <span>Open DEX</span>

            </div>
          </a>
        )}

        <ActionButton
          icon={Brain}
          title="AI Analysis"
          onClick={onAIAnalysis}
        />

        <ActionButton
          icon={Shield}
          title="Rug Radar"
          onClick={onRugRadar}
        />

        <ActionButton
          icon={Wallet}
          title="Wallet DNA"
          onClick={onWalletDNA}
        />

        <ActionButton
          icon={Play}
          title="Replay"
          onClick={onReplay}
        />

        <ActionButton
          icon={Bell}
          title="Create Alert"
        />

        <ActionButton
          icon={Bookmark}
          title="Bookmark"
        />

        <ActionButton
          icon={Flag}
          title="Report Token"
        />

      </div>

    </div>
  );
}

interface ActionButtonProps {
  icon: React.ElementType;

  title: string;

  color?: string;

  onClick?: () => void;
}

function ActionButton({
  icon: Icon,
  title,
  color = "",
  onClick,
}: ActionButtonProps) {
  return (
    <button
      onClick={onClick}
      className="
        rounded-lg
        border
        border-zinc-700
        bg-[#1B2330]
        p-4
        transition
        hover:bg-[#263244]
      "
    >
      <div className="flex flex-col items-center gap-3">

        <Icon
          size={22}
          className={color}
        />

        <span className="text-sm font-medium">

          {title}

        </span>

      </div>

    </button>
  );
}
```
