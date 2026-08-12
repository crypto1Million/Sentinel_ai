// apps/web/lib/wallet/PermissionManager.ts

import WalletManager from "./WalletManager";

export type WalletPermission =
  | "connect"
  | "disconnect"
  | "view_public_key"
  | "view_balance"
  | "sign_message"
  | "sign_transaction"
  | "sign_all_transactions"
  | "send_transaction";

export interface PermissionState {
  permission: WalletPermission;
  granted: boolean;
  lastUpdated: number;
}

export default class PermissionManager {
  private wallet: WalletManager;

  private permissions = new Map<
    WalletPermission,
    PermissionState
  >();

  constructor(wallet: WalletManager) {
    this.wallet = wallet;

    this.initialize();
  }

  // ======================================================
  // Initialize Default Permissions
  // ======================================================

  private initialize() {
    const defaults: WalletPermission[] = [
      "connect",
      "disconnect",
      "view_public_key",
      "view_balance",
      "sign_message",
      "sign_transaction",
      "sign_all_transactions",
      "send_transaction",
    ];

    defaults.forEach((permission) => {
      this.permissions.set(permission, {
        permission,
        granted: false,
        lastUpdated: Date.now(),
      });
    });
  }

  // ======================================================
  // Grant Permission
  // ======================================================

  grant(permission: WalletPermission) {
    this.permissions.set(permission, {
      permission,
      granted: true,
      lastUpdated: Date.now(),
    });
  }

  // ======================================================
  // Revoke Permission
  // ======================================================

  revoke(permission: WalletPermission) {
    this.permissions.set(permission, {
      permission,
      granted: false,
      lastUpdated: Date.now(),
    });
  }

  // ======================================================
  // Check Permission
  // ======================================================

  has(permission: WalletPermission): boolean {
    return (
      this.permissions.get(permission)
        ?.granted ?? false
    );
  }

  // ======================================================
  // Toggle Permission
  // ======================================================

  toggle(permission: WalletPermission) {
    if (this.has(permission)) {
      this.revoke(permission);
    } else {
      this.grant(permission);
    }
  }

  // ======================================================
  // Require Permission
  // ======================================================

  require(permission: WalletPermission) {
    if (!this.has(permission)) {
      throw new Error(
        `Permission "${permission}" denied.`,
      );
    }
  }

  // ======================================================
  // Grant All
  // ======================================================

  grantAll() {
    this.permissions.forEach((_, permission) => {
      this.grant(permission);
    });
  }

  // ======================================================
  // Revoke All
  // ======================================================

  revokeAll() {
    this.permissions.forEach((_, permission) => {
      this.revoke(permission);
    });
  }

  // ======================================================
  // Get All Permissions
  // ======================================================

  getPermissions(): PermissionState[] {
    return Array.from(
      this.permissions.values(),
    );
  }

  // ======================================================
  // Save Session Permissions
  // ======================================================

  saveSession() {
    localStorage.setItem(
      "sentinel_wallet_permissions",
      JSON.stringify(
        this.getPermissions(),
      ),
    );
  }

  // ======================================================
  // Load Session Permissions
  // ======================================================

  loadSession() {
    const raw =
      localStorage.getItem(
        "sentinel_wallet_permissions",
      );

    if (!raw) return;

    const stored: PermissionState[] =
      JSON.parse(raw);

    stored.forEach((permission) => {
      this.permissions.set(
        permission.permission,
        permission,
      );
    });
  }

  // ======================================================
  // Clear Session
  // ======================================================

  clearSession() {
    localStorage.removeItem(
      "sentinel_wallet_permissions",
    );

    this.revokeAll();
  }

  // ======================================================
  // Trusted Wallet
  // ======================================================

  markTrusted() {
    localStorage.setItem(
      "sentinel_wallet_trusted",
      "true",
    );
  }

  removeTrusted() {
    localStorage.removeItem(
      "sentinel_wallet_trusted",
    );
  }

  isTrusted(): boolean {
    return (
      localStorage.getItem(
        "sentinel_wallet_trusted",
      ) === "true"
    );
  }

  // ======================================================
  // Auto Connect Allowed
  // ======================================================

  allowAutoReconnect() {
    localStorage.setItem(
      "sentinel_auto_connect",
      "true",
    );
  }

  disableAutoReconnect() {
    localStorage.removeItem(
      "sentinel_auto_connect",
    );
  }

  canAutoReconnect(): boolean {
    return (
      localStorage.getItem(
        "sentinel_auto_connect",
      ) === "true"
    );
  }

  // ======================================================
  // Wallet Connected
  // ======================================================

  async isWalletConnected() {
    return this.wallet.connected();
  }

  // ======================================================
  // Permission Summary
  // ======================================================

  summary() {
    return {
      walletConnected:
        this.wallet.connected(),

      trusted: this.isTrusted(),

      autoReconnect:
        this.canAutoReconnect(),

      permissions:
        this.getPermissions(),
    };
  }

  // ======================================================
  // Reset Everything
  // ======================================================

  reset() {
    this.clearSession();

    this.removeTrusted();

    this.disableAutoReconnect();

    this.revokeAll();
  }
}