"""Celery worker for async tasks: PDF generation, report creation, email sending."""
import os
from celery import Celery

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

celery_app = Celery(
    "carboncove",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.pdf_tasks", "tasks.email_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    worker_max_tasks_per_child=100,
)
