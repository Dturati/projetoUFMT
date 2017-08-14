from __future__ import absolute_import
import zipfile
import os
from pymongo import MongoClient
from celery import shared_task
import json
import asyncio
from pymongo import MongoClient

@shared_task
def compacta_toda_pesquisa_individual(request,chave):
    # #se a pesquisa for especifica
    arquivos = []
    request = json.loads(request)
    cliente = MongoClient('localhost', 27017)
    banco = cliente.fila_download
    dados_db_fila = banco.fila

    for value in request:
        arquivos.append(str(value['diretorio'] + '/' +value['arquivo']))
    zf = zipfile.ZipFile(str(chave['chave'])+".zip", "w")

    for value in arquivos:
        fdir, fname = os.path.split(value)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, value)
        zf.write(value, zip_path)
    zf.close()
    request = json.dumps(request)
    dados_db_fila.update({'_id': str(chave['chave'])}, {"status": "download"}, upsert=False)
    resultado = dados_db_fila.find({'_id': str(chave['chave'])})
    res = [r for r in resultado]
    try:
        arq = os.getcwd() + "/" + str(chave['chave']) + ".zip"
        file = open(arq, 'r')
        while (file):
            file = open(arq, 'r')
            print("arquivo ainda existe")
    except:
        print("arquivo deletado")
        # dados_db_fila.drop({"_id":str(chave['chave'])})

    return request

@shared_task
def compacta_toda_pesquisa_completa(request,chave):
    # #se forem todos os arquivos do sistema
    cliente = MongoClient('localhost', 27017)
    banco = cliente.test_database
    dados_db = banco.teste
    resultado = dados_db.find()

    banco = cliente.fila_download
    dados_db_fila = banco.fila

    arquivos = []
    for value in resultado:
        arquivos.append(str(value['diretorio'] + '/' +value['arquivo']))
    zf = zipfile.ZipFile(str(chave['chave'])+".zip", "w")
    for value in arquivos:
        fdir, fname = os.path.split(value)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, value)
        zf.write(value, zip_path)
    zf.close()

    #manter flag no banco indicando o arquivo foi posto para Download
    dados_db_fila.update({'_id': str(chave['chave'])}, {"status": "download"}, upsert=False)
    resultado = dados_db_fila.find({'_id': str(chave['chave'])})
    res = [r for r in resultado]
    request = json.dumps(request)
    try:
        arq = os.getcwd() + "/" + str(chave['chave']) + ".zip"
        file = open(arq, 'r')
        #Manter usuário na fila enquanto o Download não terminar e o arquivo não for apagado
        while (file):
            file = open(arq, 'r')
            print("arquivo ainda existe")
    except:
        print("aquivo deletado")
    return request

# @shared_task
def compacta_pesquisa_selecionada(request,chave):
    arquivos = []
    request = json.loads(request)
    for value in request:
        arquivos.append(value)
    zf = zipfile.ZipFile(chave['chave']+".zip", "w")
    for value in arquivos:
        fdir, fname = os.path.split(value)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(value, zip_path)
    zf.close()
    request = json.dumps(request)
    return request

@shared_task
def fila_de_dowload(chave):
    try:
        arq = os.getcwd() + "/" + str(chave['chave']) + ".zip"
        file = open(arq, 'r')
        while (file):
            file = open(arq, 'r')
    except:
        pass
    return True

