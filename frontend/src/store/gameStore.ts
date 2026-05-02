import { create } from "zustand";

type GameStatus = "active" | "won" | "lost";

type GameState = {
  guesses: string[];
  currentGuessIndex: number;
  // 2D array — scores[row][col] = "correct" | "present" | "absent" | null (not yet scored)
  scores: (string | null)[][];
  status: GameStatus;
  keyboard: Record<string, string>;

  addGuess: (guess: string, score: string[]) => void;
  setStatus: (status: GameStatus) => void;
  setKeyboard: (keyboard: Record<string, string>) => void;
  reset: () => void;
  inputChar: (char: character) => void;
};

const EMPTY_SCORES = () =>
  Array.from({ length: 6 }, () => Array<string | null>(5).fill(null));

export const useGameStore = create<GameState>((set) => ({
  guesses: [],
  currentGuessIndex: 0,
  scores: EMPTY_SCORES(),
  status: "active",
  keyboard: {},

  addGuess: (guess, score) =>
    set((state) => {
      const newScores = state.scores.map((row) => [...row]);
      newScores[state.currentGuessIndex] = score;
      return {
        guesses: [...state.guesses, guess],
        scores: newScores,
        currentGuessIndex: state.currentGuessIndex + 1,
      };
    }),

  setStatus: (status) => set({ status }),

  setKeyboard: (keyboard) => set({ keyboard }),

  inputChar: (char) => {
    set((state) => {
      const currentGuess = state.guesses[state.currentGuessIndex];
      const newGuess = currentGuess + char;
      return {
        guesses: [
          ...state.guesses.slice(0, state.currentGuessIndex - 1),
          newGuess,
        ],
      };
    });
  },

  reset: () =>
    set({
      guesses: [],
      currentGuessIndex: 0,
      scores: EMPTY_SCORES(),
      status: "active",
      keyboard: {},
    }),
}));
