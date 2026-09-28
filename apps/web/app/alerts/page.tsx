import ChainTabs from "@/components/ChainTabs/ChainTabs";
import AlertsPanel, {
  type AlertItem,
} from "@/components/Alerts/AlertsPanel";

const alerts: AlertItem[] = [
  {
    id: "1",
    type: "SMART_MONEY",
    severity: "HIGH",
    title: "Smart-money accumulation detected",
    description:
      "Multiple tracked wallets increased exposure to a monitored token.",
    timestamp: "18s ago",
    acknowledged: false,
  },
  {
    id: "2",
    type: "LIQUIDITY",
    severity: "MEDIUM",
    title: "Liquidity inflow accelerating",
    description:
      "Net liquidity entering the tracked pool has increased over the latest observation window.",
    timestamp: "41s ago",
    acknowledged: false,
  },
  {
    id: "3",
    type: "NARRATIVE",
    severity: "LOW",
    title: "Narrative momentum rising",
    description:
      "Sentinel detected increasing narrative activity across monitored sources.",
    timestamp: "2m ago",
    acknowledged: true,
  },
  {
    id: "4",
    type: "RUG",
    severity: "CRITICAL",
    title: "Contract risk signal detected",
    description:
      "A monitored contract produced a security signal requiring review.",
    timestamp: "4m ago",
    acknowledged: false,
  },
];

export default function AlertsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Alerts</h1>
        <p className="mt-1 text-sm text-[#777]">
          Centralized Sentinel intelligence alert stream.
        </p>
      </div>

      <ChainTabs />

      <AlertsPanel alerts={alerts} />
    </div>
  );
}