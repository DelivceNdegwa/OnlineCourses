# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_courses.settings')

app = Celery('online_courses')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Nairobi')

# Auto-discover tasks in all installed apps.
app.autodiscover_tasks()