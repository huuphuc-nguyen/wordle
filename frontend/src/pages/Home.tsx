import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="w-full h-dvh flex justify-center items-center">
      <Button
        onClick={() => {
          navigate("/game");
        }}
      >
        <span>Start</span>
      </Button>
    </div>
  );
}

export default Home;
