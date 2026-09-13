// apps/web/lib/wallet/TransactionSigner.ts

import {
  Commitment,
  Connection,
  SendOptions,
  Transaction,
  VersionedTransaction,
} from "@solana/web3.js";

import WalletManager from "./WalletManager";

export type SolanaTransaction =
  | Transaction
  | VersionedTransaction;

export interface SimulationResult {
  success: boolean;
  logs: string[];
  unitsConsumed?: number;
  error?: unknown;
  returnData?: unknown;
}

export interface SendTransactionResult {
  signature: string;
  explorer: string;
}

function isVersionedTransaction(
  transaction: SolanaTransaction,
): transaction is VersionedTransaction {
  return transaction instanceof VersionedTransaction;
}

export default class TransactionSigner {
  private readonly wallet: WalletManager;
  private readonly connection: Connection;

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
    transaction: Transaction,
  ): Promise<Transaction> {
    return this.wallet.signTransaction(
      transaction,
    ) as Promise<Transaction>;
  }

  // ======================================================
  // Versioned Transaction
  // ======================================================

  async signVersioned(
    transaction: VersionedTransaction,
  ): Promise<VersionedTransaction> {
    return this.wallet.signTransaction(
      transaction,
    ) as Promise<VersionedTransaction>;
  }

  // ======================================================
  // Batch Sign
  // ======================================================

  async signAll(
    transactions: Transaction[],
  ): Promise<Transaction[]>;

  async signAll(
    transactions: VersionedTransaction[],
  ): Promise<VersionedTransaction[]>;

  async signAll(
    transactions: SolanaTransaction[],
  ): Promise<SolanaTransaction[]> {
    return this.wallet.signAllTransactions(
      transactions,
    ) as Promise<SolanaTransaction[]>;
  }

  // ======================================================
  // Sign Message
  // ======================================================

  async signMessage(
    message: string,
  ): Promise<Uint8Array> {
    return this.wallet.signMessage(
      message,
    ) as Promise<Uint8Array>;
  }

  // ======================================================
  // Simulate
  // ======================================================

  async simulate(
    transaction: SolanaTransaction,
  ): Promise<SimulationResult> {
    try {
      const result = isVersionedTransaction(
        transaction,
      )
        ? await this.connection.simulateTransaction(
            transaction,
            {
              sigVerify: false,
            },
          )
        : await this.connection.simulateTransaction(
            transaction,
          );

      return {
        success: result.value.err === null,
        logs: result.value.logs ?? [],
        unitsConsumed:
          result.value.unitsConsumed,
        error: result.value.err,
        returnData:
          result.value.returnData,
      };
    } catch (error) {
      return {
        success: false,
        logs: [],
        error,
      };
    }
  }

  // ======================================================
  // Send Transaction
  // ======================================================

  async send(
    transaction: SolanaTransaction,
    _options?: SendOptions,
  ): Promise<SendTransactionResult> {
    /*
     * WalletManager owns the actual wallet/provider send
     * operation. We intentionally keep the call compatible
     * with WalletManager.sendTransaction(transaction).
     *
     * `_options` remains part of this class API so callers
     * can pass SendOptions without breaking the interface.
     */
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
      explorer:
        this.explorer(signature),
    };
  }

  // ======================================================
  // Sign + Send
  // ======================================================

  async signAndSend(
    transaction: SolanaTransaction,
    options?: SendOptions,
  ): Promise<SendTransactionResult> {
    return this.send(
      transaction,
      options,
    );
  }

  // ======================================================
  // Jito Bundle
  // ======================================================

  async signBundle(
    bundle: VersionedTransaction[],
  ): Promise<VersionedTransaction[]> {
    return this.signAll(bundle) as Promise<
      VersionedTransaction[]
    >;
  }

  // ======================================================
  // Dry Run
  // ======================================================

  async dryRun(
    transaction: SolanaTransaction,
  ): Promise<SimulationResult> {
    return this.simulate(transaction);
  }

  // ======================================================
  // Estimate Fee
  // ======================================================

  async estimateFee(
    transaction: SolanaTransaction,
  ): Promise<number | null> {
    try {
      const message =
        isVersionedTransaction(transaction)
          ? transaction.message
          : transaction.compileMessage();

      const result =
        await this.connection.getFeeForMessage(
          message,
        );

      return result.value;
    } catch (error) {
      console.warn(
        "Failed to estimate transaction fee:",
        error,
      );

      return null;
    }
  }

  // ======================================================
  // Latest Blockhash
  // ======================================================

  async latestBlockhash() {
    return this.connection.getLatestBlockhash(
      "confirmed",
    );
  }

  // ======================================================
  // Wait Confirmation
  // ======================================================

  async waitConfirmation(
    signature: string,
    commitment: Commitment = "confirmed",
  ) {
    return this.connection.confirmTransaction(
      signature,
      commitment,
    );
  }

  // ======================================================
  // Verify Signature
  // ======================================================

  async verify(
    signature: string,
  ): Promise<boolean> {
    try {
      const transaction =
        await this.connection.getTransaction(
          signature,
          {
            commitment: "confirmed",
            maxSupportedTransactionVersion: 0,
          },
        );

      return transaction !== null;
    } catch (error) {
      console.warn(
        "Failed to verify transaction:",
        error,
      );

      return false;
    }
  }

  // ======================================================
  // Transaction Status
  // ======================================================

  async status(signature: string) {
    return this.connection.getSignatureStatus(
      signature,
    );
  }

  // ======================================================
  // Explorer URL
  // ======================================================

  explorer(signature: string): string {
    return `https://solscan.io/tx/${signature}`;
  }

  // ======================================================
  // Priority Fee
  // ======================================================

  async estimatePriorityFee() {
    /*
     * Placeholder until this is connected to
     * Helius/Jito/QuickNode priority-fee data.
     *
     * Values are micro-lamports per compute unit.
     */
    return {
      low: 1_000,
      medium: 5_000,
      high: 10_000,
      veryHigh: 25_000,
    };
  }

  // ======================================================
  // Compute Units
  // ======================================================

  async estimateComputeUnits(): Promise<number> {
    /*
     * Placeholder until compute-unit estimation is
     * connected to real transaction simulation.
     */
    return 200_000;
  }

  // ======================================================
  // MEV Protection
  // ======================================================

  async mevProtectedSend(
    transaction: SolanaTransaction,
    options?: SendOptions,
  ): Promise<SendTransactionResult> {
    /*
     * Placeholder for Jito bundle submission.
     *
     * For now this uses the standard wallet send path.
     */
    return this.send(
      transaction,
      options,
    );
  }
}
