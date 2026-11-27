"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export type {
  ChainId,
} from "@/store/chainStore";

interface ChainStore {
  selectedChain: ChainId;
  setSelectedChain: (chain: ChainId) => void;
}

export const useChainStore = create<ChainStore>()(
  persist(
    (set) => ({
      selectedChain: "solana",

      setSelectedChain: (chain) => {
        set({
          selectedChain: chain,
        });
      },
    }),
    {
      name: "sentinel-chain-context",
    }
  )
);