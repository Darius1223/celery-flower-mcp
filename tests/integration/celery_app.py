import time

from celery import Celery

app = Celery(
    "integration_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)
app.conf.update(task_track_started=True)


@app.task(name="tasks.add")
def add(x: int, y: int) -> int:
    return x + y


@app.task(name="tasks.sleep")
def sleep(seconds: float) -> str:
    time.sleep(seconds)
    return "done"
