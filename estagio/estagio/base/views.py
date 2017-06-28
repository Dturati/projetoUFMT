from django.http import JsonResponse
from .models import ListaArquivos,PesquisaArquivos
from django.http import HttpResponse
import os
from .form import Pesquisa
from .models import Download,Compacta_aquivos
import zipfile
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import ast
lista_arquivos = ListaArquivos
resutadopesquisaPaginado = []

def home(request):
    form = Pesquisa()
    resultadoPesquisa = []
    diretorio = []

    #Verifica se é uma paginação ou submição de formulario
    if(request.POST):
        num=1
    else:
        num = int(request.GET.get('page', 1))

    if request.method == 'POST' and num == 1:
        arquivosPesquisa = open('arquivosPesquisa.txt','w')
        form = Pesquisa(request.POST)
        if form.is_valid():
            resultadoPesquisa = pesquisa(form.data)
        else:
            print("Invalido")
        for r in resultadoPesquisa:
            arquivosPesquisa.write(str(r)+"\n")
        arquivosPesquisa.close()
        resutadopesquisaPaginado = resultadoPesquisa
    else:
        resutadopesquisaPaginado = []
        arquivosPesquisa = open('arquivosPesquisa.txt','r')
        resultado =arquivosPesquisa.readlines()
        for r in resultado:
            resutadopesquisaPaginado.append(ast.literal_eval(r))
        arquivosPesquisa.close()
    P = Paginator(resutadopesquisaPaginado,2)
    contexto = {
        'form' : form,
        'resultadoPesquisa' : resultadoPesquisa,
        'diretorio' : diretorio,
        'paginado':P.page(num)
    }

    return render(request,"home.html",contexto)

def contatos(request):
    return render(request,"contatos.html",{"teste":"teste"})

def pesquisa(dados):
    pesquisa_arquivos = PesquisaArquivos
    meuDir = '/arquivos'
    resultadoPesquisa  = pesquisa_arquivos.lista_aquivos(dados)
    return resultadoPesquisa

def lista_diretorios(request):
    caminho = request.GET.get('caminho', None)
    if(caminho == '/'):
        caminho = '/arquivos'
    meuDir = caminho
    diretorio, arquivos,detalheArquivosModificado,detalheArquivosCriados,detalhePastaModificadas,detalhePastaCriadas = lista_arquivos.list_files(os.getcwd() + meuDir)

    #Remove / duplicado em caminhos de diretorios
    teste = list(caminho[::-1].split()[0])
    anterior = list(caminho[::-1].split()[0])
    char = teste[0]
    if(teste[0] == '/'):
        teste.pop(0)
        char = teste[0]
    cont = 0
    while(char != '/'):
        teste.pop(0)
        char = teste[0]
        if(teste[0] == '/'):
            teste.pop(0)

    teste = teste[::-1]
    teste = ''.join(teste)

    data = {
        'anterior': teste,
        'arquivos' : arquivos,
        'diretorios' : diretorio,
        'caminho' : meuDir,
        'detalheArquivosModificado' : detalheArquivosModificado,
        'detalheArquivosCriados' : detalheArquivosCriados,
        'detalhePastaModificadas' : detalhePastaModificadas,
        'detalhePastaCriadas' : detalhePastaCriadas
    }
    arquivosJson = JsonResponse(data)
    return arquivosJson

#Faz download de um arquivo
def download(request,path):
    downloadModel = Download()
    return downloadModel.getDownload(request,path)

def compacta_pesquisa(request):
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

    return JsonResponse({'status':'ok'})

#Baixa os arquivos compactados
def baixar_pesquisa(request):
    nome_arquivo = os.getcwd() + "/" + "pesquisa.zip"
    nome_download = "pesquisa.zip"
    response = HttpResponse(open(nome_arquivo, 'rb').read(), content_type='x-zip-compressed')
    response['Content-Disposition'] = "attachment; filename=%s" % nome_download
    return response

def exemplo(request):
    valores = ['david','maria','jose','pedro','dois','tres','quatro']

    P = Paginator(valores,2)
    num = (request.GET.get('page'))
    context ={
        'contacts':P.page(num)
    }
    return render(request,'exemplo.html',context)






