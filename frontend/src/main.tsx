import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./index.css";
import "@fontsource/poppins";
import "@fontsource/poppins/600.css";

import App from "./App.tsx";
import { BrowserRouter } from "react-router-dom";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter basename="/wordle">
      <App />
    </BrowserRouter>
  </StrictMode>,
);
