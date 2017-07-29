from __future__ import absolute_import
import zipfile
import os
from pymongo import MongoClient
from celery import shared_task
import json

@shared_task
def compacta_toda_pesquisa_individual(request,chave):
    # #se a pesquisa for especifica
    arquivos = []
    request = json.loads(request)
    for value in request:
        arquivos.append(str("../arquivos"  + '/' + value['diretorio'] + '/' +value['arquivo']))
    zf = zipfile.ZipFile(str(chave['chave'])+".zip", "w")
    for value in arquivos:
        fdir, fname = os.path.split(value)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, value)
        zf.write(value, zip_path)
    zf.close()
    request = json.dumps(request)
    return request

@shared_task
def compacta_toda_pesquisa_completa(request,chave):
    # #se forem todos os arquivos do sistema
    cliente = MongoClient('localhost', 27017)
    banco = cliente.test_database
    dados_db = banco.teste
    resultado = dados_db.find()
    arquivos = []
    for value in resultado:
        arquivos.append(str("../arquivos"  + '/' + value['diretorio'] + '/' +value['arquivo']))
    zf = zipfile.ZipFile(str(chave['chave'])+".zip", "w")
    for value in arquivos:
        fdir, fname = os.path.split(value)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, value)
        zf.write(value, zip_path)
    zf.close()
    request = json.dumps(request)
    return request

# @shared_task
def compacta_pesquisa_selecionada(request,chave):
    arquivos = []
    request = json.loads(request)
    for value in request:
        arquivos.append(str("../arquivos" + '/' + value))
    zf = zipfile.ZipFile(chave['chave']+".zip", "w")
    for value in request:
        fdir, fname = os.path.split(value)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(value, zip_path)
    zf.close()
    request = json.dumps(request)
    return request


