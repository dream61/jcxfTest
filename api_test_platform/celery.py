from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import Settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_test_platform.settings')

app = Celery('api_test_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
