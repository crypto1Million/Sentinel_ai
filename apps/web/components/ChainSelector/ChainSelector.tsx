"use client";

import { useState } from "react";
import {
  Check,
  ChevronDown,
} from "lucide-react";

import {
  useChainStore,
  type ChainId,
} from "@/store/chainStore";

type ChainOption = {
  id: ChainId;
  name: string;
  symbol: string;
  iconUrl: string;
};

type EvmNetwork = {
  chainId: number;
  chainName: string;
  nativeCurrency: {
    name: string;
    symbol: string;
    decimals: number;
  };
  rpcUrls: string[];
  blockExplorerUrls: string[];
};

const CHAINS: ChainOption[] = [
  {
    id: "solana",
    name: "Solana",
    symbol: "SOL",
    iconUrl: "https://cdn.simpleicons.org/solana",
  },
  {
    id: "base",
    name: "Base",
    symbol: "ETH",
    iconUrl: "https://cdn.simpleicons.org/base",
  },
  {
    id: "ethereum",
    name: "Ethereum",
    symbol: "ETH",
    iconUrl: "https://cdn.simpleicons.org/ethereum",
  },
  {
    id: "bnb",
    name: "BNB Chain",
    symbol: "BNB",
    iconUrl: "https://cdn.simpleicons.org/binance",
  },
  {
    id: "robinhood",
    name: "Robinhood Chain",
    symbol: "HOOD",
    iconUrl: "https://cdn.simpleicons.org/robinhood",
  }
];

const EVM_NETWORKS: Partial<
  Record<Exclude<ChainId, "solana">, EvmNetwork>
> = {
  base: {
    chainId: 8453,
    chainName: "Base",
    nativeCurrency: {
      name: "Ether",
      symbol: "ETH",
      decimals: 18,
    },
    rpcUrls: ["https://mainnet.base.org"],
    blockExplorerUrls: ["https://basescan.org"],
  },

  ethereum: {
    chainId: 1,
    chainName: "Ethereum Mainnet",
    nativeCurrency: {
      name: "Ether",
      symbol: "ETH",
      decimals: 18,
    },
    rpcUrls: ["https://ethereum.publicnode.com"],
    blockExplorerUrls: ["https://etherscan.io"],
  },

  bnb: {
    chainId: 56,
    chainName: "BNB Smart Chain",
    nativeCurrency: {
      name: "BNB",
      symbol: "BNB",
      decimals: 18,
    },
    rpcUrls: ["https://bsc-dataseed.binance.org"],
    blockExplorerUrls: ["https://bscscan.com"],
  },

  robinhood: {
    chainId: 1,
    chainName: "Ethereum Mainnet",
    nativeCurrency: {
      name: "Ether",
      symbol: "ETH",
      decimals: 18,
    },
    rpcUrls: ["https://ethereum.publicnode.com"],
    blockExplorerUrls: ["https://etherscan.io"],
  },
};

function toHexChainId(
  chainId: number
): string {
  return `0x${chainId.toString(16)}`;
}

export default function ChainSelector() {
  const {
    selectedChain,
    setSelectedChain,
  } = useChainStore();

  const [open, setOpen] =
    useState(false);

  const activeChain =
    CHAINS.find(
      (chain) =>
        chain.id === selectedChain
    ) ?? CHAINS[0];

  async function switchChain(
    chain: ChainId
  ) {
    setSelectedChain(chain);

    if (chain === "solana") {
      setOpen(false);
      return;
    }

    const network =
      EVM_NETWORKS[chain];

    if (!network) {
      setOpen(false);
      return;
    }

    if (typeof window === "undefined") {
      setOpen(false);
      return;
    }

    const ethereum = (
      window as Window & {
        ethereum?: {
          request?: (args: {
            method: string;
            params?: unknown[];
          }) => Promise<unknown>;
        };
      }
    ).ethereum;

    if (!ethereum?.request) {
      console.warn(
        "No EVM wallet provider detected."
      );

      setOpen(false);
      return;
    }

    const hexChainId =
      toHexChainId(
        network.chainId
      );

    try {
      await ethereum.request({
        method:
          "wallet_switchEthereumChain",
        params: [
          {
            chainId: hexChainId,
          },
        ],
      });
    } catch (error) {
      const code =
        typeof error === "object" &&
        error !== null &&
        "code" in error
          ? (
              error as {
                code?: number;
              }
            ).code
          : undefined;

      if (code === 4902) {
        try {
          await ethereum.request({
            method:
              "wallet_addEthereumChain",
            params: [
              {
                chainId: hexChainId,
                chainName:
                  network.chainName,
                nativeCurrency:
                  network.nativeCurrency,
                rpcUrls:
                  network.rpcUrls,
                blockExplorerUrls:
                  network.blockExplorerUrls,
              },
            ],
          });
        } catch (addError) {
          console.error(
            "Failed to add network:",
            addError
          );
        }
      } else {
        console.error(
          "Failed to switch network:",
          error
        );
      }
    }

    setOpen(false);
  }

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() =>
          setOpen(
            (value) => !value
          )
        }
        className="flex h-11 items-center gap-2 rounded-full border border-zinc-800 bg-[#111318] px-3 text-sm text-white transition hover:border-amber-500/40"
      >
        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-zinc-900">
          <img
            src={activeChain.iconUrl}
            alt={`${activeChain.name} logo`}
            className="h-4 w-4 object-contain"
          />
        </span>

        <span className="font-medium">
          {activeChain.symbol}
        </span>

        <ChevronDown
          size={15}
          className={`text-zinc-500 transition-transform ${
            open
              ? "rotate-180"
              : ""
          }`}
        />
      </button>

      {open && (
        <div className="absolute right-0 top-full z-50 mt-2 w-64 overflow-hidden rounded-xl border border-zinc-800 bg-[#111318] shadow-2xl">
          <div className="border-b border-zinc-800 px-4 py-3">
            <div className="text-sm font-semibold text-white">
              Select Chain
            </div>

            <div className="mt-1 text-xs text-zinc-500">
              Switch Sentinel's active blockchain
            </div>
          </div>

          <div className="p-2">
            {CHAINS.map(
              (chain) => {
                const selected =
                  chain.id ===
                  selectedChain;

                return (
                  <button
                    key={chain.id}
                    type="button"
                    onClick={() =>
                      void switchChain(
                        chain.id
                      )
                    }
                    className={`flex w-full items-center gap-3 rounded-lg px-3 py-3 text-left transition ${
                      selected
                        ? "bg-zinc-800"
                        : "hover:bg-zinc-800/70"
                    }`}
                  >
                    <span className="flex h-9 w-9 items-center justify-center rounded-full bg-zinc-900">
                      <img
                        src={chain.iconUrl}
                        alt={`${chain.name} logo`}
                        className="h-5 w-5 object-contain"
                      />
                    </span>

                    <span className="min-w-0 flex-1">
                      <span className="block truncate text-sm font-medium text-white">
                        {chain.name}
                      </span>

                      <span className="block text-xs text-zinc-500">
                        {chain.symbol}
                      </span>
                    </span>

                    {selected && (
                      <Check
                        size={17}
                        className="text-amber-400"
                      />
                    )}
                  </button>
                );
              }
            )}
          </div>
        </div>
      )}
    </div>
  );
}