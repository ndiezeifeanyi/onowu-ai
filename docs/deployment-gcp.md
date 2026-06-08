# Google Cloud Deployment

The default production region is `europe-west1`.

## Services

- Artifact Registry for backend/frontend images.
- Cloud SQL PostgreSQL for durable state.
- Memorystore Redis for queues and event streams.
- Secret Manager for API keys and credentials.
- HTTPS load balancer for public ingress.
- Cloud Monitoring and Cloud Logging for observability.

## High-Level Steps

1. Create or select a GCP project.
2. Enable Cloud SQL, Memorystore, Artifact Registry, Secret Manager, Compute, and Cloud Monitoring APIs.
3. Build and push images.
4. Apply Terraform in `infra/gcp`.
5. Configure DNS and HTTPS certificates.
6. Run database migrations.
7. Start backend, frontend, worker, and beat services.

## Required Secrets

- `SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `OPENAI_API_KEY`
- Email provider credentials
- Weather provider keys
- Optional Pinecone credentials
