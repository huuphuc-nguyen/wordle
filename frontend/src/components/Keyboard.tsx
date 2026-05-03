import { useGameStore } from "@/store/gameStore";

const ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];

type Props = {
  onKey: (key: string) => void;
};

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

function Keyboard({ onKey }: Props) {
  const keyboard = useGameStore((state) => state.keyboard);

  return (
    <div className="flex flex-col items-center gap-2">
      {ROWS.map((row, rowIndex) => (
        <div key={row} className="flex gap-1.5">
          {rowIndex === 2 && (
            <button
              onClick={() => onKey("enter")}
              className="h-14 px-2 rounded-lg border-2 border-black shadow-md flex items-center justify-center text-xs font-bold uppercase bg-white text-gray-700 active:scale-95 transition-transform select-none"
            >
              Enter
            </button>
          )}
          {row.split("").map((letter) => (
            <button
              key={letter}
              onClick={() => onKey(letter)}
              className={`w-10 h-14 rounded-lg border-2 shadow-md flex items-center justify-center text-sm font-bold uppercase active:scale-95 transition-transform select-none ${getKeyColor(keyboard[letter] ?? "unknown")}`}
            >
              {letter}
            </button>
          ))}
          {rowIndex === 2 && (
            <button
              onClick={() => onKey("backspace")}
              className="h-14 px-2 rounded-lg border-2 border-black shadow-md flex items-center justify-center text-xs font-bold bg-white text-gray-700 active:scale-95 transition-transform select-none"
            >
              ⌫
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default Keyboard;
