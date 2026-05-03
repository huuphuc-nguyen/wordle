# Wordle

A full-stack Wordle clone with session-based multiplayer support, containerized and deployed on a self-managed k3s cluster with a GitOps CD pipeline.

**Live:** [wordle.felixnguyen.dev](https://wordle.felixnguyen.dev)

---

## Architecture

```
Browser → Ingress (TLS) → Frontend (React/Vite)   [wordle.felixnguyen.dev]
Browser → Ingress (TLS) → Backend (FastAPI)        [apiwordle.felixnguyen.dev]
                               └── PostgreSQL
```

- Each player gets an independent game session — multiple players can play simultaneously with different secret words
- Sessions are tracked via a signed JWT stored as an `HttpOnly` cookie (XSS-safe, auto-sent by browser)
- Token contains `game_id` + expiry (30 min); backend validates on every guess

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, Zustand, Axios |
| Backend | Python, FastAPI, SQLModel, PyJWT, uv |
| Database | PostgreSQL 15 |
| Containerization | Docker (multi-stage builds) |
| Orchestration | k3s (Kubernetes) |
| CI/CD | GitHub Actions → GHCR → GitOps (Fleet by Rancher) |

---

## Services

| Service | URL |
|---------|-----|
| Frontend | https://wordle.felixnguyen.dev |
| Backend API | https://apiwordle.felixnguyen.dev |
| API Docs | https://apiwordle.felixnguyen.dev/docs |

---

## CI/CD Pipeline

Two independent GitHub Actions workflows — one per service.

**Trigger rules:**
- `frontend.yml` — triggers on push to `main` when any file under `frontend/` changes
- `backend.yml` — triggers on push to `main` when any file under `backend/` changes
- Both support manual trigger via `workflow_dispatch`

**Each workflow:**
1. Builds a multi-arch Docker image (`linux/amd64`, `linux/arm64`)
2. Pushes to GitHub Container Registry (`ghcr.io`) tagged with the commit SHA
3. Updates the image tag in the GitOps repo (`gitops-infras`) — Fleet picks up the change and syncs the k3s cluster automatically

```
git push → GitHub Actions → ghcr.io/<image>:<sha>
                                  └── update gitops-infras/values.yaml
                                              └── Fleet detects diff → deploys to k3s
```

**Required GitHub secrets:**

| Secret | Used by |
|--------|---------|
| `GH_PAT` | Push image tag updates to `gitops-infras` repo |
| `VITE_API_URL` | Baked into the frontend bundle at build time |

---

## Local Development

**Prerequisites:** Docker, `uv` (Python), `pnpm` (Node)

**Backend**
```bash
cd backend
cp .env.example .env   # fill in DATABASE_URL and SECRET_KEY
uv sync
uv run python -m app.scripts.seed_words
uv run fastapi dev app/main.py
```

**Frontend**
```bash
cd frontend
pnpm install
pnpm dev
```

Or run everything with Docker Compose:
```bash
docker compose up --build
```

---

## Word List

Sourced from [tabatkins/wordle-list](https://github.com/tabatkins/wordle-list) — the original NYT Wordle word list.

---

## Known Gaps / Planned Work

### Game State Restore
The data layer is fully ready — all guesses are persisted to the database alongside the game session. The intended behavior: as long as the player's JWT cookie is still valid (within the 30-min window), they can close the tab and return to find their game exactly where they left it. The frontend restore logic was not implemented due to time constraints.

### Abandoned Game Cleanup
A cleanup script (`app.scripts.cleanup_games`) exists and deletes active games older than 30 minutes. It needs to be wired up as a **Kubernetes CronJob** to run automatically — currently must be triggered manually.

---

> **Note (self):** After all containers in the k3s pod reach steady state, run the word seed script manually:
> ```bash
> kubectl exec -it <backend-pod> -- uv run python -m app.scripts.seed_words
> ```
> Only needed on first deploy or if the Word table is empty.
