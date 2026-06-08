# Architecture

Personal AI OS uses a control-plane/data-plane split.

## Control Plane

- FastAPI exposes authenticated APIs.
- The master agent plans workflows and delegates to specialized agents.
- Agent and tool registries keep capabilities discoverable.
- RBAC, audit logging, rate limits, and tool permissions gate every sensitive action.

## Data Plane

- PostgreSQL stores durable state.
- Redis stores queues, rate-limit counters, workflow event streams, and short-lived context.
- Celery executes long-running work across named queues.
- Chroma stores local semantic memory vectors.
- Pinecone can be used in cloud by switching `VECTOR_PROVIDER`.

## Workflow Execution

1. A user creates a chat message, agent run, schedule, or workflow.
2. The API persists the request and enqueues work.
3. The master agent creates a plan and selects specialized agents/tools.
4. Workers execute steps with retries and state transitions.
5. Outputs are evaluated, stored in memory, and streamed as workflow events.
6. Reports and notifications are generated when configured.

## Offline Mode

Offline mode uses Ollama, cached memory, local files, and local services. External tools such as email, cloud APIs, and live web search return degraded-but-explicit results instead of silently failing.
