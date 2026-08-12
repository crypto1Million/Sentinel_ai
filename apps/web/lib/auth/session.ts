// apps/web/lib/auth/session.ts

import {
  api,
  getAccessToken,
  getRefreshToken,
  refreshToken,
  clearTokens,
  tokenExpired,
} from "./auth";

export interface Session {
  authenticated: boolean;

  accessToken: string | null;

  refreshToken: string | null;

  user: any | null;
}

let currentUser: any | null = null;


// ======================================================
// Session
// ======================================================

export async function getSession(): Promise<Session> {
  const access = getAccessToken();
  const refresh = getRefreshToken();

  return {
    authenticated: !!access,
    accessToken: access,
    refreshToken: refresh,
    user: currentUser,
  };
}


// ======================================================
// Current User
// ======================================================

export async function loadUser() {
  try {
    const response = await api.get("/auth/me");

    currentUser = response.data;

    return currentUser;
  } catch {
    return null;
  }
}


export function getCurrentUser() {
  return currentUser;
}


// ======================================================
// Session Validation
// ======================================================

export async function validateSession() {
  const access = getAccessToken();

  if (!access) return false;

  if (!tokenExpired()) return true;

  try {
    await refreshToken();

    return true;
  } catch {
    destroySession();

    return false;
  }
}


// ======================================================
// Session Refresh
// ======================================================

export async function refreshSession() {
  return refreshToken();
}


// ======================================================
// Destroy Session
// ======================================================

export function destroySession() {
  clearTokens();

  currentUser = null;
}


// ======================================================
// Initialize Session
// ======================================================

export async function initializeSession() {
  const valid = await validateSession();

  if (!valid) return null;

  return await loadUser();
}


// ======================================================
// Authorization
// ======================================================

export function hasRole(
  role: string,
): boolean {

  if (!currentUser) return false;

  return (
    currentUser.roles?.includes(role) ??
    false
  );
}


export function hasPermission(
  permission: string,
): boolean {

  if (!currentUser) return false;

  return (
    currentUser.permissions?.includes(
      permission,
    ) ?? false
  );
}


// ======================================================
// Wallet
// ======================================================

export function connectedWallet() {
  return currentUser?.wallet ?? null;
}


// ======================================================
// Login Provider
// ======================================================

export function loginProvider() {
  return currentUser?.provider ?? null;
}


// ======================================================
// Auto Refresh Loop
// ======================================================

let refreshTimer: NodeJS.Timeout | null = null;

export function startSessionRefresh() {
  stopSessionRefresh();

  refreshTimer = setInterval(
    async () => {
      try {
        if (tokenExpired()) {
          await refreshToken();
        }
      } catch {
        destroySession();
      }
    },
    1000 * 60 * 5, // every 5 minutes
  );
}


export function stopSessionRefresh() {
  if (refreshTimer) {
    clearInterval(refreshTimer);

    refreshTimer = null;
  }
}


// ======================================================
// Route Guard
// ======================================================

export async function requireAuth() {
  const valid = await validateSession();

  if (!valid) {
    window.location.href = "/login";
  }
}


// ======================================================
// Admin Guard
// ======================================================

export async function requireAdmin() {
  await requireAuth();

  if (!hasRole("admin")) {
    window.location.href = "/";
  }
}


// ======================================================
// Permission Guard
// ======================================================

export async function requirePermission(
  permission: string,
) {
  await requireAuth();

  if (!hasPermission(permission)) {
    window.location.href = "/";
  }
}