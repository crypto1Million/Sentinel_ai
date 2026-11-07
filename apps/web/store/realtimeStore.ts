"use client";

import { create } from "zustand";

export type RealtimeChannel =
  | "tokens"
  | "wallets"
  | "scores";

export type ConnectionStatus =
  | "connecting"
  | "live"
  | "reconnecting"
  | "offline";

export interface RealtimeEvent<T = Record<string, unknown>> {
  event_id: string;
  event_type: string;

  entity_type: string;
  entity_id: string;

  chain: string | null;

  payload: T;

  source: string;
  source_id: string | null;

  observed_at: string;
  received_at?: string;
  processed_at: string | null;

  chain_position?: {
    block_number?: number | null;
    block_hash?: string | null;
    slot?: number | null;
    transaction_hash?: string | null;
    transaction_signature?: string | null;
    instruction_index?: number | null;
    log_index?: number | null;
    commitment?: string | null;
  } | null;

  evidence?: Array<{
    type: string;
    value: string;
    source?: string | null;
    verified?: boolean;
  }>;

  parser_name?: string | null;
  parser_version?: string | null;

  model_name?: string | null;
  model_version?: string | null;

  parent_event_ids?: string[];

  status: string;
  version: number;

  age_ms?: number;
}

export interface RealtimeEntityState {
  values: Record<string, unknown>;
  eventId: string;
  observedAt: string;
  version: number;
  source: string;
}

interface RealtimeStore {
  connections: Record<
    RealtimeChannel,
    ConnectionStatus
  >;

  lastEventAt: Record<
    RealtimeChannel,
    number | null
  >;

  reconnectAttempts: Record<
    RealtimeChannel,
    number
  >;

  tokens: Record<
    string,
    RealtimeEntityState
  >;

  wallets: Record<
    string,
    RealtimeEntityState
  >;

  scores: Record<
    string,
    RealtimeEntityState
  >;

  alerts: RealtimeEvent[];

  recentEventIds: string[];

  setConnectionStatus: (
    channel: RealtimeChannel,
    status: ConnectionStatus,
  ) => void;

  setReconnectAttempts: (
    channel: RealtimeChannel,
    attempts: number,
  ) => void;

  applyEvent: (
    channel: RealtimeChannel,
    event: RealtimeEvent,
  ) => void;

  addAlert: (
    event: RealtimeEvent,
  ) => void;

  reset: () => void;
}

function extractPatch(
  payload: Record<string, unknown>,
): Record<string, unknown> {
  const patch = payload.patch;

  if (
    patch &&
    typeof patch === "object" &&
    !Array.isArray(patch)
  ) {
    return patch as Record<string, unknown>;
  }

  const values = payload.values;

  if (
    values &&
    typeof values === "object" &&
    !Array.isArray(values)
  ) {
    return values as Record<string, unknown>;
  }

  return payload;
}

function isNewerEvent(
  current: RealtimeEntityState | undefined,
  event: RealtimeEvent,
): boolean {
  if (!current) {
    return true;
  }

  if (event.version > current.version) {
    return true;
  }

  if (event.version < current.version) {
    return false;
  }

  return (
    event.observed_at >
    current.observedAt
  );
}

function mergeEntity(
  current: RealtimeEntityState | undefined,
  event: RealtimeEvent,
): RealtimeEntityState {
  const payload =
    event.payload &&
    typeof event.payload === "object"
      ? event.payload
      : {};

  const patch = extractPatch(
    payload as Record<string, unknown>,
  );

  return {
    values: {
      ...(current?.values ?? {}),
      ...patch,
    },

    eventId: event.event_id,
    observedAt: event.observed_at,
    version: event.version,
    source: event.source,
  };
}

export const useRealtimeStore =
  create<RealtimeStore>((set) => ({
    connections: {
      tokens: "offline",
      wallets: "offline",
      scores: "offline",
    },

    lastEventAt: {
      tokens: null,
      wallets: null,
      scores: null,
    },

    reconnectAttempts: {
      tokens: 0,
      wallets: 0,
      scores: 0,
    },

    tokens: {},
    wallets: {},
    scores: {},

    alerts: [],

    recentEventIds: [],

    setConnectionStatus: (
      channel,
      status,
    ) => {
      set((state) => ({
        connections: {
          ...state.connections,
          [channel]: status,
        },
      }));
    },

    setReconnectAttempts: (
      channel,
      attempts,
    ) => {
      set((state) => ({
        reconnectAttempts: {
          ...state.reconnectAttempts,
          [channel]: attempts,
        },
      }));
    },

    applyEvent: (
      channel,
      event,
    ) => {
      set((state) => {
        /*
         * Deduplication.
         *
         * Reconnects/backfills/providers can occasionally
         * deliver the same canonical event more than once.
         */
        if (
          state.recentEventIds.includes(
            event.event_id,
          )
        ) {
          return state;
        }

        const nextRecentIds = [
          ...state.recentEventIds,
          event.event_id,
        ].slice(-5000);

        const collections =
          channel === "tokens"
            ? state.tokens
            : channel === "wallets"
              ? state.wallets
              : state.scores;

        const current =
          collections[event.entity_id];

        /*
         * Do not allow an older event to overwrite
         * newer entity state.
         */
        if (
          event.event_type !==
            "alert.created" &&
          !isNewerEvent(current, event)
        ) {
          return {
            ...state,
            recentEventIds: nextRecentIds,
          };
        }

        const nextEntity = mergeEntity(
          current,
          event,
        );

        return {
          ...state,

          recentEventIds:
            nextRecentIds,

          lastEventAt: {
            ...state.lastEventAt,
            [channel]: Date.now(),
          },

          tokens:
            channel === "tokens"
              ? {
                  ...state.tokens,
                  [event.entity_id]:
                    nextEntity,
                }
              : state.tokens,

          wallets:
            channel === "wallets"
              ? {
                  ...state.wallets,
                  [event.entity_id]:
                    nextEntity,
                }
              : state.wallets,

          scores:
            channel === "scores"
              ? {
                  ...state.scores,
                  [event.entity_id]:
                    nextEntity,
                }
              : state,
        };
      });
    },

    addAlert: (event) => {
      set((state) => {
        if (
          state.recentEventIds.includes(
            event.event_id,
          )
        ) {
          return state;
        }

        return {
          ...state,

          alerts: [
            event,
            ...state.alerts,
          ].slice(0, 200),

          recentEventIds: [
            ...state.recentEventIds,
            event.event_id,
          ].slice(-5000),
        };
      });
    },

    reset: () => {
      set({
        connections: {
          tokens: "offline",
          wallets: "offline",
          scores: "offline",
        },

        lastEventAt: {
          tokens: null,
          wallets: null,
          scores: null,
        },

        reconnectAttempts: {
          tokens: 0,
          wallets: 0,
          scores: 0,
        },

        tokens: {},
        wallets: {},
        scores: {},
        alerts: [],
        recentEventIds: [],
      });
    },
  }));