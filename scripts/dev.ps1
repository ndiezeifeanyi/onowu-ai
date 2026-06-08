$ErrorActionPreference = "Stop"

if (!(Test-Path ".env")) {
  Copy-Item ".env.example" ".env"
  Write-Host "Created .env from .env.example"
}

try {
  docker --version | Out-Null
  docker compose -f infra/docker-compose.yml up --build
} catch {
  Write-Warning "Docker is unavailable. Starting app commands requires external PostgreSQL and Redis."
  Write-Host "Backend:  uv run --project backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
  Write-Host "Frontend: npm.cmd run dev --prefix frontend"
}

