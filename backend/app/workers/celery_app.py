from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "personal_ai_os",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_track_started=True,
    worker_prefetch_multiplier=1,
    task_routes={
        "workflows.run": {"queue": "agents"},
        "reports.generate": {"queue": "reports"},
        "scholarships.scan": {"queue": "scholarships"},
        "research.scan": {"queue": "research"},
        "notifications.dispatch": {"queue": "notifications"},
        "browser.run": {"queue": "browser"},
    },
    beat_schedule={
        "daily-scholarship-scan": {
            "task": "scholarships.scan",
            "schedule": 60 * 60 * 24,
        },
        "daily-briefing": {
            "task": "reports.generate",
            "schedule": 60 * 60 * 24,
        },
    },
)

