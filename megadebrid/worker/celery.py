from os import environ

from celery import Celery

# RESULT_BACKEND = "db+sqlite:///src/worker/results.db" if environ.get("PERSISTENT_BACKEND") else "redis://localhost:6379"


app = Celery(
    "Mega-Celery",
    broker=environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),
    result_backend=environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379"),
    include=["megadebrid.worker.tasks"],
)

# Optional configuration, see the documentation:
#  - result_expires: https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-result_expires

app.conf.update(
    timezone="Europe/Berlin",
    enable_utc=True,
    accept_content=["json"],  # Ignore other content
    task_serializer="json",
    task_track_started=True,
    result_serializer="json",
    result_expires=604800,  # Results expires after 7 days: 604800 seconds
)

if __name__ == "__main__":
    app.start()
