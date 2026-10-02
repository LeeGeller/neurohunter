import os

from celery import (
    Celery,
)


celery_app = Celery(
    'analyzer',
    broker=os.getenv('CELERY_BROKER_URL'),
    include=[
        'app.api.tasks.user_profile',
        'app.api.tasks.resume',
        'app.api.tasks.search_vacancies'
    ],
)

celery_app.conf.update(
    control_queue_exclusive=True,
    event_queue_exclusive=True,
)
