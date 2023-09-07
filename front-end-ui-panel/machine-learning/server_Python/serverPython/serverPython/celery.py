import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serverPython.settings')
app = Celery('serverPython')
app.config_from_object('django.conf:settings', namespace='CELERY')
 
app.conf.timezone = 'Europe/London'
 
app.conf.beat_schedule = {
    "every_thirty_seconds": {
        'task': 'task.scrape_tweet',
        'schedule': crontab(minute='30'),
    },
}
 
app.autodiscover_tasks()