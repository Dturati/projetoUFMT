from __future__ import absolute_import
import zipfile
import os
from pymongo import MongoClient
from celery import shared_task
import json
import asyncio
from pymongo import MongoClient
import time
from estagio.celery import app
from django.conf import settings
import time
from estagio.base.Email.email import send_email

@app.task
def compacta_toda_pesquisa(request,chave,email):
    os.chdir(settings.COMPACTA_URL)
    # #se a pesquisa for especifica
    arquivos = []
    request = json.loads(request)
    cliente = MongoClient('localhost', 27017)
    banco = cliente.fila_download
    dados_db_fila = banco.fila
    zf = zipfile.ZipFile(str(chave['chave'])+".zip", "w")
    print('Compactando: ' + str(chave['chave']))
    imprime = 0
    for valor in request:
        value = str(valor['diretorio'] + '/' +valor['arquivo'])
        if(imprime < 10):
            print(value,';', settings.MEDIA_URL,';',value.replace(settings.MEDIA_URL,''))
            imprime = imprime + 1

        fdir, fname = os.path.split(value.replace(settings.MEDIA_URL,''))
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, value)
        zf.write(value, zip_path)
    zf.close()
    print('Compactado: ' + str(chave['chave']))
    request = json.dumps(request)
    dados_db_fila.update({'_id': str(chave['chave'])}, {"status": "download"}, upsert=False)
    send_email(email, chave)
    return request

# @shared_task
def compacta_pesquisa_selecionada(request,chave):
    os.chdir(settings.COMPACTA_URL)
    arquivos = []
    request = json.loads(request)
    for value in request:
        arquivos.append(value)
    zf = zipfile.ZipFile(chave['chave']+".zip", "w")
    for value in arquivos:
        fdir, fname = os.path.split(value.replace(settings.MEDIA_URL,''))
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(value, zip_path)
    zf.close()
    request = json.dumps(request)
    return request

@app.task
def fila_de_dowload(chave):
    try:
        arq = os.getcwd() + "/" + str(chave['chave']) + ".zip"
        file = open(arq, 'r')
        while (file):
            file = open(arq, 'r')
    except:
        pass
    return True

