"use client";

import { useEffect, useState } from "react";

import {
  getWallet
} from "@/services/walletService";

export function useWallets(
  wallet: string
) {

  const [data, setData] =
    useState(null);

  useEffect(() => {

    getWallet(wallet)

      .then(setData);

  }, [wallet]);

  return data;
}