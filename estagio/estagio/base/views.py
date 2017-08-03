from django.core.serializers import json
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
from .task import add,report_progress
from .Email.email import send_email
import requests
from pymongo import MongoClient
lista_arquivos = ListaArquivos
resutadopesquisaPaginado = []
def home(request):
    form = Pesquisa(request.POST)
    try:
        if(not request.session['tipo_requisicao']):
            request.session['tipo_requisicao'] = 'todos_os_arquivos'
    except:
        request.session['tipo_requisicao'] = 'todos_os_arquivos'

    num = int(request.GET.get('page', 1))
    resultadoPesquisa = []
    if(request.session['tipo_requisicao'] == 'todos_os_arquivos'):
        # Verifica se é uma paginação ou submição de formulario
        from pymongo import MongoClient
        cliente = MongoClient('localhost', 27017)
        banco = cliente.test_database
        dados_db = banco.teste
        consulta = dados_db.find()
        try:
            P = Paginator(list(consulta),8)
            pagina = P.page(num)
        except:
            pagina = P.page(1)

        contexto = {
            'form': form,
            'resultadoPesquisa': resultadoPesquisa,
            'quantidade': 6,
            'paginado': pagina,
        }
        return render(request, "home.html", contexto)

    if (request.session['tipo_requisicao'] == 'pesquisa_individual'):
        if(request.POST):
            resultadoPesquisa = pesquisa(form.data)
            request.session['resultado'] = resultadoPesquisa
        try:
            P = Paginator(request.session['resultado'],8)
            pagina = P.page(num)
        except:
            pagina = P.page(1)
        contexto = {
                        'form': form,
                        'resultadoPesquisa': resultadoPesquisa,
                        'quantidade': 6,
                        'paginado': pagina,
                    }
        return render(request, "home.html", contexto)

def contatos(request):
    return render(request,"contatos.html",{"teste":"teste"})

def pesquisa(dados):
    pesquisa_arquivos = PesquisaArquivos
    meuDir = '/arquivos'
    resultadoPesquisa  = pesquisa_arquivos.lista_aquivos(dados)
    return resultadoPesquisa
from django.http import HttpResponse
#lista arquivos em forma de arvores
def lista_em_arvore(request):
    arquivosJson = JsonResponse(lista_arvore(request))
    return arquivosJson

#Faz download de um arquivo
def download(request,path):
    downloadModel = Download()
    return downloadModel.getDownload(request,path)

#compacta pesquisa selecionada
def view_compacta_pesquisa_selecionada(request):
    dados = request.GET.getlist('data[]')
    teste = json.dumps(dados)
    chave = hashlib.md5(str(choice([1, 1, 2, 3, 4, 5, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'i', 'j', 'k', 'l', 'm', 'n'])).encode('utf-8')).hexdigest()
    chaveJ = {'chave': chave}
    res = compacta_pesquisa_selecionada(teste,chaveJ)
    return JsonResponse({'status':'ok','id':'','chave':chave})

#compacta toda pesquisas
def view_compacta_toda_pesquisa(request):
    dados = {}
    # request.session['email'] = request.GET['email']
    chave = hashlib.md5(str(choice([1,1,2,3,4,5,7,8,9,'a','b','c','d','e','f','i','j','k','l','m','n'])).encode('utf-8')).hexdigest()
    if(request.session['tipo_requisicao'] == 'todos_os_arquivos'):
        chaveJ = {'chave': chave}
        cliente = MongoClient('localhost', 27017)
        banco = cliente.fila_download
        dados_db_fila = banco.fila
        value = {
            "_id": chave,
            "status": "compactando"
        }
        dados = dados_db_fila.insert_one(value).inserted_id
        res = compacta_toda_pesquisa_completa.delay(1,chaveJ)
        # fila_de_dowload.delay(chaveJ)



    if (request.session['tipo_requisicao'] == 'pesquisa_individual'):
        dadosRequest = json.dumps(request.session['resultado'])
        chaveJ = {'chave':chave}

        cliente = MongoClient('localhost', 27017)
        banco = cliente.fila_download
        dados_db_fila = banco.fila
        value = {
            "_id": str(chave),
            "status": "compactando"
        }

        dados = dados_db_fila.insert_one(value).inserted_id
        res = compacta_toda_pesquisa_individual.delay(dadosRequest,chaveJ)
        # fila_de_dowload.delay(chaveJ)
    return JsonResponse({'status': 'ok','id':res.id,'chave':chave})

#Baixa os arquivos compactados
def baixar_pesquisa(request):
    dados = request.GET
    nome_arquivo = os.getcwd() + "/" + str(dados['chave'])+".zip"
    nome_download = str(dados['chave'])+".zip"
    response = HttpResponse(open(nome_arquivo,'rb').read(), content_type='x-zip-compressed')
    response['Content-Disposition'] = "attachment; filename=%s" % nome_download
    os.remove(nome_arquivo)
    try:
        send_email(request.session['email'])
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
    return render(request,"requisicao_enviada.html",{})

def exemplo(request):
    # pass
    # arquivos = []
    # for root, dirs, files in os.walk("../arquivos"):
    #     for f in files:
    #         arquivos.append({'diretorio': root, 'arquivo':f,'modificado':time.ctime(os.path.getmtime(root + '/' + f)),
    #                          'criado':time.ctime(os.path.getctime(root + '/' + f))})
    #
    from pymongo import MongoClient
    # cliente = MongoClient('localhost',27017)
    # banco = cliente.test_database
    # dados_db = banco.teste
    # cont = 1
    # dados_db.drop()
    # for value in arquivos:
    #     value['_id'] = cont
    #     dados = dados_db.insert_one(value).inserted_id
    #     cont = cont + 1
    # context ={
    #     'contacts':'teste'
    # }
    #
    # return render(request,'exemplo.html',context)
    # cliente = MongoClient('localhost', 27017)
    # banco = cliente.fila_download
    # dados_db = banco.fila
    # resultado = dados_db.find({'_id':"6f8f57715090da2632453988d9a1501b"})
    # res = [r for r in resultado]
    # print(res[0]['status'])
    # dados_db.update({'_id': "6f8f57715090da2632453988d9a1501b"}, {"status": "download"}, upsert=False)
    # resultado = dados_db.find({'_id': "6f8f57715090da2632453988d9a1501b"})
    # res = [r for r in resultado]
    # print(res[0]['status'])
    from random import choice
    chave = hashlib.md5(str(choice([1,1,2,3,4,5,7,8,9,'a','b','c','d','e','f','i','j','k','l','m','n'])).encode('utf-8')).hexdigest()
    print(range())
    return HttpResponse("")
def exemplo_assinc(request):
   return render(request,"websocket.html")

def get_resultado(request):
    dados = request.GET
    res = add.AsyncResult(dados['id'])
    return JsonResponse({'status':res.status})

def status_stak_celery(request):
    dados = request.GET
    url = "http://localhost:5555/api/tasks"
    resposta = requests.get(url)
    resultadoJson = json.loads(resposta.content)
    return JsonResponse({'id':dados['id'],'tasks':resultadoJson[dados['id']],'total_tasks':resultadoJson})

def fila_celery(request):
    url = "http://localhost:5555/api/tasks"
    resposta = requests.get(url)
    resultadoJson = json.loads(resposta.content)
    return JsonResponse({'total_tasks':resultadoJson})

def cancelar_requisicao(request):
    dadosRequest = request.GET
    url = "http://localhost:5555/api/task/revoke/"+str(dadosRequest['id'])+"?terminate=true"
    resposta = requests.post(url)
    try:
        os.remove(dadosRequest['chave']+".zip")
    except:
        pass
    return JsonResponse({'status':'REVOKED'})


