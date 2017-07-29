import os
import subprocess
def iniciaServido():
    dir = os.getcwd()
    # subprocess.call('python3 manage.py')
    os.system('python3 manage.py runserver')
    os.system("redis-server")

iniciaServido()