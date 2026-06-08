# Security Model

## Identity And Access

- JWT access and refresh tokens.
- Argon2 password hashing.
- RBAC roles: owner, admin, member, viewer, agent_service.
- Every user-scoped table stores `user_id` and is filtered through service methods.

## Tool Safety

- Tool execution requires explicit capability metadata.
- Sensitive tools require role checks.
- Tool input is validated by Pydantic schemas.
- Prompt-injection indicators are detected before tool execution.
- File-system tools are confined to approved workspaces.

## Secrets

- Local secrets live in `.env`.
- Production secrets live in GCP Secret Manager.
- Secrets are not returned through API responses or logs.

## Auditability

- Authentication events, tool runs, workflow state changes, and permission denials are audit logged.
- Logs are structured and production-compatible with Cloud Logging.
