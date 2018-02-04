from django.http import HttpResponse
import time,re
import os
from wsgiref.util import FileWrapper
import mimetypes
import zipfile
from io import StringIO
from pymongo import MongoClient


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
    def lista_aquivos(pesquisa):
        # print("lista arquivos")
        try:
            todosOsArquivos = pesquisa['todosOsArquivos']
        except:
            todosOsArquivos = ""

        m_regex = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
        arquivos = []
        if(todosOsArquivos == ""):
            meuDir = '/arquivos'
            arquivos = []
            m_regex             = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
            regex_falha = ''
            porcentagem_um      =   int(pesquisa['porcentagem_um'])
            porcentagem_dois    =   int(pesquisa['porcentagem_dois'])

            tipoFalha = pesquisa['tipoFalha']
            metodo = pesquisa['metodoUtilizado']
            fala_conjunto = pesquisa['falha_conjunto']
            vetorFalha = []
            vetorFalha.append("(")
            porcentagemFalha = porcentagem_um
            while(porcentagemFalha <= porcentagem_dois):
                vetorFalha.append(porcentagemFalha)
                if(porcentagemFalha == porcentagem_dois):
                    vetorFalha.append(")")
                    break
                porcentagemFalha = porcentagemFalha + 1
                vetorFalha.append("|")
            for r in vetorFalha:
                regex_falha = regex_falha+str(r)
            regex_falha_conjunto = ""

            if(int(fala_conjunto) < 4):
                # print(fala_conjunto)
                regex_falha_conjunto = '(' +fala_conjunto+ ')' + '.' + '[0-9]'

            if(int(fala_conjunto) >= 4):
                # print(fala_conjunto)
                regex_falha_conjunto = '['+fala_conjunto+ '-9]'

            m_regex = m_regex+"-"+regex_falha+"-"+tipoFalha+"-_13_+"+regex_falha_conjunto+"-"+metodo+"[.]csv"
            # print(m_regex)
            # print(re.search(m_regex,'0000014026-18-ale-_13_1-2.csv'))
        cliente = MongoClient('localhost', 27017)
        banco = cliente.test_database
        dados_db = banco.teste
        resultado = dados_db.find()

        for f in resultado:
            if(re.search(m_regex,f['arquivo'])):
                arquivos.append({'arquivo':f['arquivo'],'criado':f['criado'],'modificado':f['modificado'],'diretorio':f['diretorio']})
        return arquivos

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

