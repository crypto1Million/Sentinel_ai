"use client";

import { useState } from "react";
import ChainTabs from "@/components/ChainTabs/ChainTabs";

export default function SettingsPage() {
  const [notifications, setNotifications] = useState(true);
  const [riskAlerts, setRiskAlerts] = useState(true);
  const [smartMoneyAlerts, setSmartMoneyAlerts] = useState(true);
  const [compactMode, setCompactMode] = useState(false);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="mt-1 text-sm text-[#777]">
          Configure Sentinel terminal behavior and intelligence preferences.
        </p>
      </div>

      <ChainTabs />

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="rounded-2xl border border-[#292929] bg-[#101010] p-6">
          <h2 className="text-xl font-semibold">
            Intelligence
          </h2>

          <div className="mt-5 space-y-4">
            <ToggleRow
              title="Notifications"
              description="Enable Sentinel system notifications."
              enabled={notifications}
              onToggle={() => setNotifications((value) => !value)}
            />

            <ToggleRow
              title="Risk Alerts"
              description="Notify when Rug Radar risk changes materially."
              enabled={riskAlerts}
              onToggle={() => setRiskAlerts((value) => !value)}
            />

            <ToggleRow
              title="Smart Money Alerts"
              description="Notify on tracked wallet activity."
              enabled={smartMoneyAlerts}
              onToggle={() =>
                setSmartMoneyAlerts((value) => !value)
              }
            />

            <ToggleRow
              title="Compact Mode"
              description="Reduce spacing across terminal panels."
              enabled={compactMode}
              onToggle={() => setCompactMode((value) => !value)}
            />
          </div>
        </section>

        <section className="rounded-2xl border border-[#292929] bg-[#101010] p-6">
          <h2 className="text-xl font-semibold">
            Trading Defaults
          </h2>

          <div className="mt-5 space-y-4">
            <SettingField
              label="Default Slippage"
              value="0.50%"
            />

            <SettingField
              label="Default Priority Fee"
              value="0.0001 SOL"
            />

            <SettingField
              label="Max Position Risk"
              value="2.00%"
            />

            <SettingField
              label="Execution Mode"
              value="AUTO"
            />
          </div>
        </section>
      </div>

      <section className="rounded-2xl border border-[#292929] bg-[#101010] p-6">
        <h2 className="text-xl font-semibold">
          Backend Connections
        </h2>

        <div className="mt-5 grid gap-3 md:grid-cols-2">
          <Connection
            name="Sentinel API"
            status="Configured"
          />

          <Connection
            name="PostgreSQL"
            status="Local configuration"
          />

          <Connection
            name="Redis"
            status="Configuration ready"
          />

          <Connection
            name="Chain RPC"
            status="Controlled by backend"
          />
        </div>

        <div className="mt-5 rounded-xl border border-[#5A4718] bg-[#17130A] p-4 text-sm text-[#B9A76A]">
          API keys, private keys and RPC credentials should remain
          in the backend environment files and must not be moved
          into client-side NEXT_PUBLIC variables.
        </div>
      </section>
    </div>
  );
}

function ToggleRow({
  title,
  description,
  enabled,
  onToggle,
}: {
  title: string;
  description: string;
  enabled: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-[#292929] bg-[#171717] p-4">
      <div>
        <div className="font-medium">{title}</div>
        <div className="mt-1 text-xs text-[#666]">
          {description}
        </div>
      </div>

      <button
        type="button"
        onClick={onToggle}
        aria-pressed={enabled}
        className={[
          "relative h-6 w-11 rounded-full transition",
          enabled ? "bg-[#D4AF37]" : "bg-[#333]",
        ].join(" ")}
      >
        <span
          className={[
            "absolute top-1 h-4 w-4 rounded-full bg-white transition",
            enabled ? "left-6" : "left-1",
          ].join(" ")}
        />
      </button>
    </div>
  );
}

function SettingField({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-[#292929] bg-[#171717] p-4">
      <div className="text-xs uppercase tracking-wider text-[#666]">
        {label}
      </div>

      <div className="mt-2 font-semibold text-white">
        {value}
      </div>
    </div>
  );
}

function Connection({
  name,
  status,
}: {
  name: string;
  status: string;
}) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-[#292929] bg-[#171717] p-4">
      <span className="font-medium">{name}</span>

      <span className="flex items-center gap-2 text-sm text-green-400">
        <span className="h-2 w-2 rounded-full bg-green-400" />
        {status}
      </span>
    </div>
  );
}