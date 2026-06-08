output "artifact_registry_repository" {
  value = google_artifact_registry_repository.containers.name
}

output "postgres_instance" {
  value = google_sql_database_instance.postgres.connection_name
}

output "redis_host" {
  value = google_redis_instance.redis.host
}

