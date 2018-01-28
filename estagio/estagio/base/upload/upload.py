import zipfile
import os
from ..ScriptR.scriptR import executaScript
import shutil
import random
from ...celery import app
from celery import shared_task
from celery import Task

class Upload():

    def upload(self,myfile):
        rashZip = str(random.getrandbits(32))
        os.chdir("/")
        with(open("arquivos/arquivos/uploads/fila.txt",'w')) as fila:
            fila.write(str(rashZip+"\n"))

        with open('arquivos/arquivos/uploads/'+myfile.name, 'wb+') as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)
        try:
            os.chdir("/")
            path = str(os.getcwd())+"arquivos/arquivos/uploads/"
            zip_ref = zipfile.ZipFile(str(os.getcwd()) + "aquivos/arquivos/uploads/" + str(myfile.name), 'r')
            zip_ref.extractall(str(os.getcwd()) + "arquivos/arquivos/uploads/"+str(rashZip))
            zip_ref.close()
        except:
            print("erro")

        os.remove(str(os.getcwd()) + "arquivos/arquivos/uploads/" + str(myfile.name))
        res = executaScript.delay(rashZip)

        return rashZip,True,"Arquivos enviados",str(res.id)
        # return rashZip,True,"Arquivos enviados","123"

    def download(self,myfile):

        raiz = os.getcwd()
        shutil.rmtree(raiz + "estagio/arquivos/upload/" + myfile)
        return True

