from rpy2.robjects.packages import STAP,STF
import rpy2.robjects.packages as rp
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
import os
import subprocess
from celery import shared_task
import zipfile

from rpy2.robjects.packages import importr
hydro = importr("hydroGOF")
from ..Gerar_grafico.Gerar_grafico import GeraArquivoParaGraficoEmR
import shutil
@shared_task
def executaScript(rash):
    os.chdir("/")
    with open(os.getcwd()+"arquivos/uploads/analise.R", "r") as r:
        string = r.read()
    fun = STAP(string, "processa")
    arquivos = []


    for root, dirs, files in os.walk("/arquivos/uploads/resultados/"):
        for value in files:
            arquivo = str(root)+str(value)
            arquivos.append(arquivo)
    os.chdir("/arquivos/uploads/")
    zf = zipfile.ZipFile(rash + ".zip", "w")

    for value in arquivos:
        try:
            fdir, fname = os.path.split(value)
            zip_subdir = str(fdir)
            zip_path = os.path.join(zip_subdir, value)
            zf.write(value, zip_path)
        except ValueError as e:
            print(e)
    zf.close()
    GeraArquivoParaGraficoEmR(rash)
    shutil.rmtree("/arquivos/uploads/"+str(rash))

    os.chdir("/")

    with open(os.getcwd() + "arquivos/uploads/grafico.R", "r") as r:
        string = r.read()
    try:
        fun = STAP(string, "processa")
    except:
        print("Erro ao executar algumas funcoes")

