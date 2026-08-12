// apps/web/lib/auth/auth.ts

import axios from "axios";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";


// ======================================================
// Types
// ======================================================

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: string;

  username?: string;

  email?: string;

  wallet?: string;

  avatar?: string;

  roles?: string[];

  permissions?: string[];
}


// ======================================================
// Storage
// ======================================================

const ACCESS_TOKEN_KEY = "sentinel_access_token";

const REFRESH_TOKEN_KEY = "sentinel_refresh_token";


// ======================================================
// Token Helpers
// ======================================================

export function getAccessToken() {
  return localStorage.getItem(
    ACCESS_TOKEN_KEY,
  );
}

export function getRefreshToken() {
  return localStorage.getItem(
    REFRESH_TOKEN_KEY,
  );
}

export function saveTokens(
  access: string,
  refresh: string,
) {
  localStorage.setItem(
    ACCESS_TOKEN_KEY,
    access,
  );

  localStorage.setItem(
    REFRESH_TOKEN_KEY,
    refresh,
  );
}

export function clearTokens() {
  localStorage.removeItem(
    ACCESS_TOKEN_KEY,
  );

  localStorage.removeItem(
    REFRESH_TOKEN_KEY,
  );
}


// ======================================================
// Axios
// ======================================================

export const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  },
);


// ======================================================
// Login
// ======================================================

export async function login(
  email: string,
  password: string,
) {
  const response =
    await api.post<LoginResponse>(
      "/auth/login",
      {
        email,
        password,
      },
    );

  saveTokens(
    response.data.access_token,
    response.data.refresh_token,
  );

  return response.data;
}


// ======================================================
// Register
// ======================================================

export async function register(
  username: string,
  email: string,
  password: string,
) {
  return api.post(
    "/auth/register",
    {
      username,
      email,
      password,
    },
  );
}


// ======================================================
// Logout
// ======================================================

export function logout() {
  clearTokens();

  window.location.href = "/login";
}


// ======================================================
// Refresh Token
// ======================================================

export async function refreshToken() {
  const refresh =
    getRefreshToken();

  if (!refresh) return null;

  const response =
    await api.post<LoginResponse>(
      "/auth/refresh",
      {
        refresh_token: refresh,
      },
    );

  saveTokens(
    response.data.access_token,
    response.data.refresh_token,
  );

  return response.data;
}


// ======================================================
// Current User
// ======================================================

export async function getCurrentUser() {
  const response =
    await api.get<User>(
      "/auth/me",
    );

  return response.data;
}


// ======================================================
// Google Login
// ======================================================

export function loginGoogle() {
  window.location.href =
    `${API_URL}/auth/google`;
}


// ======================================================
// Discord Login
// ======================================================

export function loginDiscord() {
  window.location.href =
    `${API_URL}/auth/discord`;
}


// ======================================================
// Wallet Login
// ======================================================

export async function walletLogin(
  provider: string,
  wallet: string,
  message: string,
  signature: string,
) {
  const response =
    await api.post<LoginResponse>(
      "/auth/wallet",
      {
        provider,
        wallet,
        message,
        signature,
      },
    );

  saveTokens(
    response.data.access_token,
    response.data.refresh_token,
  );

  return response.data;
}


// ======================================================
// Token Validation
// ======================================================

export function isAuthenticated() {
  return !!getAccessToken();
}


// ======================================================
// Decode JWT
// ======================================================

export function decodeJWT(
  token: string,
) {
  try {
    const payload =
      token.split(".")[1];

    return JSON.parse(
      atob(payload),
    );
  } catch {
    return null;
  }
}


// ======================================================
// Token Expiry
// ======================================================

export function tokenExpired() {
  const token =
    getAccessToken();

  if (!token) return true;

  const payload =
    decodeJWT(token);

  if (!payload) return true;

  return (
    Date.now() >=
    payload.exp * 1000
  );
}


// ======================================================
// Auto Refresh
// ======================================================

export async function ensureSession() {
  if (
    tokenExpired() &&
    getRefreshToken()
  ) {
    try {
      await refreshToken();
    } catch {
      logout();
    }
  }
}