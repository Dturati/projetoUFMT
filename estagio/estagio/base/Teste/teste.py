from celery import task
from celery.app import shared_task

@shared_task
def teste(valor):
    for r in range(1,valor):
        pass
    return valor
