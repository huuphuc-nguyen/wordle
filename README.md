# Wordle

- Frontend: React (Vite) with pnpm for fast and efficient package management, tailwind CSS, shadcn
- Backend: Python (FastAPI) with SQLModel ORM
- Database: PostgreSQL (Docker), well-suited for SQLModel built on SQLAlchemy
- Hosting: Self-managed VPS for full-stack deployment; fallback to Vercel if needed

each game session has an id -> multiple players get multiple secret, can replay multiple time.

each session has a session token stored as cookie, storing game id, useragent, expiring time 30 minutes.

wordle list https://github.com/tabatkins/wordle-list
