import { MESSAGES } from "@/constant/message";
import { startGame } from "@/lib/api";
import toast from "react-hot-toast";
import { useGameStore } from "@/store/gameStore";
import { useEffect } from "react";

export const useStartGame = () => {
  // reset store
  const reset = useGameStore((state) => state.reset);
  const inputChar = useGameStore((state) => state.inputChar);

  // fetch start api
  const fetchstart = async () => {
    const response = await startGame();
    if (response.status === "success") {
      toast.success(MESSAGES.GAME_STARTED);
    } else {
      toast.error(MESSAGES.GAME_STARTED_ERROR);
    }
  };

  const handleKeyUp = (e: KeyboardEvent) => {
    const key = e.key.toLowerCase();

    if (/^[a-z]$/.test(key)) {
      inputChar(key);
    }

    if (key === "backspace") {
      //("");
    }

    if (key === "enter") {
      //  addGuess();
    }
  };

  const init = async () => {
    await fetchstart();
    reset();
  };

  useEffect(() => {
    init();

    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);
  return {};
};
