import os
import csv
def GeraArquivoParaGraficoEmR(nomeArquivo):
    os.chdir("/")
    with open('/arquivos/arquivos/uploads/'+str(nomeArquivo)+'.csv', 'w') as datafile:
        datafile.write(str('Tipo' + ','
                           + 'Porcentagem' + ','
                           + 'Metodo' + ','
                           + 'Variavel' + ','
                           + 'R2' + ','
                           + 'd' + ','
                           + 'MAE' + ','
                           + 'RMSE' + ','
                           + 'Juncao' + ','
                           + 'Tempo' + '\n'
                           )
                       )
        for root, dirs, files in os.walk(os.getcwd()+"/arquivos/arquivos/uploads/resultados/"):
            for arqcsv in files:

                    with open(str(os.getcwd() + "/arquivos/arquivos/uploads/resultados/" + str(arqcsv))) as arq:
                        reader = csv.DictReader(arq)
                        for row in reader:
                            datafile.write(str(
                                row['Tipo'] + ','
                                + row['Porcentagem'] + ','
                                + row['Metodo'] + ','
                                + row['Variavel'] + ','
                                + row['R2'] + ','
                                + row['d'] + ','
                                + row['MAE'] + ','
                                + row['RMSE'] + ','
                                + row['Juncao'] + ','
                                + row['Tempo'] + '\n'
                            ))
    datafile.close()

    return "Gera Gráfico"