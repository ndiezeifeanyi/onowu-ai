from app.core.logging import get_logger

logger = get_logger(__name__)


def audit_log(user_id: str | None, path: str, status_code: int) -> None:
    logger.info("audit.log", extra={"user_id": user_id, "path": str(path), "status": status_code})
