from celery  import (
    Celery,
)

import os


celery_app = Celery(
    'analyzer',
    broker=os.getenv('CELERY_BROKER_URL'),
    include=[
        'app.tasks.user_profile',
    ],
)
