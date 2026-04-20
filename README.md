# SupportSaaS - Production-Ready Project

This is an end-to-end, production-style implementation of the project:
**AI-powered multi-tenant customer support SaaS**.

## What is included

- Multi-tenant architecture (`Tenant`, `User`, `Ticket`) with strict tenant-level data isolation.
- JWT authentication with secure password hashing.
- Ticket lifecycle API (create/list/update).
- Async AI suggestion generation via Celery + Redis worker.
- End-to-end web dashboard served by FastAPI static UI.
- Dockerized services for API, worker, PostgreSQL, and Redis.
- CI workflow with automated tests.

## Tech stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis + Celery
- Docker / Docker Compose
- GitHub Actions

## Quick start (local)

1. Copy env file:

   ```bash
   cp .env.example .env
   ```

2. Run all services:

   ```bash
   docker compose up --build
   ```

3. Open:

   - App UI: [http://localhost:8000](http://localhost:8000)
   - Health: [http://localhost:8000/health](http://localhost:8000/health)
   - API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API overview

- `POST /api/v1/tenants` - create tenant
- `POST /api/v1/auth/register` - register tenant user
- `POST /api/v1/auth/login` - get access token
- `GET /api/v1/tickets` - list tenant tickets
- `POST /api/v1/tickets` - create ticket (AI suggestion generated async)
- `PATCH /api/v1/tickets/{ticket_id}` - update status/priority/assignee

## Deploy to repository

### Option A: GitHub CLI

```bash
git init
git add .
git commit -m "feat: production-ready AI support SaaS project"
gh repo create support-saas-cv-project-one --private --source . --remote origin --push
```

### Option B: Manual remote

```bash
git init
git add .
git commit -m "feat: production-ready AI support SaaS project"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

## Production hardening checklist

- Replace `SECRET_KEY` and use a secret manager.
- Switch to managed PostgreSQL and Redis in production.
- Add DB migrations (Alembic) and backup strategy.
- Replace AI stub in `app/services/ai.py` with real OpenAI integration.
- Add request rate limiting and audit logging.
- Add monitoring/alerts (Sentry, Prometheus, Grafana).
