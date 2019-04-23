import os,time
from django.conf import settings


class Sincroniza():

    def inicia(self):
        nome = 'NET_GLOBALI_GLOBALR_PARI_PAR;all_line;T_UR;Tsolo_URsolo;net;globali;globalr;pari;parr;tsoil;ppt;t;rh;u;rhsoil'
        colunas = nome.split(';')
        arquivos = []
        cont = 1
        for root, dirs, files in os.walk(settings.MEDIA_URL):
            for f in files:
                limpo = f.replace('-',' ').replace('_',' ').replace('  ',' ').replace('  ',' ').replace('.csv','')
                dados = limpo.split(' ')
                tipo = 'random'
                if(dados[2] == 'seq'):
                    tipo = 'sequential'
                
                var = {'diretorio': root, 'arquivo':f,'modificado':time.ctime(os.path.getmtime(root + '/' + f)),'criado':time.ctime(os.path.getctime(root + '/' + f)),
                        'type':dados[2], 
                        'type_name':tipo,
                        'percent':int(dados[1]),
                        'column_name':colunas[int(dados[4])],
                        'column':int(dados[4])}
                arquivos.append(var)


        print('meio')
        from pymongo import MongoClient
        cliente = MongoClient('localhost',27017)
        banco = cliente.test_database
        dados_db = banco.teste
        cont = 1
        dados_db.drop()
        for value in arquivos:
            value['_id'] = cont
            dados = dados_db.insert_one(value).inserted_id
            cont = cont + 1
        print('fim')

