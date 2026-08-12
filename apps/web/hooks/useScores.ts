"use client";

import { useEffect, useState } from "react";

import {
  getScore
} from "@/services/scoreService";

export function useScores(
  mint: string
) {

  const [score, setScore] =
    useState(null);

  useEffect(() => {

    getScore(mint)

      .then(setScore);

  }, [mint]);

  return score;
}