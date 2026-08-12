// apps/web/components/wallet/WalletProvider.tsx

"use client";

import React, {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  Connection,
  clusterApiUrl,
  PublicKey,
} from "@solana/web3.js";

import WalletManager, {
  WalletType,
  WalletInfo,
} from "@/lib/wallet/WalletManager";

import PermissionManager from "@/lib/wallet/PermissionManager";

import TransactionSigner from "@/lib/wallet/TransactionSigner";

interface WalletContextType {
  walletManager: WalletManager;

  permissionManager: PermissionManager;

  signer: TransactionSigner;

  wallet: WalletInfo | null;

  connected: boolean;

  connecting: boolean;

  publicKey: PublicKey | null;

  address: string | null;

  balance: number;

  provider: WalletType | null;

  connect: (
    provider: WalletType,
  ) => Promise<void>;

  disconnect: () => Promise<void>;

  refresh: () => Promise<void>;

  signMessage: (
    message: string,
  ) => Promise<any>;

  signTransaction: (
    transaction: any,
  ) => Promise<any>;
}

const WalletContext =
  createContext<WalletContextType | null>(
    null,
  );

interface Props {
  children: React.ReactNode;
}

export function WalletProvider({
  children,
}: Props) {
  const connection = useMemo(
    () =>
      new Connection(
        clusterApiUrl(
          "mainnet-beta",
        ),
      ),
    [],
  );

  const walletManager = useMemo(
    () => new WalletManager(),
    [],
  );

  const permissionManager =
    useMemo(
      () =>
        new PermissionManager(
          walletManager,
        ),
      [walletManager],
    );

  const signer = useMemo(
    () =>
      new TransactionSigner(
        walletManager,
        connection,
      ),
    [walletManager, connection],
  );

  const [wallet, setWallet] =
    useState<WalletInfo | null>(
      null,
    );

  const [connecting, setConnecting] =
    useState(false);

  // ===================================================
  // Refresh Wallet
  // ===================================================

  const refresh = async () => {
    if (
      !walletManager.connected()
    )
      return;

    const info =
      await walletManager.walletInfo();

    setWallet(info);
  };

  // ===================================================
  // Connect
  // ===================================================

  const connect = async (
    provider: WalletType,
  ) => {
    try {
      setConnecting(true);

      const info =
        await walletManager.connect(
          provider,
        );

      permissionManager.grantAll();

      permissionManager.markTrusted();

      permissionManager.allowAutoReconnect();

      permissionManager.saveSession();

      setWallet(info);
    } finally {
      setConnecting(false);
    }
  };

  // ===================================================
  // Disconnect
  // ===================================================

  const disconnect =
    async () => {
      await walletManager.disconnect();

      permissionManager.reset();

      setWallet(null);
    };

  // ===================================================
  // Sign Message
  // ===================================================

  const signMessage =
    async (
      message: string,
    ) => {
      permissionManager.require(
        "sign_message",
      );

      return signer.signMessage(
        message,
      );
    };

  // ===================================================
  // Sign Transaction
  // ===================================================

  const signTransaction =
    async (
      transaction: any,
    ) => {
      permissionManager.require(
        "sign_transaction",
      );

      return signer.signLegacy(
        transaction,
      );
    };

  // ===================================================
  // Auto Connect
  // ===================================================

  useEffect(() => {
    permissionManager.loadSession();

    if (
      !permissionManager.canAutoReconnect()
    )
      return;

    const reconnect =
      async () => {
        const installed =
          walletManager.installedWallets();

        if (
          installed.phantom
        ) {
          const result =
            await walletManager.autoConnect(
              "phantom",
            );

          if (result) {
            await refresh();
            return;
          }
        }

        if (
          installed.backpack
        ) {
          const result =
            await walletManager.autoConnect(
              "backpack",
            );

          if (result) {
            await refresh();
            return;
          }
        }

        if (
          installed.solflare
        ) {
          const result =
            await walletManager.autoConnect(
              "solflare",
            );

          if (result) {
            await refresh();
          }
        }
      };

      reconnect();
    }, []);

  // ===================================================
  // Wallet Events
  // ===================================================

  useEffect(() => {
    walletManager.onConnect(
      refresh,
    );

    walletManager.onDisconnect(
      () => {
        setWallet(null);
      },
    );

    walletManager.onAccountChanged(
      refresh,
    );
  }, []);

  return (
    <WalletContext.Provider
      value={{
        walletManager,

        permissionManager,

        signer,

        wallet,

        connected:
          wallet?.connected ??
          false,

        connecting,

        publicKey:
          wallet?.publicKey ??
          null,

        address:
          wallet?.publicKey?.toBase58() ??
          null,

        balance:
          wallet?.balance ?? 0,

        provider:
          wallet?.provider ??
          null,

        connect,

        disconnect,

        refresh,

        signMessage,

        signTransaction,
      }}
    >
      {children}
    </WalletContext.Provider>
  );
}

// =======================================================
// Hook
// =======================================================

export function useWallet() {
  const context =
    useContext(
      WalletContext,
    );

  if (!context)
    throw new Error(
      "useWallet must be used inside WalletProvider",
    );

  return context;
}