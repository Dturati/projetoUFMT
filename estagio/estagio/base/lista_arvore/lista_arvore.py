from django.http import JsonResponse
from ...base.processa import ListaArquivos
import os
from django.conf import settings

lista_arquivos = ListaArquivos

def lista_arvore(request):
    caminho = request.GET.get('caminho', None)
    if(caminho == '/'):
        caminho = settings.MEDIA_URL
    meuDir = caminho
    diretorio, arquivos,detalheArquivosModificado,\
    detalheArquivosCriados,detalhePastaModificadas,\
    detalhePastaCriadas = lista_arquivos.list_files(meuDir)

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
    return data
