import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const startGame = async () => {
  const response = await api.get("/newgame");
  return response.data;
};
