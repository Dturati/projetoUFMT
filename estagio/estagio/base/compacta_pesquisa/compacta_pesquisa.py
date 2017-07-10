import zipfile
from django.http import JsonResponse
import os
from pymongo import MongoClient
def compacta_toda_pesquisa(request):
    #se a pesquisa for especifica
    if(request.session['resultado']):
        request = request.session['resultado']
        arquivos = []
        for r in request:
            arquivos.append(str(r['diretorio']))
        zf = zipfile.ZipFile('pesquisa.zip', "w")

        for fpath in arquivos:
            fdir, fname = os.path.split(fpath)
            zip_subdir = str(fdir)
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(fpath, zip_path)
        zf.close()

        return JsonResponse({'status': 'ok'})

    #se forem todos os arquivos do sistema
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

def compacta_pesquisa_selecionada(request):
    request = request.GET.getlist('data[]')
    arquivos = []

    for r in request:
        arquivos.append(str(os.getcwd() + '/' + r))

    zf = zipfile.ZipFile('pesquisa.zip', "w")
    for fpath in request:
        fdir, fname = os.path.split(fpath)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)
    zf.close()

