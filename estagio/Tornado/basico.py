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
import tornado.httpserver
from pymongo import MongoClient
class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def divide(self, num):
        cliente = MongoClient('localhost', 27017)
        banco = cliente.fila_download
        dados_db = banco.fila
        resultado = dados_db.find({'_id': str(num)})
        res = [r for r in resultado]
        while(res[0]['status'] == "compactando"):
            resultado = dados_db.find({'_id': str(num)})
            res = [r for r in resultado]

    def on_message(self, message):
        print(message)
        self.divide(message)
        self.write_message('SUCCESS')

    def on_close(self):
        print("WebSocket closed")
    def close(self, code=None, reason=None):
        print("close")
    def check_origin(self, origin):
        return True

app = tornado.web.Application([
    (r'/echo', EchoWebSocket),
])

if __name__ == '__main__':
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8080)
    server.start(0)  # autodetect number of cores and fork a process for each
    tornado.ioloop.IOLoop.instance().start()