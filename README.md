# Personal AI OS

Personal AI OS is a private multi-user autonomous assistant platform. It combines a FastAPI backend, LangGraph-based orchestration, Celery workers, persistent memory, dynamic tool use, and a Next.js dashboard.

## What Is Included

- FastAPI API under `/api/v1`
- JWT authentication with RBAC
- PostgreSQL data model for users, workflows, tasks, memory, schedules, notifications, reports, scholarships, and research
- Redis/Celery background execution
- LangGraph-ready master orchestration layer
- Dynamic agent and tool registries
- Chroma local vector memory with Pinecone-ready abstraction
- Next.js dashboard for chat, workflows, agents, memory, reports, research, scholarships, and settings
- Docker Compose for local services
- Google Cloud Europe deployment scaffolding

## Local Development

PowerShell blocks `npm.ps1` on this machine, so use `npm.cmd` on Windows.

```powershell
copy .env.example .env
uv sync --project backend
npm.cmd install --prefix frontend
```

If Docker Desktop is installed:

```powershell
docker compose -f infra/docker-compose.yml up --build
```

Without Docker, point `.env` to running PostgreSQL and Redis instances, then run:

```powershell
uv run --project backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
npm.cmd run dev --prefix frontend
```

## Default URLs

- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`
- Chroma: `http://localhost:8001`

## Production Target

The production target is Google Cloud Europe, defaulting to `europe-west1`, with:

- Cloud SQL PostgreSQL
- Memorystore Redis
- Secret Manager
- Artifact Registry
- HTTPS load balancing
- Cloud Monitoring and structured logs

See [docs/deployment-gcp.md](docs/deployment-gcp.md).
