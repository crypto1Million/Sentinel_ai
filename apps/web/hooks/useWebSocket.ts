"use client";

import { useEffect } from "react";

import {
  getAccessToken
} from "@/lib/auth/auth";

import {
  useRealtimeStore
} from "@/store/realtimeStore";

import type {
  RealtimeEvent
} from "@/types/realtime";


const RECONNECT_BASE_MS = 1_000;

const RECONNECT_MAX_MS = 30_000;


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
  }

  else if (url.protocol === "http:") {
    url.protocol = "ws:";
  }


  if (
    url.protocol !== "ws:" &&
    url.protocol !== "wss:"
  ) {
    throw new Error(
      "NEXT_PUBLIC_WS_URL must use ws:// or wss://"
    );
  }


  if (
    !url.pathname.endsWith("/ws/events")
  ) {

    url.pathname =
      `${url.pathname.replace(/\/+$/, "")}/ws/events`;
  }


  url.search = "";

  url.hash = "";


  return url;
}


// =============================================
// REQUEST AUTHENTICATED REALTIME TICKET
// =============================================

async function requestRealtimeTicket(): Promise<string> {

  const accessToken = getAccessToken();


  if (!accessToken) {

    throw new Error(
      "Authentication required for realtime events"
    );
  }


  const apiOrigin =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";


  const response = await fetch(

    new URL(
      "/realtime/ticket",
      apiOrigin
    ),

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
      `Realtime ticket request failed (${response.status})`
    );
  }


  const body = await response.json() as {
    ticket?: unknown;
  };


  if (
    typeof body.ticket !== "string" ||
    !body.ticket
  ) {

    throw new Error(
      "Realtime ticket response was invalid"
    );
  }


  return body.ticket;
}


// =============================================
// VALIDATE EVENT MESSAGE
// =============================================

function isRealtimeEvent(
  value: unknown
): value is RealtimeEvent {

  if (
    !value ||
    typeof value !== "object"
  ) {
    return false;
  }


  const candidate =
    value as Record<string, unknown>;


  return (

    typeof candidate.event_id === "string" &&

    typeof candidate.event_type === "string" &&

    typeof candidate.entity_type === "string" &&

    typeof candidate.entity_id === "string" &&

    typeof candidate.observed_at === "string" &&

    candidate.payload !== null &&

    typeof candidate.payload === "object" &&

    !Array.isArray(candidate.payload)

  );
}


// =============================================
// MAIN WEBSOCKET HOOK
// =============================================

export function useWebSocket() {

  useEffect(() => {

    let socket: WebSocket | null = null;

    let reconnectTimer:
      ReturnType<typeof setTimeout> | undefined;

    let reconnectAttempt = 0;

    let connecting = false;

    let disposed = false;


    const setConnectionStatus =
      useRealtimeStore.getState().setConnectionStatus;


    // =========================================
    // RECONNECT SCHEDULER
    // =========================================

    const scheduleReconnect = () => {

      if (
        disposed ||
        reconnectTimer
      ) {
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


    // =========================================
    // CONNECT
    // =========================================

    const connect = async () => {

      if (
        disposed ||
        connecting
      ) {
        return;
      }


      connecting = true;


      setConnectionStatus(

        reconnectAttempt === 0
          ? "connecting"
          : "reconnecting"
      );


      let ticket: string;


      try {

        ticket =
          await requestRealtimeTicket();

      }

      catch {

        connecting = false;

        setConnectionStatus("error");

        scheduleReconnect();

        return;
      }


      if (disposed) {

        connecting = false;

        return;
      }


      let currentSocket: WebSocket;


      try {

        const url =
          resolveEventsUrl();


        url.searchParams.set(
          "ticket",
          ticket
        );


        currentSocket = new WebSocket(
          url.toString()
        );

      }

      catch {

        connecting = false;

        setConnectionStatus("error");

        scheduleReconnect();

        return;
      }


      socket = currentSocket;

      connecting = false;


      // =======================================
      // CONNECTED
      // =======================================

      currentSocket.onopen = () => {

        reconnectAttempt = 0;

        setConnectionStatus("connected");
      };


      // =======================================
      // RECEIVE REAL BACKEND EVENTS
      // =======================================

      currentSocket.onmessage = (
        message: MessageEvent<string>
      ) => {

        let parsed: unknown;


        try {

          parsed = JSON.parse(
            message.data
          );

        }

        catch {

          return;
        }


        if (
          isRealtimeEvent(parsed)
        ) {

          useRealtimeStore
            .getState()
            .applyEvent(parsed);
        }
      };


      // =======================================
      // SOCKET ERROR
      // =======================================

      currentSocket.onerror = () => {

        setConnectionStatus("error");
      };


      // =======================================
      // SOCKET CLOSED
      // =======================================

      currentSocket.onclose = () => {

        if (socket === currentSocket) {
          socket = null;
        }


        if (disposed) {

          setConnectionStatus("disconnected");

          return;
        }


        setConnectionStatus("reconnecting");

        scheduleReconnect();
      };

    };


    // START CONNECTION

    void connect();


    // =========================================
    // CLEANUP
    // =========================================

    return () => {

      disposed = true;


      if (reconnectTimer) {

        clearTimeout(
          reconnectTimer
        );
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


      setConnectionStatus(
        "disconnected"
      );

    };

  }, []);

}