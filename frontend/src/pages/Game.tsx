import Board from "../components/Board";
import { useGameStore } from "../store/gameStore";
import { useEffect } from "react";
import { useStartGame } from "../hooks/useStartGame";

function Game() {
  const guesses = useGameStore((state) => state.guesses);
  const scores = useGameStore((state) => state.scores);
  useStartGame();
  return (
    <div className="w-full h-dvh flex flex-col gap-4 justify-center items-center">
      <h1>Wordle</h1>
      <Board guesses={guesses} scores={scores} />
    </div>
  );
}

export default Game;
