import os

from celery import (
    Celery,
)


celery_app = Celery(
    'analyzer',
    broker=os.getenv('CELERY_BROKER_URL'),
    include=[
        'app.api.tasks.user_profile',
    ],
)

celery_app.conf.update(
    control_queue_exclusive=True,
    event_queue_exclusive=True,
)
