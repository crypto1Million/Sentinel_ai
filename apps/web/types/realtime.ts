import { create } from "zustand";

import type {
  RealtimeAlert,
  RealtimeConnectionStatus,
  RealtimeEvent,
  RealtimeToken,
  RealtimeWallet,
} from "@/types/realtime";


interface RealtimeStore {
  connectionStatus: RealtimeConnectionStatus;

  lastEventAt: string | null;

  lastEventType: string | null;

  eventCount: number;

  eventCountsByType: Record<string, number>;

  tokensByKey: Record<string, RealtimeToken>;

  scoresByToken: Record<
    string,
    Record<string, unknown>
  >;

  walletsByKey: Record<string, RealtimeWallet>;

  alerts: RealtimeAlert[];

  setConnectionStatus: (
    status: RealtimeConnectionStatus
  ) => void;

  applyEvent: (
    event: RealtimeEvent
  ) => void;
}


const TOKEN_PATCH_TYPES = new Set([
  "token.updated",
  "pool.updated",
  "launchpad.detected",
  "rug.updated",
  "market_intelligence.updated",
  "j7.updated",
  "narrative.updated",
]);


function asRecord(
  value: unknown
): Record<string, unknown> {

  return (
    value !== null &&
    typeof value === "object" &&
    !Array.isArray(value)
  )
    ? value as Record<string, unknown>
    : {};
}


function asString(
  ...values: unknown[]
): string | undefined {

  for (const value of values) {

    if (
      typeof value === "string" &&
      value.trim()
    ) {
      return value.trim();
    }
  }

  return undefined;
}


function asNumber(
  ...values: unknown[]
): number | undefined {

  for (const value of values) {

    if (
      typeof value === "number" &&
      Number.isFinite(value)
    ) {
      return value;
    }

    if (
      typeof value === "string" &&
      value.trim()
    ) {

      const parsed = Number(value);

      if (Number.isFinite(parsed)) {
        return parsed;
      }
    }
  }

  return undefined;
}


function shortAddress(
  address: string
): string {

  return address.length > 12
    ? `${address.slice(0, 5)}…${address.slice(-5)}`
    : address;
}


export const useRealtimeStore =
  create<RealtimeStore>((set) => ({

    connectionStatus: "disconnected",

    lastEventAt: null,

    lastEventType: null,

    eventCount: 0,

    eventCountsByType: {},

    tokensByKey: {},

    scoresByToken: {},

    walletsByKey: {},

    alerts: [],


    setConnectionStatus: (
      connectionStatus
    ) => set({
      connectionStatus,
    }),


    applyEvent: (event) =>

      set((state) => {

        const payload = asRecord(
          event.payload
        );

        const chain =
          event.chain || "unknown";


        const eventCountsByType = {
          ...state.eventCountsByType,

          [event.event_type]:
            (
              state.eventCountsByType[
                event.event_type
              ] || 0
            ) + 1,
        };


        let tokensByKey =
          state.tokensByKey;

        let scoresByToken =
          state.scoresByToken;

        let walletsByKey =
          state.walletsByKey;

        let alerts =
          state.alerts;


        // =========================================
        // TOKEN / MARKET / INTELLIGENCE EVENTS
        // =========================================

        if (
          TOKEN_PATCH_TYPES.has(
            event.event_type
          )
        ) {

          const mint = asString(

            payload.token_mint,

            payload.token,

            payload.mint,

            payload.token_address,

            event.entity_type === "token"
              ? event.entity_id
              : undefined
          );


          if (mint) {

            const key = `${chain}:${mint}`;

            const previous =
              state.tokensByKey[key];


            const symbol =
              asString(
                payload.symbol,
                previous?.symbol
              ) || shortAddress(mint);


            const name =
              asString(
                payload.name,
                previous?.name
              ) || symbol;


            const token: RealtimeToken = {

              mint,

              chain,

              symbol,

              name,

              marketCap:
                asNumber(
                  payload.market_cap_usd,
                  payload.market_cap,
                  payload.marketCap
                ) ?? previous?.marketCap,

              liquidity:
                asNumber(
                  payload.liquidity_usd,
                  payload.liquidity,
                  payload.liquidityUsd
                ) ?? previous?.liquidity,

              volume24h:
                asNumber(
                  payload.volume_24h_usd,
                  payload.volume_24h,
                  payload.volume24h
                ) ?? previous?.volume24h,

              holders:
                asNumber(
                  payload.holders,
                  payload.holder_count,
                  payload.num_holders
                ) ?? previous?.holders,

              price:
                asNumber(
                  payload.price_usd,
                  payload.price,
                  payload.priceUsd
                ) ?? previous?.price,

              observedAt:
                event.observed_at,

              lastEventType:
                event.event_type,

              raw: {
                ...(previous?.raw || {}),
                ...payload,
              },
            };


            tokensByKey = {

              ...state.tokensByKey,

              [key]: token,
            };
          }
        }


        // =========================================
        // SENTINEL SCORE EVENTS
        // =========================================

        if (
          event.event_type === "score.updated"
        ) {

          const mint = asString(

            payload.token_mint,

            payload.token,

            payload.mint,

            event.entity_type === "token"
              ? event.entity_id
              : undefined
          );


          if (mint) {

            const key = `${chain}:${mint}`;

            const result = asRecord(
              payload.result
            );


            scoresByToken = {

              ...state.scoresByToken,

              [key]: {

                ...(
                  state.scoresByToken[key] || {}
                ),

                ...payload,

                ...result,

                updatedAt:
                  event.observed_at,
              },
            };
          }
        }


        // =========================================
        // WALLET DNA EVENTS
        // =========================================

        if (
          event.event_type === "wallet.updated" ||
          event.event_type === "wallet_dna.updated"
        ) {

          const address = asString(

            payload.wallet_address,

            payload.wallet,

            payload.address,

            event.entity_type === "wallet"
              ? event.entity_id
              : undefined
          );


          if (address) {

            const key = `${chain}:${address}`;

            const previous =
              state.walletsByKey[key];


            walletsByKey = {

              ...state.walletsByKey,

              [key]: {

                address,

                chain,

                updatedAt:
                  event.observed_at,

                raw: {
                  ...(previous?.raw || {}),
                  ...payload,
                },
              },
            };
          }
        }


        // =========================================
        // ALERT EVENTS
        // =========================================

        if (
          event.event_type === "alert.created"
        ) {

          const alert: RealtimeAlert = {

            eventId:
              event.event_id,

            chain:
              event.chain || null,

            severity:
              asString(payload.severity) || "info",

            title:
              asString(payload.title) ||
              "Sentinel alert",

            message:
              asString(payload.message) ||
              "A new alert was received.",

            createdAt:
              event.observed_at,

            payload,
          };


          alerts = [

            alert,

            ...state.alerts.filter(
              (item) =>
                item.eventId !== event.event_id
            ),

          ].slice(0, 50);
        }


        // =========================================
        // UPDATE STORE
        // =========================================

        return {

          eventCount:
            state.eventCount + 1,

          eventCountsByType,

          lastEventAt:
            event.observed_at,

          lastEventType:
            event.event_type,

          tokensByKey,

          scoresByToken,

          walletsByKey,

          alerts,
        };

      }),

  }));