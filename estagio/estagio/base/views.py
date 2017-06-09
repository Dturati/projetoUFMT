from builtins import type
from django.http import JsonResponse
from django.shortcuts import render
from .models import ListaArquivos,PesquisaArquivos
from django.conf import settings
from django.http import HttpResponse
import os,time
from .form import Pesquisa
import re
from .models import Download,Compacta_aquivos
from wsgiref.util import FileWrapper
import mimetypes
import zipfile
from io import StringIO,BytesIO
# Create your views here.
lista_arquivos = ListaArquivos

def home(request):
    form = Pesquisa()
    resultadoPesquisa = []
    detalheArquivosCriados = []
    detalheArquivosModificado = []
    diretorio = []
    if request.method == 'POST':
        form = Pesquisa(request.POST)
        if form.is_valid():
            resultadoPesquisa,diretorio,detalheArquivosCriados,detalheArquivosModificado = pesquisa(form.data)
        else:
            print("Invalido")
    contexto = {
        'form' : form,
        'resultadoPesquisa' : resultadoPesquisa,
        'diretorio' : diretorio,
        'iterar' : range(len(resultadoPesquisa)),
        'teste' : zip(resultadoPesquisa,diretorio,detalheArquivosModificado,detalheArquivosModificado)

    }
    return render(request,"home.html",contexto)

def contatos(request):
    return render(request,"contatos.html",{"teste":"teste"})

def pesquisa(dados):
    pesquisa_arquivos = PesquisaArquivos
    resultado = dados['numeroSequencial']
    resultado += '-' + dados['porcentagem']
    resultado += '-' + dados['tipoFalha']
    resultado += '-' + '_'+'13'+'_'
    resultado +=  dados['tipoFalhaConjunto']
    resultado += '-' + dados['variavelFalhada']
    resultado += '-' + dados['metodoUtilizado']
    resultado += '.csv'

    meuDir = '/arquivos'
    resultadoPesquisa,diretorio,detalheArquivosCriados,detalheArquivosModificado = pesquisa_arquivos.lista_aquivos(resultado)
    return resultadoPesquisa,diretorio,detalheArquivosCriados,detalheArquivosModificado

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
    print(arquivos)
    # zip_subdir = 'estagio'
    zf = zipfile.ZipFile('pesquisa.zip', "w")
    for fpath in request:
        fdir, fname = os.path.split(fpath)
        zip_subdir = str(fdir)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)
    zf.close()
    return JsonResponse({'status':'ok'})

def baixar_pesquisa(request):
    nome_arquivo = os.getcwd() + "/" + "pesquisa.zip"
    nome_download = "pesquisa.zip"
    response = HttpResponse(open(nome_arquivo, 'rb').read(), content_type='x-zip-compressed')
    response['Content-Disposition'] = "attachment; filename=%s" % nome_download
    return response






