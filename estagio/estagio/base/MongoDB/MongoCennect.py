from pymongo import MongoClient
class MongoConnect:
    def __init__(self):
        pass
        # print("Inicia conexão")

    def connect(self,nomeBanco):
        self.nomeBanco = nomeBanco
        cliente = MongoClient('localhost', 27017)
        banco = cliente[nomeBanco]
        return banco

