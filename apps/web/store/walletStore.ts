import { create } from "zustand";

interface WalletStore {

  selectedWallet: string;

  setWallet:
    (wallet: string) => void;
}

export const useWalletStore =
  create<WalletStore>(
    (set) => ({

      selectedWallet: "",

      setWallet:
        (wallet) =>
          set({
            selectedWallet: wallet
          })
    })
  );