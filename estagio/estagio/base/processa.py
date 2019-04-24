from django.http import HttpResponse
import time,re
import os
from wsgiref.util import FileWrapper
import mimetypes
import zipfile
from io import StringIO
from pymongo import MongoClient
from django.conf import settings


class ListaArquivos:
    def list_files(startpath):
        detalheArquivosModificado = []
        detalheArquivosCriados = []
        detalhePastaCriadas = []
        detalhePastaModificadas = []

        for root, dirs, files in os.walk(startpath):
            for r in files:
                detalheArquivosModificado.append(time.ctime(os.path.getmtime(root+'/'+r)))
                detalheArquivosCriados.append(time.ctime(os.path.getctime(root+'/'+r)))

            for r in dirs:
                detalhePastaModificadas.append(time.ctime(os.path.getmtime(root+'/'+r)))
                detalhePastaCriadas.append(time.ctime(os.path.getctime(root+'/'+ r)))

            return dirs,files,detalheArquivosModificado,detalheArquivosCriados,detalhePastaModificadas,detalhePastaCriadas

class PesquisaArquivos:
    '''0000000030-35-seq-_13_0.4-1.csv'''
    def lista_arquivos(pesquisa):
        # print("lista arquivos")

        m_regex = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
        arquivos = []

        cliente = MongoClient('localhost', 27017)
        banco = cliente.test_database
        dados_db = banco.teste

        filtro = {}
        percent = {}
        if(pesquisa.get('porcentagem_um','') != ""):
            percent['$gte'] = int(pesquisa.get('porcentagem_um'))

        if(pesquisa.get('porcentagem_dois','') != ""):
            percent['$lte'] = int(pesquisa.get('porcentagem_dois'))

        if(percent):
            filtro['percent'] = percent

        if(pesquisa.get('tipoFalha','') != ""):
            filtro['type'] = pesquisa.get('tipoFalha','')

        if(pesquisa.get('falha_conjunto','') != ""):
            conjunto = int(pesquisa.get('falha_conjunto'))
            if(conjunto>=4):
                filtro['column'] = {'$gte':conjunto}
            else:
                filtro['column'] = conjunto

        resultado = dados_db.find(filtro)

        return resultado

class Download:
    def getDownload(self, request, path):
        nome_arquivo = os.getcwd() + "/" + path
        nome_download = os.getcwd() + "/" + path + ".csv"
        wrapper = FileWrapper(open(nome_arquivo))
        content_type = mimetypes.guess_type(nome_arquivo)[0]
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(nome_arquivo)
        response['Content-Disposition'] = "attachment; filename=%s" % nome_download
        return response

class Compacta_aquivos():
    def getArquivosCompactados(self):
        arquivos = [str(os.getcwd() + '/' + 'arquivos/' '123.csv')]
        zip_subdir = 'estagio'
        zip_filename = "%s.zip" % zip_subdir
        s = StringIO()
        zf = zipfile.ZipFile('pesquisa.zip', "w")

        for fpath in arquivos:
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(fpath)
        zf.close()
        resp = HttpResponse(s.getvalue(), mimetype="application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp

class sincroniza():
    pass

