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
├── scripts/        # One-off and scheduled scripts (seed_words, cleanup_games)
├── services/       # Business logic (game_service, session_service)
├── db.py           # Database engine and session
└── main.py         # App entry point
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Secret used to sign JWT session tokens |

Copy the example file and fill in the values:
```bash
cp .env.example .env
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/newgame` | Start a new game, sets session cookie |
| POST | `/api/guess` | Submit a guess, returns score and game state |
| GET | `/api/secret` | Return secret word (only when game is over) |
| GET | `/health/health` | Health check |

## Local Development

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

**2. Install dependencies**
```bash
uv sync
```

**3. Seed the word list**
```bash
uv run python -m app.scripts.seed_words
```

**4. Start the dev server**
```bash
uv run fastapi dev app/main.py
```

## Docker

**Build**
```bash
docker build -t wordle-be .
```

**Run**
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@host.containers.internal:5432/wordle_db \
  -e SECRET_KEY=your-secret-key \
  wordle-be
```

## Maintenance Scripts

| Script | Description |
|--------|-------------|
| `app.scripts.seed_words` | Populate the Word table from `data/words.txt` |
| `app.scripts.cleanup_games` | Delete abandoned active games older than 30 minutes |

Run any script with:
```bash
uv run python -m app.scripts.<script_name>
```

Schedule `cleanup_games` with cron (every 30 min):
```
*/30 * * * * cd /path/to/backend && uv run python -m app.scripts.cleanup_games
```

## Session Security

Each game issues a signed JWT stored as an `HttpOnly` cookie. The token contains the `game_id` and expires after 30 minutes. The frontend never handles the token directly — the browser sends it automatically on every request.
