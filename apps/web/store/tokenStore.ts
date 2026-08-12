import { create } from "zustand";

interface TokenStore {

  selectedToken: string;

  setToken:
    (token: string) => void;
}

export const useTokenStore =
  create<TokenStore>(
    (set) => ({

      selectedToken: "",

      setToken:
        (token) =>
          set({
            selectedToken: token
          })
    })
  );