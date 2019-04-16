from django.core.serializers import json
from django.conf import settings
from django.http import JsonResponse
from .processa import ListaArquivos,PesquisaArquivos
import os,time
from .form import Pesquisa
from .processa import Download
from django.shortcuts import render
from django.core.paginator import Paginator
from estagio.base.lista_arvore.lista_arvore import lista_arvore
from estagio.base.compacta_pesquisa.compacta_pesquisa import compacta_toda_pesquisa_individual,\
    compacta_toda_pesquisa_completa,compacta_pesquisa_selecionada
import json
import hashlib
from random import choice
# from .task import add,report_progress
from estagio.celery import app as meu_celery
from .Email.email import send_email
import requests
import random
from django.core.files.storage import FileSystemStorage
from pymongo import MongoClient
lista_arquivos = ListaArquivos
resutadopesquisaPaginado = []
from .MongoDB.MongoCennect import MongoConnect


from estagio.celery import app

import sys


def home(request):
    form = Pesquisa(request.POST)
    try:
        if(not request.session['tipo_requisicao']):
            request.session['tipo_requisicao_'] = 'todos_os_arquivos'
    except:
        request.session['tipo_requisicao'] = 'todos_os_arquivos'

    num = int(request.GET.get('page', 1))

    resultadoPesquisa = []
    #if(request.session['tipo_requisicao'] == 'todos_os_arquivos'):
    # Verifica se é uma paginação ou submição de formulario
    con = MongoConnect()
    banco = con.connect("test_database")
    dados_db = banco.teste
    consulta = dados_db.find()
    print(consulta)
    try:
        P = Paginator(list(consulta),8)
        pagina = P.page(num)
    except:
        pagina = P.page(1)

    contexto = {
        'form': form,
        'resultadoPesquisa': resultadoPesquisa,
        'quantidade': pagina.paginator.num_pages * 8,
        'paginado': pagina,
    }
    return render(request, "home.html", contexto)

    '''if (request.session['tipo_requisicao'] == 'pesquisa_individual'):
        if(request.POST):
            resultadoPesquisa = pesquisa(form.data)
            request.session['form'] = form.data
            # print(resultadoPesquisa[0]['diretorio'])
        else:
            try:
                resultadoPesquisa = pesquisa(request.session['form'])
            except:
                pass

        try:
            P = Paginator(resultadoPesquisa,8)
            pagina = P.page(num)
        except:
            pagina = P.page(1)
        contexto = {
                        'form': form,
                        'resultadoPesquisa': resultadoPesquisa,
                        'quantidade': pagina.paginator.num_pages * 8,
                        'paginado': pagina,
                    }
        return render(request, "home.html", contexto)
	'''

def contatos(request):
    return render(request,"contatos.html",{"teste":"teste"})

def pesquisa(dados):
    pesquisa_arquivos = PesquisaArquivos
    meuDir = settings.MEDIA_URL + '/arquivos'
    resultadoPesquisa  = pesquisa_arquivos.lista_aquivos(dados)
    return resultadoPesquisa

from django.http import HttpResponse
#lista arquivos em forma de arvores
def lista_em_arvore(request):
    arquivosJson = JsonResponse(lista_arvore(request))
    return arquivosJson

#Faz download de um único  arquivo
def download(request,path):
    downloadModel = Download()
    return downloadModel.getDownload(request,path)

#compacta pesquisa selecionada
def view_compacta_pesquisa_selecionada(request):
    dados = request.GET.getlist('data[]')
    teste = json.dumps(dados)
    chave = str(random.getrandbits(128))
    chaveJ = {'chave': chave}
    res = compacta_pesquisa_selecionada(teste,chaveJ)
    return JsonResponse({'status':'ok','id':'','chave':chave})

#compacta toda pesquisas
def view_compacta_toda_pesquisa(request):
    dados = {}
    chave = str(random.getrandbits(128))

    if(request.session['tipo_requisicao'] == 'todos_os_arquivos'):
        chaveJ = {'chave': chave}
        con = MongoConnect()
        banco = con.connect("fila_download")
        dados_db_fila = banco.fila

        value = {
            "_id": chave,
            "status": "compactando"
        }
        dados = dados_db_fila.insert_one(value).inserted_id
        res = compacta_toda_pesquisa_completa.delay(1,chaveJ)
        # fila_de_dowload.delay(chaveJ)


    if (request.session['tipo_requisicao'] == 'pesquisa_individual'):
        resultadoPesquisa = pesquisa(request.session['form'])
        dadosRequest = json.dumps(resultadoPesquisa)
        chave = str(random.getrandbits(128))
        chaveJ = {'chave':chave}
        try:
            con = MongoConnect()
            banco = con.connect("fila_download")
        except:
            pass
            # print('Erro ao conectar')

        dados_db_fila = banco.fila
        value = {
            "_id": str(chave),
            "status": "compactando"
        }

        dados = dados_db_fila.insert_one(value).inserted_id
        res = compacta_toda_pesquisa_individual.delay(dadosRequest,chaveJ)
    return JsonResponse({'status': 'ok','id':res.id,'chave':chave})

#Baixa os arquivos compactados
import mimetypes
from django.http import StreamingHttpResponse
# from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
def baixar_pesquisa(request):
    dados = request.GET
    # os.chdir("/home/david/Documentos/projeto_estagio_django/estagio")
    os.chdir(settings.MEDIA_URL + "/arquivos")
    nome_arquivo = os.getcwd() + "/" + str(dados['chave'])+".zip"
    filename = os.path.basename(nome_arquivo)
    nome_download = str(dados['chave'])+".zip"
    try:
        response = HttpResponse(open(nome_arquivo,'rb').read(), content_type='x-zip-compressed')
        response['Content-Disposition'] = "attachment; filename=%s" % nome_download
        # chunk_size = 8192
        # response = StreamingHttpResponse(FileWrapper(open(nome_arquivo, 'rb'), chunk_size),
        #                                  content_type=mimetypes.guess_type(nome_arquivo)[0])
        # response['Content-Length'] = os.path.getsize(nome_arquivo)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # response['Content-Disposition'] = "attachment; filename=" % filename
        os.remove(nome_arquivo)
    except:
        return render(request,"home.html",{})
    try:
        # send_email(request.session['email'])
        pass
    except:
        pass
    return response


def define_sessao(request):
    status = request.GET
    if(status['status'] == 'desativado'):
        request.session['tipo_requisicao'] = 'todos_os_arquivos'
    else:
        request.session['tipo_requisicao'] = 'pesquisa_individual'
    return JsonResponse({'status': 'ok'})


def requisicao_enviada(request):
    quantidade_arquivos = request.GET['quantidade']
    try:
        request.session['email'] = request.GET['email']
    except:
        pass
    return render(request,"requisicao_enviada.html",{"qtdArquivos":quantidade_arquivos})

#sistema de upload
from .upload.upload import Upload
def upload(request):
    # verifica = VerificaUpload()
    instUpload =  Upload()
    constrole_upload = 0
    if(request.method == 'POST'):
        try:
            request.FILES['myfile']
        except:
            return render(request, "upload.html",{"resposta":"Escolha Um Arquivo"})

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        rashZip, sucess, uploaded_file_url, idTask = instUpload.upload(myfile)

        if(sucess):
            context = {
                    'uploaded_file_url': uploaded_file_url,
                    'status' : 'OK',
                    'file':myfile,
                    'rashZip': rashZip,
                    'idTask' :idTask,
            }
            return render(request, 'upload.html',context)

    return render(request,"upload.html",{'status':'erro'})

from .upload.upload import Upload
from django.http import HttpResponseRedirect
def DownloadUpload(request,file):
    if(file==""):
        return HttpResponseRedirect("/home/")
    dados = request.GET
    os.chdir("/")
    nome_arquivo = settings.MEDIA_URL + "/arquivos/uploads/"+str(file)+".zip"
    nome_download = str(file)+".zip"
    try:
        response = HttpResponse(open(nome_arquivo, 'rb').read(), content_type='x-zip-compressed')
        response['Content-Disposition'] = "attachment; filename=%s" % nome_download
        os.remove(nome_arquivo)
    except:
        return HttpResponseRedirect("/home/")
    return response


#Gerar exibe grafico gerado pelo R
from .Gerar_grafico.Gerar_grafico import GeraArquivoParaGraficoEmR
def gerarGrafico(request):
    os.chdir("/")
    with open("arquivos/arquivos/uploads/grafico/BoxplotVar/R2/metodo_R2.png", "rb") as plot:
        imagem = plot.read()
    response = HttpResponse(imagem, content_type="image/jpg")
    return response

from rpy2.robjects.packages import importr
from rpy2.robjects.packages import STAP,STF
hydro = importr("hydroGOF")

def exemplo(request):
    os.chdir("/")
    with open(os.getcwd() + "/arquivos/uploads/grafico.R", "r") as r:
        string = r.read()
    # print(string)
    try:
     fun = STAP(string, "grafico")
    except:
        pass
    return HttpResponse("Exemplo")

#Um teste usando o Celery
from .Teste.teste import teste
def exemplo_assinc(request):
    valor = request.GET['valor']
    teste.delay(int(valor))
    return HttpResponse("Pronto")

def get_resultado(request):
    dados = request.GET
    res = app.AsyncResult(dados['id'])
    return JsonResponse({'status':res.status})

#Retorna o status do id na fila
def status_stak_celery(request):
    dados = request.GET
    url = "http://localhost:5555/api/tasks"
    resposta = requests.get(url)
    resultadoJson = json.loads(resposta.content.decode('utf-8'))
    return JsonResponse({'id':dados['id'],'tasks':resultadoJson[dados['id']],'total_tasks':resultadoJson})

#retorna o status completo da fila
def fila_celery(request):
    url = "http://localhost:5555/api/tasks"
    resposta = requests.get(url)
    resultadoJson = json.loads(resposta.content.decode('utf-8'))
    return JsonResponse({'total_tasks':resultadoJson})

# from celery import app
def cancelar_requisicao(request):
    os.chdir(settings.MEDIA_URL)
    dadosRequest = request.GET
    url = "http://localhost:5555/api/task/revoke/"+str(dadosRequest['id'])+"?terminate=true"
    resposta = requests.post(url)
    con = MongoConnect()
    banco = con.connect("fila_download")
    dados_db_fila = banco.fila
    dado = dados_db_fila.update({'_id': str(dadosRequest['chave'])}, {"status": "cancelado"}, upsert=False)
    try:
        os.remove(dadosRequest['chave']+".zip")
    except:
        pass
        # print("Não é possível remover o arquivo solicitado")
    return JsonResponse({'status':'REVOKED'})

from .sincroniza.sincroniza import Sincroniza
def sincroniza_dados(request):
    print('chegou')
    sinc = Sincroniza()
    sinc.inicia()
    return HttpResponse("Pronto")

def cancela_requisicao_upload(request):
    idTask = request.GET['id']
    url = "http://localhost:5555/api/task/revoke/" + str(idTask) + "?terminate=true"
    resposta = requests.post(url)
    return JsonResponse({"ok":"ok"})

def status_requisicao_upload(request):
    idTask = request.GET['id']
    url = "http://localhost:5555/api/task/result/" + str(idTask)
    resposta = requests.get(url)
    resultadoJson = json.loads(resposta.content.decode('utf-8'))
    return JsonResponse({"status": "ok",'statusTask':resultadoJson})
