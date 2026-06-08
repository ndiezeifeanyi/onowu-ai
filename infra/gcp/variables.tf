variable "project_id" {
  type        = string
  description = "Google Cloud project id."
}

variable "region" {
  type        = string
  description = "Primary Google Cloud region."
  default     = "europe-west1"
}

variable "database_tier" {
  type        = string
  description = "Cloud SQL instance tier."
  default     = "db-custom-1-3840"
}

variable "artifact_repository" {
  type        = string
  description = "Artifact Registry repository name."
  default     = "personal-ai-os"
}

