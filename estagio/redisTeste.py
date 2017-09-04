from estagio.celery import app
res = app.control.revoke('c628cc63-2d57-4759-b3f2-884db5f9015b',terminate=True,signal='SIGKILL')
print(res)