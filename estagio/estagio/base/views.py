from django.http import JsonResponse
from .processa import ListaArquivos,PesquisaArquivos
from django.http import HttpResponse
import os
from .form import Pesquisa
from .processa import Download
import zipfile
from django.shortcuts import render
from django.core.paginator import Paginator
from pymongo import MongoClient
from estagio.base.lista_arvore.lista_arvore import lista_arvore
from estagio.base.compacta_pesquisa.compacta_pesquisa import compacta_toda_pesquisa,compacta_pesquisa_selecionada
lista_arquivos = ListaArquivos
resutadopesquisaPaginado = []

def home(request):
    form = Pesquisa(request.POST)
    num = int(request.GET.get('page', 1))
    act = str(request.GET.get('act'))
    anterior = 1
    proximo = 2
    if(request.POST):
        try:
            form.data['todosOsArquivos']
            request.session['tipo_requisicao'] = 'todos_os_arquivos'
        except:
            request.session['tipo_requisicao'] = 'pesquisa_individual'

    if(request.session.get('tipo_requisicao') == 'todos_os_arquivos'):
        request.session['resultado'] = ''
        #Paginacao
        if (num > 2 and act == 'S'):
            num = num - 1
            anterior = num
            proximo = num + 1

        resultadoPesquisa = []
        #Verifica se é uma paginação ou submição de formulario
        cliente = MongoClient('localhost', 27017)
        banco = cliente.test_database
        dados_db = banco.teste
        consulta = dados_db.find().skip(10*(num-1)).limit(10)
        P = Paginator(list(consulta),10)

        if (act == 'A' and P.count > 1 and num > 1):
            proximo = num + 1
            anterior = num - 1
            num = num + 1

        if(P.count == 0):
            proximo = num - 1
            anterior = num - 2
            num = num - 1
            consulta = dados_db.find().skip(10 * (num - 1)).limit(10)
            P = Paginator(list(consulta), 10)

        contexto = {
            'form' : form,
            'resultadoPesquisa' : resultadoPesquisa,
            'quantidade' : 6,
            'paginado':P.page(1),
            'anterior':anterior,
            'proximo':proximo
        }
        return render(request,"home.html",contexto)

    if (request.session.get('tipo_requisicao') == 'pesquisa_individual'):
        # Paginacao
        if(request.POST):
            resultadoPesquisa = pesquisa(form.data)
            request.session['resultado'] = resultadoPesquisa
        # print(request.session['resultado'])
        if (num > 2 and act == 'S'):
            num = num - 1
            anterior = num
            proximo = num + 1

        resultadoPesquisa = []
        P = Paginator(request.session['resultado'], 10)

        if (act == 'A' and P.count > 1 and num > 1):
            proximo = num + 1
            anterior = num - 1
            num = num + 1

        if (P.count == 0):
            proximo = num - 1
            anterior = num - 2
            num = num - 1
            P = Paginator(request.session['resultado'], 10)

        #Ultima página
        try:
            P.page(num)
        except:
            if(P.count == 0):
                num = 2
            contexto = {
                'form': form,
                'resultadoPesquisa': resultadoPesquisa,
                'quantidade': 6,
                'paginado': P.page(num-1),
                'anterior': anterior,
                'proximo': proximo - 1
            }
            return render(request, "home.html", contexto)

        contexto = {
            'form': form,
            'resultadoPesquisa': resultadoPesquisa,
            'quantidade': 6,
            'paginado': P.page(1),
            'anterior': anterior,
            'proximo': proximo
        }
        return render(request, "home.html", contexto)

def contatos(request):
    return render(request,"contatos.html",{"teste":"teste"})

def pesquisa(dados):
    pesquisa_arquivos = PesquisaArquivos
    meuDir = '/arquivos'
    resultadoPesquisa  = pesquisa_arquivos.lista_aquivos(dados)
    return resultadoPesquisa

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
    compacta_pesquisa_selecionada(request)
    return JsonResponse({'status':'ok'})

#compacta toda pesquisas
#aqui devo fazer uma fila de requisições
def view_compacta_toda_pesquisa(request):
    compacta_toda_pesquisa(request)
    return JsonResponse({'status': 'ok'})

#Baixa os arquivos compactados
def baixar_pesquisa(request):
    nome_arquivo = os.getcwd() + "/" + "pesquisa.zip"
    nome_download = "pesquisa.zip"
    response = HttpResponse(open(nome_arquivo, 'rb').read(), content_type='x-zip-compressed')
    response['Content-Disposition'] = "attachment; filename=%s" % nome_download
    return response

def exemplo(request):
    from pymongo import MongoClient
    cliente = MongoClient('localhost',27017)
    banco = cliente.test_database
    dados_db = banco.teste
    dados= []
    dados = {'todosOsArquivos':"ativado"}
    todos_os_arquivos = pesquisa(dados)
    cont = 1
    for value in todos_os_arquivos:
        value['_id'] = cont
        dados = dados_db.insert_one(value).inserted_id
        cont = cont + 1
    #
    consulta  = dados_db.find()
    # consulta  = dados_db.drop()
    # cont = 1
    # for r in consulta:
    #     print(r)
    #     if cont == 10:
    #         break;
    #     cont = cont + 1
    context ={
        'contacts':'teste'
    }
    return render(request,'exemplo.html',context)

def exemplo_assinc(request):
    return render(request,"websocket.html",{})






