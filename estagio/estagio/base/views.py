from django.core.serializers import json
from django.http import JsonResponse
from .processa import ListaArquivos,PesquisaArquivos
from django.http import HttpResponse
import os,time
from .form import Pesquisa
from .processa import Download
from django.shortcuts import render
from django.core.paginator import Paginator
from estagio.base.lista_arvore.lista_arvore import lista_arvore
from estagio.base.compacta_pesquisa.compacta_pesquisa import compacta_toda_pesquisa,compacta_pesquisa_selecionada
import json
lista_arquivos = ListaArquivos
resutadopesquisaPaginado = []

def home(request):
    form = Pesquisa(request.POST)
    request.session['tipo_requisicao'] = 'todos_os_arquivos'
    if(request.POST):
        try:
            form.data['todosOsArquivos']
            request.session['tipo_requisicao'] = 'todos_os_arquivos'
        except:
            request.session['tipo_requisicao'] = 'pesquisa_individual'

    num = int(request.GET.get('page', 1))
    resultadoPesquisa = []
    if( request.session['tipo_requisicao'] == 'todos_os_arquivos' or not request.session['tipo_requisicao']):
        # Verifica se é uma paginação ou submição de formulario
        from pymongo import MongoClient
        cliente = MongoClient('localhost', 27017)
        banco = cliente.test_database
        dados_db = banco.teste
        consulta = dados_db.find()
        P = Paginator(list(consulta), 10)
        contexto = {
            'form': form,
            'resultadoPesquisa': resultadoPesquisa,
            'quantidade': 6,
            'paginado': P.page(num),
        }
        return render(request, "home.html", contexto)

    if (request.session['tipo_requisicao'] == 'pesquisa_individual'):
        if(request.POST):
            resultadoPesquisa = pesquisa(form.data)
            request.session['resultado'] = resultadoPesquisa
        P = Paginator(request.session['resultado'], 10)
        contexto = {
                        'form': form,
                        'resultadoPesquisa': resultadoPesquisa,
                        'quantidade': 6,
                        'paginado': P.page(num),
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
    dados = request.GET.getlist('data[]')
    teste = json.dumps(dados)
    compacta_pesquisa_selecionada.delay(teste)
    return JsonResponse({'status':'ok'})

#compacta toda pesquisas
#aqui devo fazer uma fila de requisições
def view_compacta_toda_pesquisa(request):
    try:
        dados = json.dumps(request.session['resultado'])
    except:
        dados = {}
    # dados = json.dumps(request)
    compacta_toda_pesquisa.delay(dados)
    # compacta_toda_pesquisa(dados)
    return JsonResponse({'status': 'ok'})

#Baixa os arquivos compactados
def baixar_pesquisa(request):
    nome_arquivo = os.getcwd() + "/" + "pesquisa.zip"
    nome_download = "pesquisa.zip"
    response = HttpResponse(open(nome_arquivo, 'rb').read(), content_type='x-zip-compressed')
    response['Content-Disposition'] = "attachment; filename=%s" % nome_download
    return response

def exemplo(request):
    arquivos = []
    for root, dirs, files in os.walk("./arquivos"):
        for f in files:
            # detalheArquivosModificado.append(time.ctime(os.path.getmtime(root + '/' + r)))
            # detalheArquivosCriados.append(time.ctime(os.path.getctime(root + '/' + r)))
            arquivos.append({'diretorio': root, 'arquivo':f,'modificado':time.ctime(os.path.getmtime(root + '/' + f)),
                             'criado':time.ctime(os.path.getctime(root + '/' + f))})
    # print(arquivos)
    from pymongo import MongoClient
    cliente = MongoClient('localhost',27017)
    banco = cliente.test_database
    dados_db = banco.teste
    # dados= []
    # dados = {'todosOsArquivos':"ativado"}
    # todos_os_arquivos = pesquisa(dados)
    # print(todos_os_arquivos)
    cont = 1
    dados_db.drop()
    for value in arquivos:
        # print(value)
        value['_id'] = cont
        dados = dados_db.insert_one(value).inserted_id
        cont = cont + 1
    #
    # consulta  = dados_db.find()
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

from estagio.base.task import add
def exemplo_assinc(request):
    dados = request.GET
    dados = dados['valor']
    resultado = add.delay(dados)
    redis ={
        'id':resultado.id,
        'status':resultado.status
    }
    return render(request,"websocket.html",redis)

def get_resultado(request):
    dados = request.GET
    res = add.AsyncResult(dados['status'])
    print(res.id)
    print(res.status)
    print(res.get())
    resultado = str("id: " + res.id + " status: " + res.status)
    return HttpResponse(resultado)




