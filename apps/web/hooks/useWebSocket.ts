"use client";

import { useEffect } from "react";

export function useWebSocket() {

  useEffect(() => {

    const ws =
      new WebSocket(
        "ws://localhost:8000/ws/tokens"
      );

    ws.onmessage =
      (event) => {

        console.log(
          JSON.parse(
            event.data
          )
        );
      };

    return () => {

      ws.close();
    };

  }, []);
}