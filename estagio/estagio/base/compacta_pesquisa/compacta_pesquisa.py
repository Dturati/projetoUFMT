from __future__ import absolute_import
import zipfile
from django.http import JsonResponse
import os
from pymongo import MongoClient
from celery import shared_task
from celery import task
from estagio.celery import app
import json

@shared_task
def compacta_toda_pesquisa(request):
    # #se a pesquisa for especifica
    if(request):
        arquivos = []
        request = json.loads(request)
        for value in request:
            arquivos.append(str(os.getcwd() + '/'+value['diretorio']))
        zf = zipfile.ZipFile('pesquisa.zip', "w")
        for value in request:
            fdir, fname = os.path.split(value['diretorio'])
            zip_subdir = str(fdir)
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(value['diretorio'], zip_path)
        zf.close()
        request = json.dumps(request)
        return request

    # #se forem todos os arquivos do sistema
    cliente = MongoClient('localhost', 27017)
    banco = cliente.test_database
    dados_db = banco.teste
    resultado = dados_db.find()
    arquivos = []
    for r in resultado:
        arquivos.append(r['diretorio'])
    zf = zipfile.ZipFile('pesquisa.zip', "w")
    for fpath in arquivos:
        fdir, fname = os.path.split(fpath)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)
    zf.close()
    request = json.dumps(request)
    return request
@shared_task
def compacta_pesquisa_selecionada(request):
    arquivos = []
    request = json.loads(request)
    for value in request:
        arquivos.append(str(os.getcwd() + '/' + value))
    zf = zipfile.ZipFile('pesquisa.zip', "w")
    for value in request:
        fdir, fname = os.path.split(value)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(value, zip_path)
    zf.close()
    request = json.dumps(request)
    return request

