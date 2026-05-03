import Board from "../components/Board";
import Keyboard from "../components/Keyboard";
import { useGameStore } from "../store/gameStore";
import { useStartGame } from "../hooks/useStartGame";
import { Button } from "../components/ui/button";

function Game() {
  const guesses = useGameStore((state) => state.guesses);
  const scores = useGameStore((state) => state.scores);
  const status = useGameStore((state) => state.status);
  const { restart } = useStartGame();

  return (
    <div className="w-full h-dvh flex flex-col gap-4 justify-center items-center">
      <h1>Wordle</h1>
      <Board guesses={guesses} scores={scores} />
      <Keyboard />
      {status !== "active" && (
        <Button onClick={restart}>Play Again</Button>
      )}
    </div>
  );
}

export default Game;
