# Wordle Frontend

React + TypeScript + Vite frontend for the Wordle game.

## Stack

- **React 19** — UI framework
- **TypeScript** — type safety
- **Vite** — build tool
- **Zustand** — state management
- **Tailwind CSS v4** — styling
- **Axios** — HTTP client
- **pnpm** — package manager

## Project Structure

```
src/
├── assets/         # Static assets (background image)
├── components/     # Reusable UI components (Board, Keyboard)
├── constant/       # Shared constants (messages)
├── hooks/          # Custom hooks (useStartGame)
├── lib/            # Axios instance and API calls
├── pages/          # Route pages (Home, Game)
├── store/          # Zustand game state
└── main.tsx        # App entry point
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend base URL (e.g. `http://localhost:8000`) |

> **Note:** Vite bakes environment variables into the bundle at **build time**, not runtime.
> You must provide `VITE_API_URL` when building the image — it cannot be changed after the image is built.

Create a `.env` file for local development:
```bash
VITE_API_URL=http://localhost:8000
```

## Local Development

**1. Install dependencies**
```bash
pnpm install
```

**2. Start the dev server**
```bash
pnpm dev
```

App runs at `http://localhost:5173`.

## Docker

> **Important:** `VITE_API_URL` must be passed as a build argument — it is baked into the bundle at build time.

**Build**
```bash
docker build \
  --build-arg VITE_API_URL=http://localhost:8000 \
  -t wordle-fe .
```

**Run**
```bash
docker run -p 3000:3000 wordle-fe
```

App is served at `http://localhost:3000`.
