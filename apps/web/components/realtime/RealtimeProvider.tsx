"use client";

import {
  useWebSocket
} from "@/hooks/useWebSocket";


export default function RealtimeProvider() {

  useWebSocket();

  return null;
}