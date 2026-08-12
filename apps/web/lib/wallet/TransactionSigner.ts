// apps/web/lib/wallet/TransactionSigner.ts

import {
  Connection,
  Transaction,
  VersionedTransaction,
  SimulatedTransactionResponse,
  SendOptions,
  Commitment,
} from "@solana/web3.js";

import WalletManager from "./WalletManager";

export interface SimulationResult {
  success: boolean;

  logs: string[];

  unitsConsumed?: number;

  error?: any;
}

export interface SendTransactionResult {
  signature: string;

  explorer: string;
}

export default class TransactionSigner {
  private wallet: WalletManager;

  private connection: Connection;

  constructor(
    wallet: WalletManager,
    connection: Connection,
  ) {
    this.wallet = wallet;
    this.connection = connection;
  }

  // ======================================================
  // Legacy Transaction
  // ======================================================

  async signLegacy(
    tx: Transaction,
  ): Promise<Transaction> {
    return await this.wallet.signTransaction(
      tx,
    );
  }

  // ======================================================
  // Versioned Transaction
  // ======================================================

  async signVersioned(
    tx: VersionedTransaction,
  ): Promise<VersionedTransaction> {
    return await this.wallet.signTransaction(
      tx,
    );
  }

  // ======================================================
  // Batch Sign
  // ======================================================

  async signAll(
    transactions:
      | Transaction[]
      | VersionedTransaction[],
  ) {
    return await this.wallet.signAllTransactions(
      transactions,
    );
  }

  // ======================================================
  // Sign Message
  // ======================================================

  async signMessage(
    message: string,
  ) {
    return await this.wallet.signMessage(
      message,
    );
  }

  // ======================================================
  // Simulate
  // ======================================================

  async simulate(
    transaction:
      | Transaction
      | VersionedTransaction,
  ): Promise<SimulationResult> {
    try {
      const result =
        await this.connection.simulateTransaction(
          transaction,
        );

      return {
        success:
          result.value.err === null,

        logs:
          result.value.logs ?? [],

        unitsConsumed:
          result.value.unitsConsumed,

        error:
          result.value.err,
      };
    } catch (err) {
      return {
        success: false,
        logs: [],
        error: err,
      };
    }
  }

  // ======================================================
  // Send Transaction
  // ======================================================

  async send(
    transaction:
      | Transaction
      | VersionedTransaction,

    options?: SendOptions,
  ): Promise<SendTransactionResult> {
    const signature =
      await this.wallet.sendTransaction(
        transaction,
      );

    await this.connection.confirmTransaction(
      signature,
      "confirmed",
    );

    return {
      signature,

      explorer: `https://solscan.io/tx/${signature}`,
    };
  }

  // ======================================================
  // Sign + Send
  // ======================================================

  async signAndSend(
    transaction:
      | Transaction
      | VersionedTransaction,
  ) {
    return await this.send(
      transaction,
    );
  }

  // ======================================================
  // Jito Bundle (Placeholder)
  // ======================================================

  async signBundle(
    bundle: VersionedTransaction[],
  ) {
    return await this.signAll(
      bundle,
    );
  }

  // ======================================================
  // Dry Run
  // ======================================================

  async dryRun(
    tx:
      | Transaction
      | VersionedTransaction,
  ) {
    return await this.simulate(
      tx,
    );
  }

  // ======================================================
  // Estimate Fee
  // ======================================================

  async estimateFee(
    transaction:
      | Transaction
      | VersionedTransaction,
  ) {
    try {
      const fee =
        await this.connection.getFeeForMessage(
          transaction.message,
        );

      return fee.value;
    } catch {
      return null;
    }
  }

  // ======================================================
  // Latest Blockhash
  // ======================================================

  async latestBlockhash() {
    return await this.connection.getLatestBlockhash();
  }

  // ======================================================
  // Wait Confirmation
  // ======================================================

  async waitConfirmation(
    signature: string,
    commitment: Commitment = "confirmed",
  ) {
    return await this.connection.confirmTransaction(
      signature,
      commitment,
    );
  }

  // ======================================================
  // Verify Signature
  // ======================================================

  async verify(
    signature: string,
  ) {
    const tx =
      await this.connection.getTransaction(
        signature,
      );

    return tx !== null;
  }

  // ======================================================
  // Transaction Status
  // ======================================================

  async status(
    signature: string,
  ) {
    return await this.connection.getSignatureStatus(
      signature,
    );
  }

  // ======================================================
  // Explorer URL
  // ======================================================

  explorer(
    signature: string,
  ) {
    return `https://solscan.io/tx/${signature}`;
  }

  // ======================================================
  // Priority Fee (Phase 14 Ready)
  // ======================================================

  async estimatePriorityFee() {
    // Placeholder for Jito/Priority Fee API

    return {
      low: 1000,

      medium: 5000,

      high: 10000,

      veryHigh: 25000,
    };
  }

  // ======================================================
  // Compute Units (Placeholder)
  // ======================================================

  async estimateComputeUnits() {
    return 200000;
  }

  // ======================================================
  // MEV Protection (Placeholder)
  // ======================================================

  async mevProtectedSend(
    tx:
      | Transaction
      | VersionedTransaction,
  ) {
    // Will be integrated with Jito Bundle API
    return await this.send(tx);
  }
}