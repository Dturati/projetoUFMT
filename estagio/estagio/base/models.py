from django.db import models
from django.http import HttpResponse
import os,time,re
import os, tempfile, zipfile
from wsgiref.util import FileWrapper
import mimetypes
import zipfile
from io import StringIO
# Create your models here.

'''
import os.path, time
print "last modified: %s" % time.ctime(os.path.getmtime(file))
print "created: %s" % time.ctime(os.path.getctime(file))

'''
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
    def lista_aquivos(pesquisa):
        meuDir = '/arquivos'
        arquivos = []
        diretorio = []
        detalheArquivosModificado = []
        detalheArquivosCriados = []
        tempo =''
        for root,dirs,files in os.walk('.',topdown=False):
            for f in files:
                if(re.match(f,pesquisa)):
                    detalheArquivosModificado.append(time.ctime(os.path.getmtime(root + '/' + f)))
                    detalheArquivosCriados.append(time.ctime(os.path.getctime(root + '/' + f)))
                    arquivos.append(f)
                    diretorio.append(str(root)+"/"+f)
        return arquivos,diretorio,detalheArquivosCriados,detalheArquivosModificado

class Download:
    def getDownload(self, request, path):
        nome_arquivo = os.getcwd() + "/" + path
        print(nome_arquivo)
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
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            # Add file, at correct path
            zf.write(fpath)
        #
        # # Must close zip for all contents to be written
        zf.close()
        #
        # # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), mimetype="application/x-zip-compressed")
        # # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp

