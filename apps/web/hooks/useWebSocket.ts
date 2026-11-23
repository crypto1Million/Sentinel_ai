
"use client";

import { useEffect } from "react";

import { getAccessToken } from "@/lib/auth/auth";

import {
  useRealtimeStore,
  type RealtimeEvent,
  type RealtimeChannel,
  type ConnectionStatus,
} from "@/store/realtimeStore";

const RECONNECT_BASE_MS = 1000;
const RECONNECT_MAX_MS = 30000;

// --------------------------------------------------
// WEBSOCKET URL
// --------------------------------------------------

function resolveEventsUrl(): URL {
  const configuredUrl =
    process.env.NEXT_PUBLIC_WS_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";

  const url = new URL(
    configuredUrl,
    window.location.origin
  );

  if (url.protocol === "https:") {
    url.protocol = "wss:";
  } else if (url.protocol === "http:") {
    url.protocol = "ws:";
  }

  if (
    url.protocol !== "ws:" &&
    url.protocol !== "wss:"
  ) {
    throw new Error("Invalid WebSocket protocol");
  }

  if (!url.pathname.endsWith("/ws/events")) {
    url.pathname =
      `${url.pathname.replace(/\/+$/, "")}/ws/events`;
  }

  url.search = "";
  url.hash = "";

  return url;
}

// --------------------------------------------------
// AUTHENTICATED REALTIME TICKET
// --------------------------------------------------

async function requestRealtimeTicket(): Promise<string> {
  const accessToken = getAccessToken();

  if (!accessToken) {
    throw new Error("Authentication required");
  }

  const apiOrigin =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";

  const response = await fetch(
    new URL("/realtime/ticket", apiOrigin),
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(
      `Realtime ticket failed: ${response.status}`
    );
  }

  const body = await response.json() as {
    ticket?: unknown;
  };

  if (
    typeof body.ticket !== "string" ||
    !body.ticket
  ) {
    throw new Error("Invalid realtime ticket response");
  }

  return body.ticket;
}

// --------------------------------------------------
// EVENT VALIDATION
// --------------------------------------------------

function isRealtimeEvent(
  value: unknown
): value is RealtimeEvent {
  if (
    !value ||
    typeof value !== "object" ||
    Array.isArray(value)
  ) {
    return false;
  }

  const event = value as Record<string, unknown>;

  return (
    typeof event.event_id === "string" &&
    typeof event.event_type === "string" &&
    typeof event.entity_type === "string" &&
    typeof event.entity_id === "string" &&
    typeof event.observed_at === "string" &&
    event.payload !== null &&
    typeof event.payload === "object" &&
    !Array.isArray(event.payload)
  );
}

// --------------------------------------------------
// MAIN WEBSOCKET HOOK
// --------------------------------------------------

export function useWebSocket() {
  useEffect(() => {
    let socket: WebSocket | null = null;

    let reconnectTimer:
      ReturnType<typeof setTimeout> | undefined;

    let reconnectAttempt = 0;
    let connecting = false;
    let disposed = false;

    // Update all realtime channels consistently.
    const updateConnectionStatus = (
      status: ConnectionStatus
    ) => {
      const store = useRealtimeStore.getState();

      const channels: RealtimeChannel[] = [
        "tokens",
        "wallets",
        "scores",
      ];

      channels.forEach((channel) => {
        store.setConnectionStatus(channel, status);
      });
    };

    // ------------------------------------------------
    // RECONNECT SCHEDULER
    // ------------------------------------------------

    const scheduleReconnect = () => {
      if (disposed || reconnectTimer !== undefined) {
        return;
      }

      const delay = Math.min(
        RECONNECT_BASE_MS *
          2 ** Math.min(reconnectAttempt, 5),
        RECONNECT_MAX_MS
      );

      reconnectAttempt += 1;

      reconnectTimer = setTimeout(() => {
        reconnectTimer = undefined;
        void connect();
      }, delay);
    };

    // ------------------------------------------------
    // ROUTE BACKEND EVENTS
    // ------------------------------------------------

    const handleEvent = (event: RealtimeEvent) => {
      const store = useRealtimeStore.getState();

      if (event.event_type === "alert.created") {
        store.addAlert(event);
        return;
      }

      let channel: RealtimeChannel;

      if (
        event.entity_type === "wallet" ||
        event.event_type.startsWith("wallet")
      ) {
        channel = "wallets";
      } else if (
        event.entity_type === "score" ||
        event.event_type.startsWith("score")
      ) {
        channel = "scores";
      } else {
        channel = "tokens";
      }

      store.applyEvent(channel, event);
    };

    // ------------------------------------------------
    // CONNECT
    // ------------------------------------------------

    const connect = async (): Promise<void> => {
      if (disposed || connecting) {
        return;
      }

      connecting = true;

      updateConnectionStatus(
        reconnectAttempt === 0
          ? "connecting"
          : "reconnecting"
      );

      try {
        const ticket = await requestRealtimeTicket();

        if (disposed) {
          return;
        }

        const url = resolveEventsUrl();

        url.searchParams.set("ticket", ticket);

        const currentSocket = new WebSocket(
          url.toString()
        );

        socket = currentSocket;

        // --------------------------------------------
        // CONNECTED
        // --------------------------------------------

        currentSocket.onopen = () => {
          reconnectAttempt = 0;
          updateConnectionStatus("live");
        };

        // --------------------------------------------
        // RECEIVE EVENTS
        // --------------------------------------------

        currentSocket.onmessage = (
          message: MessageEvent<string>
        ) => {
          let parsed: unknown;

          try {
            parsed = JSON.parse(message.data);
          } catch {
            return;
          }

          if (isRealtimeEvent(parsed)) {
            handleEvent(parsed);
          }
        };

        // --------------------------------------------
        // SOCKET ERROR
        // --------------------------------------------

        currentSocket.onerror = () => {
          updateConnectionStatus("reconnecting");
        };

        // --------------------------------------------
        // SOCKET CLOSED
        // --------------------------------------------

        currentSocket.onclose = () => {
          if (socket === currentSocket) {
            socket = null;
          }

          if (disposed) {
            updateConnectionStatus("offline");
            return;
          }

          updateConnectionStatus("reconnecting");
          scheduleReconnect();
        };

      } catch (error) {
        console.error(
          "[SentinelAI] Realtime connection failed:",
          error
        );

        updateConnectionStatus("reconnecting");
        scheduleReconnect();

      } finally {
        connecting = false;
      }
    };

    // START
    void connect();

    // ------------------------------------------------
    // CLEANUP
    // ------------------------------------------------

    return () => {
      disposed = true;

      if (reconnectTimer !== undefined) {
        clearTimeout(reconnectTimer);
        reconnectTimer = undefined;
      }

      if (socket) {
        socket.onopen = null;
        socket.onmessage = null;
        socket.onerror = null;
        socket.onclose = null;

        socket.close(
          1000,
          "Realtime provider unmounted"
        );

        socket = null;
      }

      updateConnectionStatus("offline");
    };

  }, []);
}
