import { create } from "zustand";

type GameState = {
  guesses: string[];
  currentGuessIndex: number;

  addGuess: (guess: string) => void;
  setCurrentGuessIndex: (index: number) => void;
  reset: () => void;
};

export const useGameStore = create<GameState>((set) => ({
  guesses: [],
  currentGuessIndex: 0,
  addGuess: (guess: string) =>
    set((state) => ({ guesses: [...state.guesses, guess] })),
  setCurrentGuessIndex: (index: number) => set({ currentGuessIndex: index }),
  reset: () => set({ guesses: [], currentGuessIndex: 0 }),
}));
