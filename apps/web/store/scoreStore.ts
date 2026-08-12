import { create } from "zustand";

interface ScoreStore {

  score: number;

  setScore:
    (score: number) => void;
}

export const useScoreStore =
  create<ScoreStore>(
    (set) => ({

      score: 0,

      setScore:
        (score) =>
          set({ score })
    })
  );