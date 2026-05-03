import { useState } from "react";
import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";

const RULES = [
  "Guess the secret 5-letter word in 6 tries.",
  "Each guess must be a valid word — press Enter to submit.",
  "After each guess, the tiles show how close you were:",
  "🟩 Green — correct letter, correct position.",
  "🟡 Yellow — correct letter, wrong position.",
  "⬛ Grey — letter not in the word.",
];

function Home() {
  const navigate = useNavigate();
  const [showRules, setShowRules] = useState(false);

  return (
    <div className="cosmic-bg w-full h-dvh flex justify-center items-center">
      <div className="glass p-10 flex flex-col items-center gap-8 w-full max-w-md mx-4">

        {/* Title */}
        <div className="flex flex-col items-center gap-2">
          <h1 className="gradient-text text-6xl font-black tracking-widest uppercase select-none">
            Wordle
          </h1>
          <p className="text-emerald-600/70 text-sm tracking-wider font-medium">
            Guess the word. Beat the clock.
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-3 w-full">
          <Button
            className="w-full h-12 text-base tracking-widest uppercase bg-emerald-500 hover:bg-emerald-600 text-white"
            onClick={() => navigate("/game")}
          >
            Play
          </Button>
          <Button
            className="w-full h-12 text-base tracking-widest uppercase bg-transparent hover:bg-emerald-50 text-emerald-600 border border-emerald-200"
            onClick={() => setShowRules(true)}
          >
            How to Play
          </Button>
        </div>
      </div>

      {/* Rules modal */}
      {showRules && (
        <div
          className="fixed inset-0 flex items-center justify-center z-50 bg-black/20 backdrop-blur-sm"
          onClick={() => setShowRules(false)}
        >
          <div
            className="glass p-8 max-w-sm w-full mx-4 flex flex-col gap-5"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="gradient-text text-2xl font-bold tracking-wide text-center">
              How to Play
            </h2>
            <ul className="flex flex-col gap-3">
              {RULES.map((rule, i) => (
                <li key={i} className="text-gray-600 text-sm leading-relaxed">
                  {rule}
                </li>
              ))}
            </ul>
            <Button
              className="w-full bg-emerald-500 hover:bg-emerald-600 text-white"
              onClick={() => setShowRules(false)}
            >
              Got it
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
