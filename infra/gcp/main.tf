terraform {
  required_version = ">= 1.7.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "containers" {
  location      = var.region
  repository_id = var.artifact_repository
  description   = "Personal AI OS containers"
  format        = "DOCKER"
}

resource "google_sql_database_instance" "postgres" {
  name             = "personal-ai-os-postgres"
  region           = var.region
  database_version = "POSTGRES_16"

  settings {
    tier              = var.database_tier
    availability_type = "ZONAL"
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
    }

    ip_configuration {
      ipv4_enabled = false
    }
  }
}

resource "google_sql_database" "database" {
  name     = "personal_ai_os"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "app" {
  name     = "personal_ai_os"
  instance = google_sql_database_instance.postgres.name
  password = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "google_redis_instance" "redis" {
  name           = "personal-ai-os-redis"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = var.region
  redis_version  = "REDIS_7_0"
}

resource "google_secret_manager_secret" "secret_key" {
  secret_id = "personal-ai-os-secret-key"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "openai_api_key" {
  secret_id = "personal-ai-os-openai-api-key"
  replication {
    auto {}
  }
}
