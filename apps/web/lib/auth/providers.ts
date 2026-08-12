// apps/web/lib/auth/providers.ts

export interface AuthProvider {
  id: string;

  name: string;

  icon: string;

  description: string;

  color: string;

  enabled: boolean;

  loginUrl: string;
}

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://localhost:8000";

// ======================================================
// Authentication Providers
// ======================================================

export const AUTH_PROVIDERS: AuthProvider[] = [
  {
    id: "google",
    name: "Google",
    icon: "/icons/google.svg",
    description: "Continue with Google",
    color: "#ffffff",
    enabled: true,
    loginUrl: `${API_URL}/auth/google`,
  },

  {
    id: "discord",
    name: "Discord",
    icon: "/icons/discord.svg",
    description: "Continue with Discord",
    color: "#5865F2",
    enabled: true,
    loginUrl: `${API_URL}/auth/discord`,
  },

  {
    id: "phantom",
    name: "Phantom",
    icon: "/icons/phantom.svg",
    description: "Connect Phantom Wallet",
    color: "#AB9FF2",
    enabled: true,
    loginUrl: "/wallet/phantom",
  },

  {
    id: "backpack",
    name: "Backpack",
    icon: "/icons/backpack.svg",
    description: "Connect Backpack Wallet",
    color: "#19C37D",
    enabled: true,
    loginUrl: "/wallet/backpack",
  },

  {
    id: "solflare",
    name: "Solflare",
    icon: "/icons/solflare.svg",
    description: "Connect Solflare Wallet",
    color: "#FC8B36",
    enabled: true,
    loginUrl: "/wallet/solflare",
  },
];

// ======================================================
// Lookup Helpers
// ======================================================

export function getProvider(
  id: string,
): AuthProvider | undefined {
  return AUTH_PROVIDERS.find(
    (provider) => provider.id === id,
  );
}

export function getEnabledProviders() {
  return AUTH_PROVIDERS.filter(
    (provider) => provider.enabled,
  );
}

export function isProviderEnabled(
  id: string,
): boolean {
  const provider = getProvider(id);

  return provider?.enabled ?? false;
}

// ======================================================
// OAuth Providers
// ======================================================

export const OAUTH_PROVIDERS =
  AUTH_PROVIDERS.filter(
    (provider) =>
      provider.id === "google" ||
      provider.id === "discord",
  );

// ======================================================
// Wallet Providers
// ======================================================

export const WALLET_PROVIDERS =
  AUTH_PROVIDERS.filter(
    (provider) =>
      provider.id === "phantom" ||
      provider.id === "backpack" ||
      provider.id === "solflare",
  );

// ======================================================
// Navigation
// ======================================================

export function redirectToProvider(
  providerId: string,
) {
  const provider = getProvider(providerId);

  if (!provider) {
    throw new Error(
      `Unknown provider: ${providerId}`,
    );
  }

  window.location.href =
    provider.loginUrl;
}

// ======================================================
// Labels
// ======================================================

export function providerDisplayName(
  providerId: string,
): string {
  return (
    getProvider(providerId)?.name ??
    providerId
  );
}