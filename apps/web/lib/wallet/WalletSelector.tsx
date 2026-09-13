"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Check,
  ChevronDown,
  Wallet,
  ExternalLink,
} from "lucide-react";

type WalletType =
  | "phantom"
  | "backpack"
  | "solflare"
  | "unknown";

type WalletOption = {
  id: WalletType;
  name: string;
  description: string;
  installUrl: string;
};

type WalletProvider = {
  isPhantom?: boolean;
  isBackpack?: boolean;
  isSolflare?: boolean;
  publicKey?: {
    toString: () => string;
  } | null;
  connect?: () => Promise<unknown>;
  disconnect?: () => Promise<void>;
};

const WALLET_OPTIONS: WalletOption[] = [
  {
    id: "phantom",
    name: "Phantom",
    description: "Solana wallet",
    installUrl: "https://phantom.app/",
  },
  {
    id: "backpack",
    name: "Backpack",
    description: "Solana wallet",
    installUrl: "https://www.backpack.app/",
  },
  {
    id: "solflare",
    name: "Solflare",
    description: "Solana wallet",
    installUrl: "https://solflare.com/",
  },
];

type InstalledWalletType =
  | "phantom"
  | "backpack"
  | "solflare";

type InstalledWallets = Record<
  InstalledWalletType,
  boolean
>;

function isInstalledWalletType(
  id: WalletType
): id is InstalledWalletType {
  return (
    id === "phantom" ||
    id === "backpack" ||
    id === "solflare"
  );
}

function getWalletProviders() {
  if (
    typeof window === "undefined"
  ) {
    return {
      phantom: undefined,
      backpack: undefined,
      solflare: undefined,
    };
  }

  const win = window as Window & {
    solana?: WalletProvider;
    backpack?: WalletProvider;
    solflare?: WalletProvider;
  };

  return {
    phantom:
      win.solana?.isPhantom
        ? win.solana
        : undefined,

    backpack:
      win.backpack?.isBackpack
        ? win.backpack
        : undefined,

    solflare:
      win.solflare?.isSolflare
        ? win.solflare
        : undefined,
  };
}

export default function WalletSelector() {
  const [open, setOpen] =
    useState(false);

  const [selectedWallet, setSelectedWallet] =
    useState<WalletType>("unknown");

  const [connectedAddress, setConnectedAddress] =
    useState<string | null>(null);

  const [installed, setInstalled] =
    useState<InstalledWallets>({
      phantom: false,
      backpack: false,
      solflare: false,
    });

  useEffect(() => {
    const providers =
      getWalletProviders();

    setInstalled({
      phantom:
        Boolean(providers.phantom),
      backpack:
        Boolean(providers.backpack),
      solflare:
        Boolean(providers.solflare),
    });
  }, []);

  const activeWallet = useMemo(() => {
    return WALLET_OPTIONS.find(
      (wallet) =>
        wallet.id === selectedWallet
    );
  }, [selectedWallet]);

  async function connectWallet(
    wallet: WalletOption
  ) {
    if (
      !isInstalledWalletType(wallet.id)
    ) {
      return;
    }

    const providers =
      getWalletProviders();

    const provider =
      providers[wallet.id];

    if (!provider) {
      window.open(
        wallet.installUrl,
        "_blank",
        "noopener,noreferrer"
      );

      return;
    }

    try {
      if (!provider.connect) {
        console.error(
          `${wallet.name} provider does not support connect().`
        );

        return;
      }

      const result =
        await provider.connect();

      const publicKey =
        provider.publicKey?.toString?.() ??
        null;

      setSelectedWallet(
        wallet.id
      );

      setConnectedAddress(
        publicKey
      );

      setOpen(false);

      console.log(
        `${wallet.name} connected`,
        {
          result,
          publicKey,
        }
      );
    } catch (error) {
      console.error(
        `Failed to connect ${wallet.name}:`,
        error
      );
    }
  }

  async function disconnectWallet() {
    if (
      !isInstalledWalletType(
        selectedWallet
      )
    ) {
      setSelectedWallet(
        "unknown"
      );

      setConnectedAddress(
        null
      );

      return;
    }

    const providers =
      getWalletProviders();

    const provider =
      providers[selectedWallet];

    try {
      if (provider?.disconnect) {
        await provider.disconnect();
      }
    } catch (error) {
      console.error(
        "Failed to disconnect wallet:",
        error
      );
    } finally {
      setSelectedWallet(
        "unknown"
      );

      setConnectedAddress(
        null
      );

      setOpen(false);
    }
  }

  function handleWalletClick(
    wallet: WalletOption
  ) {
    if (
      selectedWallet === wallet.id &&
      connectedAddress
    ) {
      void disconnectWallet();
      return;
    }

    void connectWallet(wallet);
  }

  function formatAddress(
    address: string | null
  ) {
    if (!address) {
      return null;
    }

    if (address.length <= 12) {
      return address;
    }

    return `${address.slice(
      0,
      6
    )}...${address.slice(-4)}`;
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
        className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-[#11161d] px-3 py-2 text-sm text-white transition hover:border-amber-500/40"
      >
        <Wallet
          size={17}
          className="text-amber-400"
        />

        <span className="max-w-[100px] truncate">
          {activeWallet?.name ??
            "Connect Wallet"}
        </span>

        {connectedAddress && (
          <span className="text-xs text-zinc-500">
            {formatAddress(
              connectedAddress
            )}
          </span>
        )}

        <ChevronDown
          size={16}
          className={`text-zinc-500 transition-transform ${
            open
              ? "rotate-180"
              : ""
          }`}
        />
      </button>

      {open && (
        <div className="absolute right-0 top-full z-50 mt-2 w-72 overflow-hidden rounded-xl border border-zinc-800 bg-[#11161d] shadow-2xl">
          <div className="border-b border-zinc-800 px-4 py-3">
            <div className="text-sm font-semibold text-white">
              Wallet
            </div>

            <div className="mt-1 text-xs text-zinc-500">
              Connect your Solana wallet
            </div>
          </div>

          <div className="p-2">
            {WALLET_OPTIONS.map(
              (wallet) => {
                const isInstalledWallet =
                  isInstalledWalletType(
                    wallet.id
                  );

                const isInstalled =
                  wallet.id === "phantom"
                    ? installed.phantom
                    : wallet.id === "backpack"
                      ? installed.backpack
                      : wallet.id === "solflare"
                        ? installed.solflare
                        : false;

                const isSelected =
                  selectedWallet ===
                  wallet.id;

                const isConnected =
                  isSelected &&
                  Boolean(
                    connectedAddress
                  );

                return (
                  <button
                    key={wallet.id}
                    type="button"
                    onClick={() =>
                      handleWalletClick(
                        wallet
                      )
                    }
                    className="flex w-full items-center gap-3 rounded-lg px-3 py-3 text-left transition hover:bg-zinc-800"
                  >
                    <div className="flex h-9 w-9 items-center justify-center rounded-full border border-zinc-700 bg-zinc-900">
                      {wallet.id ===
                      "phantom" ? (
                        <span className="text-sm font-bold text-white">
                          P
                        </span>
                      ) : wallet.id ===
                        "backpack" ? (
                        <span className="text-sm font-bold text-white">
                          B
                        </span>
                      ) : (
                        <span className="text-sm font-bold text-white">
                          S
                        </span>
                      )}
                    </div>

                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="truncate text-sm font-medium text-white">
                          {wallet.name}
                        </span>

                        {isInstalled && (
                          <span className="text-[10px] uppercase tracking-wide text-green-400">
                            Installed
                          </span>
                        )}
                      </div>

                      <div className="truncate text-xs text-zinc-500">
                        {isConnected
                          ? formatAddress(
                              connectedAddress
                            )
                          : wallet.description}
                      </div>
                    </div>

                    {isConnected ? (
                      <Check
                        size={17}
                        className="text-green-400"
                      />
                    ) : isInstalled ? (
                      <span className="text-xs text-zinc-500">
                        Connect
                      </span>
                    ) : (
                      <ExternalLink
                        size={15}
                        className="text-zinc-600"
                      />
                    )}
                  </button>
                );
              }
            )}
          </div>

          {connectedAddress && (
            <div className="border-t border-zinc-800 p-3">
              <button
                type="button"
                onClick={() =>
                  void disconnectWallet()
                }
                className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2 text-xs font-medium text-zinc-300 transition hover:border-red-500/40 hover:text-red-400"
              >
                Disconnect Wallet
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}