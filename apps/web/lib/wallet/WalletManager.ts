// apps/web/lib/wallet/WalletManager.ts

import {
  Connection,
  PublicKey,
  Transaction,
  VersionedTransaction,
  clusterApiUrl,
} from "@solana/web3.js";

export type WalletType =
  | "phantom"
  | "backpack"
  | "solflare"
  | "unknown";

export interface WalletInfo {
  provider: WalletType;

  publicKey: PublicKey | null;

  connected: boolean;

  balance: number;

  network: string;
}

declare global {
  interface Window {
    phantom?: any;
    backpack?: any;
    solflare?: any;

    solana?: any;
  }
}

export default class WalletManager {
  private provider: any = null;

  private walletType: WalletType = "unknown";

  private connection: Connection;

  constructor(
    rpc?: string,
  ) {
    this.connection = new Connection(
      rpc ??
        clusterApiUrl("mainnet-beta"),
      "confirmed",
    );
  }

  // ===================================================
  // Detect Wallets
  // ===================================================

  installedWallets() {
    return {
      phantom:
        !!window.phantom?.solana ||
        !!window.solana?.isPhantom,

      backpack:
        !!window.backpack,

      solflare:
        !!window.solflare,
    };
  }

  // ===================================================
  // Wallet Detection
  // ===================================================

  detectProvider(
    wallet: WalletType,
  ) {
    switch (wallet) {
      case "phantom":
        return (
          window.phantom?.solana ??
          window.solana
        );

      case "backpack":
        return window.backpack;

      case "solflare":
        return window.solflare;

      default:
        return null;
    }
  }

  // ===================================================
  // Connect
  // ===================================================

  async connect(
    wallet: WalletType,
  ): Promise<WalletInfo> {
    this.provider =
      this.detectProvider(wallet);

    if (!this.provider)
      throw new Error(
        `${wallet} not installed`,
      );

    const response =
      await this.provider.connect();

    this.walletType = wallet;

    const balance =
      await this.getBalance(
        response.publicKey,
      );

    return {
      provider: wallet,

      publicKey:
        response.publicKey,

      connected: true,

      balance,

      network:
        await this.network(),
    };
  }

  // ===================================================
  // Disconnect
  // ===================================================

  async disconnect() {
    if (!this.provider) return;

    await this.provider.disconnect();

    this.provider = null;

    this.walletType =
      "unknown";
  }

  // ===================================================
  // Auto Reconnect
  // ===================================================

  async autoConnect(
    wallet: WalletType,
  ) {
    this.provider =
      this.detectProvider(wallet);

    if (!this.provider)
      return null;

    if (
      this.provider.connect
    ) {
      try {
        return await this.provider.connect(
          {
            onlyIfTrusted: true,
          },
        );
      } catch {
        return null;
      }
    }

    return null;
  }

  // ===================================================
  // Connected
  // ===================================================

  connected() {
    return (
      this.provider?.isConnected ??
      false
    );
  }

  // ===================================================
  // Public Key
  // ===================================================

  publicKey():
    | PublicKey
    | null {
    return (
      this.provider
        ?.publicKey ?? null
    );
  }

  // ===================================================
  // Address
  // ===================================================

  address():
    | string
    | null {
    return this.publicKey()?.toBase58() ??
      null;
  }

  // ===================================================
  // Balance
  // ===================================================

  async getBalance(
    key?: PublicKey,
  ) {
    const publicKey =
      key ??
      this.publicKey();

    if (!publicKey)
      return 0;

    const lamports =
      await this.connection.getBalance(
        publicKey,
      );

    return lamports /
      1_000_000_000;
  }

  // ===================================================
  // Network
  // ===================================================

  async network() {
    const version =
      await this.connection.getVersion();

    return version["solana-core"];
  }

  // ===================================================
  // Sign Message
  // ===================================================

  async signMessage(
    message: string,
  ) {
    if (
      !this.provider
        ?.signMessage
    )
      throw new Error(
        "Wallet does not support message signing.",
      );

    const encoded =
      new TextEncoder().encode(
        message,
      );

    return await this.provider.signMessage(
      encoded,
    );
  }

  // ===================================================
  // Sign Transaction
  // ===================================================

  async signTransaction(
    tx:
      | Transaction
      | VersionedTransaction,
  ) {
    if (
      !this.provider
        ?.signTransaction
    )
      throw new Error(
        "Wallet cannot sign transactions.",
      );

    return await this.provider.signTransaction(
      tx,
    );
  }

  // ===================================================
  // Sign All Transactions
  // ===================================================

  async signAllTransactions(
    txs:
      | Transaction[]
      | VersionedTransaction[],
  ) {
    if (
      !this.provider
        ?.signAllTransactions
    )
      throw new Error(
        "Wallet cannot batch sign.",
      );

    return await this.provider.signAllTransactions(
      txs,
    );
  }

  // ===================================================
  // Send Transaction
  // ===================================================

  async sendTransaction(
    tx:
      | Transaction
      | VersionedTransaction,
  ) {
    if (
      !this.provider
        ?.sendTransaction
    )
      throw new Error(
        "Wallet cannot send transaction.",
      );

    return await this.provider.sendTransaction(
      tx,
      this.connection,
    );
  }

  // ===================================================
  // Wallet Type
  // ===================================================

  walletTypeName() {
    return this.walletType;
  }

  // ===================================================
  // Explorer URL
  // ===================================================

  explorerUrl() {
    const address =
      this.address();

    if (!address)
      return null;

    return `https://solscan.io/account/${address}`;
  }

  // ===================================================
  // Current Wallet Info
  // ===================================================

  async walletInfo(): Promise<WalletInfo> {
    return {
      provider:
        this.walletType,

      publicKey:
        this.publicKey(),

      connected:
        this.connected(),

      balance:
        await this.getBalance(),

      network:
        await this.network(),
    };
  }

  // ===================================================
  // Event Listeners
  // ===================================================

  onConnect(
    callback: () => void,
  ) {
    this.provider?.on(
      "connect",
      callback,
    );
  }

  onDisconnect(
    callback: () => void,
  ) {
    this.provider?.on(
      "disconnect",
      callback,
    );
  }

  onAccountChanged(
    callback: (
      publicKey: PublicKey,
    ) => void,
  ) {
    this.provider?.on(
      "accountChanged",
      callback,
    );
  }

  // ===================================================
  // Destroy
  // ===================================================

  destroy() {
    this.provider = null;
  }
}