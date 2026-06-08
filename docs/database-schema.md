# Database Schema

The database schema is defined in `backend/app/db/models.py` and exposed to Alembic through `backend/alembic/env.py`.

## Core Tables

- `users`: account identity, hashed passwords, role, preferences, timezone.
- `audit_logs`: auth events, workflow changes, tool execution, permission denials.
- `conversations`, `messages`: chat history and assistant messages.
- `agents`, `tools`, `tool_permissions`: registered runtime capabilities and RBAC gates.

## Execution Tables

- `workflow_runs`: high-level autonomous goals, plans, status, result payloads.
- `workflow_steps`: agent-level step tracking.
- `task_runs`: Celery queue jobs, retry state, output, and errors.
- `schedules`: recurring workflow definitions.

## Intelligence Tables

- `memory_items`: user-scoped long-term and semantic memory records.
- `scholarship_opportunities`: normalized opportunity tracking, scoring, deadlines.
- `research_items`: normalized paper/research intelligence tracking.
- `notifications`: dashboard/email/mobile notification state.
- `reports`: generated daily/weekly/productivity/research/scholarship reports.

All user-owned data includes `user_id` and must be accessed through service methods that filter by the current authenticated user.

