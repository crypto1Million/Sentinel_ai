"use client";

import { useChainStore, type ChainId } from "@/store/chainStore";

interface ChainOption {
  id: ChainId;
  name: string;
  symbol: string;
  icon: string;
}

const CHAINS: ChainOption[] = [
  {
    id: "solana",
    name: "Solana",
    symbol: "SOL",
    icon: "/brand/chains/solana.svg",
  },
  {
    id: "base",
    name: "Base",
    symbol: "ETH",
    icon: "/brand/chains/base.svg",
  },
  {
    id: "ethereum",
    name: "Ethereum",
    symbol: "ETH",
    icon: "/brand/chains/ethereum.svg",
  },
  {
    id: "bnb",
    name: "BNB",
    symbol: "BNB",
    icon: "/brand/chains/bnb.svg",
  },
  {
    id: "robinhood",
    name: "Robinhood",
    symbol: "HOOD",
    icon: "/brand/chains/robinhood-chain.svg",
  },
];

export default function ChainTabs() {
  const { selectedChain, setSelectedChain } = useChainStore();

  return (
    <div className="flex items-center gap-2 overflow-x-auto rounded-xl border border-[#292929] bg-[#101010] p-2">
      {CHAINS.map((chain) => {
        const active = selectedChain === chain.id;

        return (
          <button
            key={chain.id}
            type="button"
            onClick={() => setSelectedChain(chain.id)}
            className={[
              "flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition",
              active
                ? "border border-[#5A4718] bg-[#1A160C] text-[#F5C84C]"
                : "border border-transparent text-[#888] hover:bg-[#171717] hover:text-white",
            ].join(" ")}
          >
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-[#070707]">
              <img
                src={chain.icon}
                alt={chain.name}
                className="h-4 w-4 object-contain"
              />
            </span>

            <span>{chain.symbol}</span>

            {active && (
              <span className="h-1.5 w-1.5 rounded-full bg-[#F5C84C]" />
            )}
          </button>
        );
      })}
    </div>
  );
}