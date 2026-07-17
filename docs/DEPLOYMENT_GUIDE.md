# Deployment Guide

## Local

Run backend and frontend separately during development. SQLite is the default database.

## Docker Compose

```bash
docker compose up --build
```

## Production Notes

- Replace `SECRET_KEY`.
- Use PostgreSQL through `DATABASE_URL`.
- Mount durable upload storage.
- Put TLS termination in front of Nginx/FastAPI.
- Run Alembic migrations before app rollout.
- Add background workers when OCR latency blocks API request budgets.

## Backup

Back up database and upload storage at the same snapshot point.

