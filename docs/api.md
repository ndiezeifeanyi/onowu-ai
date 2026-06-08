# API Overview

All endpoints live under `/api/v1`.

## Auth

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`

## Agents And Workflows

- `GET /agents`
- `POST /agents/{agent_id}/runs`
- `POST /workflows`
- `GET /workflows`
- `GET /workflows/{id}`
- `POST /workflows/{id}/cancel`
- `GET /events/workflows/{workflow_id}`

## Memory

- `POST /memory/items`
- `GET /memory/items`
- `POST /memory/search`

## Operations

- `GET /tasks`
- `GET /tasks/{id}`
- `POST /tasks/{id}/retry`
- `GET /tools`
- `POST /tools/{tool_id}/execute`
- `POST /schedules`
- `GET /schedules`
- `PATCH /schedules/{id}`
- `GET /notifications`
- `POST /notifications/test`
- `GET /reports`
- `POST /reports/generate`
