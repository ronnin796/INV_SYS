# inv/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inv.settings')

app = Celery('inv')

# read configuration from Django settings, using CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover tasks from all registered Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
