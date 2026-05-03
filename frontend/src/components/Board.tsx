type Props = {
  guesses: string[];
  scores: (string | null)[][];
};

function getColor(score: string | null) {
  switch (score) {
    case "correct":
      return "bg-emerald-400 text-white border-black";
    case "present":
      return "bg-yellow-400 text-white border-black";
    case "absent":
      return "bg-gray-300 text-gray-400 border-black";
    default:
      return "bg-white text-gray-800 border-black";
  }
}

function Board({ guesses, scores }: Props) {
  return (
    <div className="flex flex-col gap-2 justify-center items-center">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="flex gap-2">
          {Array.from({ length: 5 }).map((_, j) => {
            const letter = guesses[i]?.[j] || "";
            const score = scores?.[i]?.[j] ?? null;

            return (
              <div
                key={j}
                className={`w-14 h-14 rounded-xl border-2 shadow-md flex items-center justify-center text-lg font-bold
                  ${getColor(score)}
                `}
              >
                {letter}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}

export default Board;
