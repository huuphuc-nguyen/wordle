For testing and local dev only

docker run -d \
 --name wordle-db \
 -e POSTGRES_USER=user \
 -e POSTGRES_PASSWORD=password \
 -e POSTGRES_DB=wordle_db \
 -p 5432:5432 \
 postgres:15

run the seed script after the db is ready

```uv run python -m app.scripts.seed_words

```

start server: uv run fastapi dev app/main.py
