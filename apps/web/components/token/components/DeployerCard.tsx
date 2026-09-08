"use client";

import {
  ShieldCheck,
  ShieldAlert,
  Wallet,
  Trophy,
  TrendingUp,
  TrendingDown,
  Coins,
  ExternalLink,
  Copy,
} from "lucide-react";

interface DeployerCardProps {
  address: string;
  verified: boolean;
  reputationScore: number;
  totalTokens: number;
  successfulTokens: number;
  ruggedTokens: number;
  winRate: number;
  currentHoldings: number;
  soldPercentage: number;
  explorerUrl?: string;
}

export default function DeployerCard({
  address,
  verified,
  reputationScore,
  totalTokens,
  successfulTokens,
  ruggedTokens,
  winRate,
  currentHoldings,
  soldPercentage,
  explorerUrl,
}: DeployerCardProps) {
  async function copyAddress() {
    await navigator.clipboard.writeText(address);
  }

  const shortAddress =
    address.length > 14
      ? `${address.slice(0, 6)}...${address.slice(-6)}`
      : address;

  return (
    <div className="rounded-xl border border-[#292929] bg-[#101010] p-5">
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Wallet
            size={24}
            className="text-[#D4AF37]"
          />

          <div>
            <h2 className="text-lg font-semibold text-white">
              Deployer Intelligence
            </h2>

            <p className="text-xs text-[#8B8B8B]">
              Creator wallet reputation and history
            </p>
          </div>
        </div>

        {verified ? (
          <div className="flex items-center gap-2 rounded-lg border border-[#8C6D1F] bg-[#171717] px-3 py-2 text-[#F5C84C]">
            <ShieldCheck size={16} />
            <span className="text-sm font-medium">
              Verified
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-2 rounded-lg border border-red-900 bg-red-950/20 px-3 py-2 text-red-400">
            <ShieldAlert size={16} />
            <span className="text-sm font-medium">
              Unverified
            </span>
          </div>
        )}
      </div>

      {/* Address */}

      <div className="mb-6 rounded-xl border border-[#292929] bg-[#171717] p-4">
        <div className="mb-2 text-xs text-[#8B8B8B]">
          Deployer Wallet
        </div>

        <div className="flex items-center justify-between gap-3">
          <code className="text-sm text-[#F5C84C]">
            {shortAddress}
          </code>

          <div className="flex items-center gap-2">
            <button
              onClick={copyAddress}
              className="rounded-md border border-[#292929] p-2 text-[#8B8B8B] hover:text-white"
            >
              <Copy size={15} />
            </button>

            {explorerUrl && (
              <a
                href={explorerUrl}
                target="_blank"
                rel="noreferrer"
                className="rounded-md border border-[#292929] p-2 text-[#8B8B8B] hover:text-white"
              >
                <ExternalLink size={15} />
              </a>
            )}
          </div>
        </div>
      </div>

      {/* Reputation */}

      <div className="mb-6 rounded-xl border border-[#8C6D1F] bg-[#171717] p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Trophy
              size={18}
              className="text-[#D4AF37]"
            />

            <span className="text-sm text-[#8B8B8B]">
              Reputation Score
            </span>
          </div>

          <span className="text-2xl font-bold text-[#F5C84C]">
            {reputationScore}/100
          </span>
        </div>

        <div className="h-2 overflow-hidden rounded-full bg-[#070707]">
          <div
            className="h-full rounded-full bg-[#D4AF37]"
            style={{
              width: `${Math.max(
                0,
                Math.min(reputationScore, 100)
              )}%`,
            }}
          />
        </div>
      </div>

      {/* Metrics */}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <Metric
          title="Tokens Created"
          value={totalTokens}
          icon={Coins}
          color="text-[#D4AF37]"
        />

        <Metric
          title="Successful Tokens"
          value={successfulTokens}
          icon={TrendingUp}
          color="text-green-400"
        />

        <Metric
          title="Rugged Tokens"
          value={ruggedTokens}
          icon={TrendingDown}
          color="text-red-400"
        />

        <Metric
          title="Win Rate"
          value={`${winRate}%`}
          icon={Trophy}
          color="text-[#F5C84C]"
        />

        <Metric
          title="Current Holdings"
          value={`${currentHoldings}%`}
          icon={Wallet}
          color="text-blue-400"
        />

        <Metric
          title="Sold"
          value={`${soldPercentage}%`}
          icon={Coins}
          color="text-orange-400"
        />
      </div>
    </div>
  );
}

function Metric({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string;
  value: string | number;
  icon: React.ElementType;
  color: string;
}) {
  return (
    <div className="rounded-xl border border-[#292929] bg-[#171717] p-4">
      <div className="mb-3 flex items-center gap-2">
        <Icon
          size={17}
          className={color}
        />

        <span className="text-sm text-[#8B8B8B]">
          {title}
        </span>
      </div>

      <div className="text-xl font-semibold text-white">
        {value}
      </div>
    </div>
  );
}