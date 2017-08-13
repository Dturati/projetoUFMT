from __future__ import absolute_import,unicode_literals
from celery import shared_task
from estagio.celery import app
from celery import task

def yielder():
    for i in range(2**100):
        yield i

@shared_task
def report_progress():
    for progress in yielder():
        # set current progress on the task
        report_progress.backend.mark_as_started(
            report_progress.request.id,
            progress=progress)

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@task
def add(r):
    for r in range(1, int(r)):
        pass
    return int(r)

