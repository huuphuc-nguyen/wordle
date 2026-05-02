# Wordle Backend

FastAPI + PostgreSQL backend for the Wordle game.

## Stack

- **FastAPI** — API framework
- **SQLModel** — ORM (built on SQLAlchemy + Pydantic)
- **PostgreSQL** — database
- **PyJWT** — session token signing
- **uv** — package manager

## Project Structure

```
app/
├── enums/          # Shared enums (GameStatus, APIStatus)
├── models/         # Database table definitions (Game, Word)
├── routers/        # HTTP endpoints (game, health)
├── schemas/        # Request and response shapes
│   ├── request/
│   └── response/
├── scripts/        # One-off scripts (seed_words)
├── services/       # Business logic (game_service, session_service)
├── db.py           # Database engine and session
└── main.py         # App entry point
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/newgame` | Start a new game, sets session cookie |
| POST | `/api/guess` | Submit a guess, returns score and game state |
| GET | `/health/health` | Health check |

## Local Setup

**1. Start PostgreSQL**
```bash
docker run -d \
  --name wordle-db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=wordle_db \
  -p 5432:5432 \
  postgres:15
```

**2. Configure environment**
```bash
cp .env.example .env
```

**3. Install dependencies**
```bash
uv sync
```

**4. Seed the word list**
```bash
uv run python -m app.scripts.seed_words
```

**5. Start the server**
```bash
uv run fastapi dev app/main.py
```

## Session Security

Each game issues a signed JWT stored as an `HttpOnly` cookie. The token contains the `game_id` and expires after 30 minutes. The frontend never handles the token directly — the browser sends it automatically on every request.
