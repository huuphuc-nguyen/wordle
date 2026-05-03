import { useEffect, useState } from "react";
import Board from "../components/Board";
import Keyboard from "../components/Keyboard";
import { useGameStore } from "../store/gameStore";
import { useStartGame } from "../hooks/useStartGame";
import { Button } from "../components/ui/button";
import { fetchSecretWord } from "../lib/api";

function Game() {
  const guesses = useGameStore((state) => state.guesses);
  const scores = useGameStore((state) => state.scores);
  const status = useGameStore((state) => state.status);
  const { restart } = useStartGame();
  const [secretWord, setSecretWord] = useState<string | null>(null);

  useEffect(() => {
    if (status !== "active") {
      fetchSecretWord().then((res) => {
        if (res.code === 200) setSecretWord(res.data.secret_word);
      });
    } else {
      setSecretWord(null);
    }
  }, [status]);

  return (
    <div className="cosmic-bg w-full h-dvh flex flex-col justify-center items-center gap-6 px-4">

      {/* Title */}
      <div className="flex flex-col items-center gap-1">
        <h1 className="gradient-text text-5xl font-black tracking-widest uppercase select-none">
          Wordle
        </h1>
        <div className="h-px w-24 bg-emerald-300/60 rounded-full" />
      </div>

      {/* Board — standalone, no card */}
      <Board guesses={guesses} scores={scores} />

      {/* Status message */}
      {status !== "active" && (
        <div className="flex flex-col items-center gap-3">
          <p className="text-3xl font-black tracking-wide drop-shadow-sm"
            style={{ WebkitTextStroke: "0.5px black", color: status === "won" ? "#065f46" : "#991b1b" }}
          >
            {status === "won" ? "🎉 You got it!" : "😔 Better luck next time"}
          </p>
          {secretWord && (
            <p className="text-gray-800 font-semibold text-sm">
              The word was <span className="font-black text-emerald-800 uppercase tracking-widest">{secretWord}</span>
            </p>
          )}
          <Button
            className="bg-emerald-500 hover:bg-emerald-600 text-white tracking-widest uppercase px-8 border-2 border-black shadow-md"
            onClick={restart}
          >
            Play Again
          </Button>
        </div>
      )}

      {/* Keyboard — standalone, no card */}
      <Keyboard />
    </div>
  );
}

export default Game;
