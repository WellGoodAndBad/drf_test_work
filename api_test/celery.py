from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_test.settings')
app = Celery('api_test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parse-data-one-time-hour': {
        'task': 'api_test_work.tasks.parse_task',
        'schedule': crontab(minute='*/60'),
    },
}