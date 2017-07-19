from __future__ import absolute_import
from celery import shared_task
from estagio.celery import app


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def add(r):
    for r in range(1, int(r)):
        pass
    return int(r)

