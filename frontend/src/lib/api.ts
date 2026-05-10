import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true, // send cookies on every request
  headers: {
    "Content-Type": "application/json",
  },
});

export const startGame = async () => {
  const response = await api.get("/apiwordle/api/newgame");
  return response.data;
};

export const submitGuess = async (word: string) => {
  const response = await api.post("/apiwordle/api/guess", { word });
  return response.data;
};

export const fetchSecretWord = async () => {
  const response = await api.get("/apiwordle/api/secret");
  return response.data;
};
