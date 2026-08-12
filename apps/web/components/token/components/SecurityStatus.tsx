"use client";

import {
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ShieldCheck,
  ShieldAlert,
  Lock,
  Flame,
  Coins,
} from "lucide-react";

interface SecurityStatusProps {
  mintAuthority: boolean;
  freezeAuthority: boolean;

  lpLocked: boolean;
  lpBurned: boolean;

  verifiedContract: boolean;
  renounced: boolean;

  honeypot: boolean;

  securityScore?: number;
}

interface RowProps {
  title: string;
  value: boolean;
  positiveLabel: string;
  negativeLabel: string;
}

function SecurityRow({
  title,
  value,
  positiveLabel,
  negativeLabel,
}: RowProps) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-zinc-800 bg-[#1B2330] px-4 py-3">

      <span className="text-sm text-zinc-300">
        {title}
      </span>

      <div className="flex items-center gap-2">

        {value ? (
          <>
            <CheckCircle2
              size={18}
              className="text-green-400"
            />

            <span className="text-sm font-medium text-green-400">
              {positiveLabel}
            </span>
          </>
        ) : (
          <>
            <XCircle
              size={18}
              className="text-red-400"
            />

            <span className="text-sm font-medium text-red-400">
              {negativeLabel}
            </span>
          </>
        )}

      </div>

    </div>
  );
}

export default function SecurityStatus({
  mintAuthority,
  freezeAuthority,
  lpLocked,
  lpBurned,
  verifiedContract,
  renounced,
  honeypot,
  securityScore = 92,
}: SecurityStatusProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-[#11161d] p-5">

      {/* Header */}

      <div className="mb-6 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <ShieldCheck
            className="text-cyan-400"
            size={24}
          />

          <div>

            <h2 className="text-lg font-semibold">

              Security Status

            </h2>

            <p className="text-xs text-zinc-500">

              Rug Radar Security Overview

            </p>

          </div>

        </div>

        <div className="rounded-lg bg-cyan-500 px-4 py-2 font-bold text-black">

          {securityScore}/100

        </div>

      </div>

      {/* Status Grid */}

      <div className="grid gap-3">

        <SecurityRow
          title="Verified Contract"
          value={verifiedContract}
          positiveLabel="Verified"
          negativeLabel="Not Verified"
        />

        <SecurityRow
          title="Mint Authority"
          value={!mintAuthority}
          positiveLabel="Revoked"
          negativeLabel="Enabled"
        />

        <SecurityRow
          title="Freeze Authority"
          value={!freezeAuthority}
          positiveLabel="Revoked"
          negativeLabel="Enabled"
        />

        <SecurityRow
          title="LP Locked"
          value={lpLocked}
          positiveLabel="Locked"
          negativeLabel="Unlocked"
        />

        <SecurityRow
          title="LP Burned"
          value={lpBurned}
          positiveLabel="Burned"
          negativeLabel="Not Burned"
        />

        <SecurityRow
          title="Ownership"
          value={renounced}
          positiveLabel="Renounced"
          negativeLabel="Active"
        />

      </div>

      {/* Risk Warning */}

      <div className="mt-6 rounded-xl border border-zinc-800 bg-[#1B2330] p-4">

        <div className="flex items-center gap-3">

          {honeypot ? (
            <>
              <ShieldAlert
                className="text-red-500"
                size={24}
              />

              <div>

                <div className="font-semibold text-red-400">

                  Honeypot Risk Detected

                </div>

                <div className="text-sm text-zinc-400">

                  Selling restrictions or malicious
                  behavior detected.

                </div>

              </div>
            </>
          ) : (
            <>
              <ShieldCheck
                className="text-green-400"
                size={24}
              />

              <div>

                <div className="font-semibold text-green-400">

                  No Honeypot Detected

                </div>

                <div className="text-sm text-zinc-400">

                  Rug Radar currently detects
                  normal trading behavior.

                </div>

              </div>
            </>
          )}

        </div>

      </div>

      {/* Quick Security Badges */}

      <div className="mt-6 flex flex-wrap gap-3">

        <div className="flex items-center gap-2 rounded-full bg-[#1B2330] px-4 py-2">

          <Lock
            size={16}
            className="text-cyan-400"
          />

          LP Locked

        </div>

        <div className="flex items-center gap-2 rounded-full bg-[#1B2330] px-4 py-2">

          <Flame
            size={16}
            className="text-orange-400"
          />

          LP Burned

        </div>

        <div className="flex items-center gap-2 rounded-full bg-[#1B2330] px-4 py-2">

          <Coins
            size={16}
            className="text-green-400"
          />

          Ownership Renounced

        </div>

        <div className="flex items-center gap-2 rounded-full bg-[#1B2330] px-4 py-2">

          <AlertTriangle
            size={16}
            className="text-yellow-400"
          />

          Rug Radar Active

        </div>

      </div>

    </div>
  );
}