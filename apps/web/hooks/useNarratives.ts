"use client";

import { useEffect, useState } from "react";

import {
  getNarratives
} from "@/services/narrativeService";

export function useNarratives() {

  const [data, setData] =
    useState([]);

  useEffect(() => {

    getNarratives()

      .then(setData);

  }, []);

  return data;
}