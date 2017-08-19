import os,time
class Sincroniza():

    def inicia(self):
        arquivos = []
        cont = 1
        for root, dirs, files in os.walk("/arquivos"):
            for f in files:
                arquivos.append({'diretorio': root, 'arquivo':f,'modificado':time.ctime(os.path.getmtime(root + '/' + f)),
                                 'criado':time.ctime(os.path.getctime(root + '/' + f))})

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

