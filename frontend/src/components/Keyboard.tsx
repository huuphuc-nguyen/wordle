import { useGameStore } from "@/store/gameStore";

const ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];

function getKeyColor(state: string) {
  switch (state) {
    case "correct":
      return "bg-green-500 text-white";
    case "present":
      return "bg-yellow-500 text-white";
    case "absent":
      return "bg-gray-500 text-white";
    default:
      return "bg-gray-200 text-black";
  }
}

function Keyboard() {
  const keyboard = useGameStore((state) => state.keyboard);

  return (
    <div className="flex flex-col items-center gap-2">
      {ROWS.map((row) => (
        <div key={row} className="flex gap-1">
          {row.split("").map((letter) => (
            <div
              key={letter}
              className={`w-9 h-12 rounded flex items-center justify-center text-sm font-bold uppercase ${getKeyColor(keyboard[letter] ?? "unknown")}`}
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
