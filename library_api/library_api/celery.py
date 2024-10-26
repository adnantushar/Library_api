import os

from django.conf import settings

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_api.settings')

app = Celery('library_api')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule= {
    'archive_old_books' : {
        'task' : 'library.task.archive_old_books',
        'schedule': crontab(minute='*/30'),
    }
}