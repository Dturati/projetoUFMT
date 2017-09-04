from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estagio.settings')

# app = Celery('tasks',backend='amqp',broker = 'amqp://david:123@192.168.15.11/amd')

app = Celery('estagio')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))