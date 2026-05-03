import { MESSAGES } from "@/constant/message";
import { startGame, submitGuess } from "@/lib/api";
import toast from "react-hot-toast";
import { useGameStore } from "@/store/gameStore";
import { useEffect } from "react";

export const useStartGame = () => {
  const reset = useGameStore((state) => state.reset);
  const inputChar = useGameStore((state) => state.inputChar);
  const deleteChar = useGameStore((state) => state.deleteChar);
  const addGuess = useGameStore((state) => state.addGuess);
  const setStatus = useGameStore((state) => state.setStatus);
  const setKeyboard = useGameStore((state) => state.setKeyboard);
  const currentGuessIndex = useGameStore((state) => state.currentGuessIndex);
  const guesses = useGameStore((state) => state.guesses);
  const status = useGameStore((state) => state.status);

  const fetchstart = async () => {
    const response = await startGame();
    if (response.status === "success") {
      toast.success(MESSAGES.GAME_STARTED);
    } else {
      toast.error(MESSAGES.GAME_STARTED_ERROR);
    }
  };

  // Exposed so the restart button can call it
  const restart = async () => {
    await fetchstart();
    reset();
  };

  const handleKeyUp = async (e: KeyboardEvent) => {
    // Block all input when game is over — player must press restart
    if (status !== "active") return;

    const key = e.key.toLowerCase();

    if (/^[a-z]$/.test(key)) {
      if (guesses[currentGuessIndex].length >= 5) {
        toast.error(MESSAGES.MAX_CHAR);
        return;
      }
      inputChar(key);
    }

    if (key === "backspace") {
      deleteChar();
    }

    if (key === "enter") {
      const currentGuess = guesses[currentGuessIndex];

      if (currentGuess.length < 5) {
        toast.error(MESSAGES.NOT_ENOUGH_LETTERS);
        return;
      }

      try {
        const response = await submitGuess(currentGuess);

        if (response.code === 401) {
          // Session expired — show restart button instead of auto-restarting
          toast.error(MESSAGES.SESSION_EXPIRED);
          setStatus("lost");
          return;
        }

        if (response.code === 400) {
          if (response.message === MESSAGES.INVALID_WORD) {
            toast.error(response.message);
            return;
          }
          // Game not found or already over — show restart button
          toast.error(response.message);
          setStatus("lost");
          return;
        }

        const { score, status: newStatus, keyboard } = response.data;
        addGuess(currentGuess, score);
        setStatus(newStatus);
        setKeyboard(keyboard);

        if (newStatus === "won") toast.success(MESSAGES.GAME_WON);
        if (newStatus === "lost") toast.error(MESSAGES.GAME_LOST);
      } catch {
        toast.error(MESSAGES.GAME_STARTED_ERROR);
      }
    }
  };

  useEffect(() => {
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, [guesses, currentGuessIndex, status]);

  useEffect(() => {
    restart();
  }, []);

  return { restart };
};
