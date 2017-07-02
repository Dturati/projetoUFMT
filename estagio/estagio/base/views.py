from django.http import JsonResponse
from .processa import ListaArquivos,PesquisaArquivos
from django.http import HttpResponse
import os
from .form import Pesquisa
from .processa import Download
import zipfile
from django.shortcuts import render
from django.core.paginator import Paginator
import ast
lista_arquivos = ListaArquivos
resutadopesquisaPaginado = []

def home(request):
    form = Pesquisa()
    resultadoPesquisa = []
    diretorio = []

    if(not(request.session.get('resultado'))):
        request.session['resultado'] = ''
    #Verifica se é uma paginação ou submição de formulario
    if(request.POST):
        num = 1
    else:
        num = int(request.GET.get('page', 1))
    if request.method == 'POST' and num == 1:
        form = Pesquisa(request.POST)
        if form.is_valid():
            resultadoPesquisa = pesquisa(form.data)
            request.session['resultado'] = resultadoPesquisa
        else:
            print("Invalido")
    P = Paginator(request.session['resultado'],6)
    contexto = {
        'form' : form,
        'resultadoPesquisa' : resultadoPesquisa,
        'quantidade' : len(request.session['resultado']),
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

def compacta_toda_pesquisa(request):
    request = request.session['resultado']
    arquivos = []
    print(request)
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






