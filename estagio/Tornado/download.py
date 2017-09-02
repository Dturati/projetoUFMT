    #def divide(self, num):
# url = "http://localhost:5555/api/tasks"
# resposta = requests.get(url)
# resultadoJson = json.loads(resposta.content)
# while(resultadoJson[num]['state'] != "SUCCESS" and resultadoJson[num]['state'] != "REVOKED"):
#     url = "http://localhost:5555/api/tasks"
#     resposta = requests.get(url)
#     resultadoJson = json.loads(resposta.content)
# return resultadoJson[num]['state']

import tornado.ioloop
import tornado.web
from tornado import websocket,ioloop
import asyncio
from tornado import gen
import json
import requests
import os
import tornado.httpserver
from pymongo import MongoClient
import requests
import tornado.options

class EchoWebSocket(websocket.WebSocketHandler):
    chave    = ""
    id       = ""
    def open(self):
        print("WebSocket opened")

    @gen.coroutine
    def divide(self, num):
        self.chave = num
        cliente = MongoClient('localhost', 27017)
        banco = cliente.fila_download
        dados_db = banco.fila
        resultado = dados_db.find({'_id': str(num)})
        res = [r for r in resultado]
        while(res[0]['status'] == "compactando"):
            resultado = dados_db.find({'_id': str(num)})
            res = [r for r in resultado]
        if(res[0]['status'] == 'cancelado'):
            return 'CANCELADO'
        else:
            return 'SUCCESS'

    @gen.coroutine
    def on_message(self, message):
        try:
            message = json.loads(message)
            self.chave = message["chave"]
            self.id    = message["id"]
            res = yield self.divide(message["chave"])
            self.write_message(res)
        except:
            print("erro ao receber ")

    def on_close(self):
        print(self.id)
        print("WebSocket closed")

    def close(self, code=None, reason=None):
        print("close")


    def check_origin(self, origin):
        return True

app = tornado.web.Application([
    (r'/echo', EchoWebSocket)
])

if __name__ == '__main__':
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8080)
    server.start(0)  # autodetect number of cores and fork a process for each
    tornado.ioloop.IOLoop.instance().start()


