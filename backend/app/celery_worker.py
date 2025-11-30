from celery import Celery

celery_app = Celery(
    'worker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['app.tasks.email']
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)