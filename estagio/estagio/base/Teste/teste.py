from celery import task,Celery
from celery.app import shared_task
from ...celery import app

@app.task
def teste(valor):
    # print("Vadia")
    for r in range(1,valor):
        pass
    return valor
