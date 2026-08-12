"use client";

import { useEffect, useState } from "react";

import {
  getTokens
} from "@/services/tokenService";

export function useTokens() {

  const [tokens, setTokens] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    getTokens()

      .then(setTokens)

      .finally(() =>
        setLoading(false)
      );

  }, []);

  return {

    tokens,

    loading
  };
}