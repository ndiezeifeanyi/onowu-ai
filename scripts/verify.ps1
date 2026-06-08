$ErrorActionPreference = "Stop"

Write-Host "Checking local toolchain..."

$commands = @(
  @{ Name = "python"; Args = "--version" },
  @{ Name = "uv"; Args = "--version" },
  @{ Name = "node"; Args = "--version" },
  @{ Name = "npm.cmd"; Args = "--version" },
  @{ Name = "git"; Args = "--version" }
)

foreach ($command in $commands) {
  try {
    & $command.Name $command.Args | Out-Host
  } catch {
    Write-Error "$($command.Name) is missing or unavailable."
  }
}

try {
  docker --version | Out-Host
} catch {
  Write-Warning "Docker is not available on PATH. Install Docker Desktop for full local orchestration."
}

try {
  gcloud --version | Select-Object -First 1 | Out-Host
} catch {
  Write-Warning "gcloud is not available on PATH. Install Google Cloud CLI before cloud deployment."
}

Write-Host "Repository verification complete."

