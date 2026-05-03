import { useGameStore } from "@/store/gameStore";

const ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];

function getKeyColor(state: string) {
  switch (state) {
    case "correct":
      return "bg-emerald-400 text-white border-black";
    case "present":
      return "bg-yellow-400 text-white border-black";
    case "absent":
      return "bg-gray-300 text-gray-400 border-black";
    default:
      return "bg-white text-gray-700 border-black";
  }
}

function Keyboard() {
  const keyboard = useGameStore((state) => state.keyboard);

  return (
    <div className="flex flex-col items-center gap-2">
      {ROWS.map((row) => (
        <div key={row} className="flex gap-1.5">
          {row.split("").map((letter) => (
            <div
              key={letter}
              className={`w-10 h-14 rounded-lg border-2 shadow-md flex items-center justify-center text-sm font-bold uppercase transition-colors ${getKeyColor(keyboard[letter] ?? "unknown")}`}
            >
              {letter}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default Keyboard;
