"use client";

import type { ElementType } from "react";
import { useState } from "react";

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
    try {
      await navigator.clipboard.writeText(contract);
      setCopied(true);

      window.setTimeout(() => {
        setCopied(false);
      }, 1500);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div className="rounded-xl border border-[#292929] bg-[#101010] p-5">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-white">
          Quick Actions
        </h2>

        <p className="text-xs text-[#8B8B8B]">
          Token shortcuts and Sentinel tools
        </p>
      </div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <ActionButton
          icon={Star}
          title={favorite ? "Favorited" : "Favorite"}
          color={favorite ? "text-[#F5C84C]" : undefined}
          onClick={() => setFavorite((current) => !current)}
        />

        <ActionButton
          icon={watching ? Eye : EyeOff}
          title={watching ? "Watching" : "Watchlist"}
          color={watching ? "text-[#D4AF37]" : undefined}
          onClick={() => setWatching((current) => !current)}
        />

        <ActionButton
          icon={Copy}
          title={copied ? "Copied" : "Copy Contract"}
          color={copied ? "text-green-400" : undefined}
          onClick={copyContract}
        />

        {explorerUrl && (
          <a
            href={explorerUrl}
            target="_blank"
            rel="noreferrer"
            className="rounded-lg border border-[#292929] bg-[#171717] p-4 transition hover:border-[#8C6D1F] hover:bg-[#1f1a0f]"
          >
            <div className="flex items-center gap-3">
              <ExternalLink
                size={20}
                className="text-[#D4AF37]"
              />

              <span className="text-white">
                Explorer
              </span>
            </div>
          </a>
        )}

        {dexUrl && (
          <a
            href={dexUrl}
            target="_blank"
            rel="noreferrer"
            className="rounded-lg border border-[#292929] bg-[#171717] p-4 transition hover:border-[#8C6D1F] hover:bg-[#1f1a0f]"
          >
            <div className="flex items-center gap-3">
              <Share2
                size={20}
                className="text-[#D4AF37]"
              />

              <span className="text-white">
                Open DEX
              </span>
            </div>
          </a>
        )}

        <ActionButton
          icon={Brain}
          title="AI Analysis"
          color="text-purple-400"
          onClick={onAIAnalysis}
        />

        <ActionButton
          icon={Shield}
          title="Rug Radar"
          color="text-red-400"
          onClick={onRugRadar}
        />

        <ActionButton
          icon={Wallet}
          title="Wallet DNA"
          color="text-blue-400"
          onClick={onWalletDNA}
        />

        <ActionButton
          icon={Play}
          title="Replay"
          color="text-[#D4AF37]"
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
          color="text-red-400"
        />
      </div>
    </div>
  );
}

interface ActionButtonProps {
  icon: ElementType;
  title: string;
  color?: string;
  onClick?: () => void;
}

function ActionButton({
  icon: Icon,
  title,
  color = "text-[#8B8B8B]",
  onClick,
}: ActionButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="rounded-lg border border-[#292929] bg-[#171717] p-4 transition hover:border-[#8C6D1F] hover:bg-[#1f1a0f]"
    >
      <div className="flex flex-col items-center gap-3">
        <Icon
          size={22}
          className={color}
        />

        <span className="text-sm font-medium text-white">
          {title}
        </span>
      </div>
    </button>
  );
}