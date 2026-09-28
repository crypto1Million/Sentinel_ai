import ChainTabs from "@/components/ChainTabs/ChainTabs";
import J7Tracker, {
  type J7Wallet,
} from "@/components/j7/J7Tracker";

const wallets: J7Wallet[] = [
  {
    id: "1",
    address: "7xJ...92K",
    label: "Smart Wallet Alpha",
    score: 94,
    pnl: 182.4,
    winRate: 78,
    lastAction: "BUY",
    token: "$SENTRY",
    amount: 12500,
    timestamp: "12s ago",
  },
  {
    id: "2",
    address: "9Qa...M2L",
    label: "Whale Cluster 04",
    score: 89,
    pnl: 94.1,
    winRate: 71,
    lastAction: "BUY",
    token: "$NOVA",
    amount: 8200,
    timestamp: "36s ago",
  },
  {
    id: "3",
    address: "4Zp...F7A",
    label: "Momentum Wallet",
    score: 86,
    pnl: -11.2,
    winRate: 69,
    lastAction: "SELL",
    token: "$ROAR",
    amount: 3200,
    timestamp: "1m ago",
  },
];

export default function TrackerPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Tracker</h1>
        <p className="mt-1 text-sm text-[#777]">
          J7 smart-money, whale and wallet activity intelligence.
        </p>
      </div>

      <ChainTabs />

      <J7Tracker
        score={91}
        confidence={94}
        wallets={wallets}
        smartMoneyCount={127}
        whaleCount={31}
        activeWallets={842}
        aiSummary="Smart-money activity is concentrated around a small number of high-conviction wallets. Recent accumulation is strongest in the highest-ranked opportunities."
      />
    </div>
  );
}