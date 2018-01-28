import os
import logging
import tornado.httpserver
import tornado.ioloop
from  tornado import web,websocket
import json
clients = []
import requests
import asyncio

class WSHandler(tornado.websocket.WebSocketHandler):
    id = 0
    def check_origin(self, origin):
        return True

    def verificaUpload(self,attr):
        try:
            url = "http://localhost:5555/api/task/result/" + str(attr)
            resposta = requests.get(url)
            resultadoJson = json.loads(resposta.content)

            while(resultadoJson['state'] != 'SUCCESS'):
                url = "http://localhost:5555/api/task/result/" + str(attr)
                resposta = requests.get(url)
                resultadoJson = json.loads(resposta.content)
                print(resultadoJson)
        except:
            print("Erro ao verificar download")

        return True

    def open(self):
        clients.append(self)
        print('Conexão aberta')

    def on_close(self):
        try:
            url = "http://localhost:5555/api/task/revoke/" + str(self.id) + "?terminate=true"
            resposta = requests.post(url)
            print('conexão fechada')
        except:
            print("Erro ao cancelar task")

        clients.remove(self)

    def on_message(self, message):

        try:
            message = json.loads(message)
            self.id = message['id_tarefa']
            if(message['upload'] == "iniciou"):
                self.verificaUpload(message['id'])
                self.write_message('Sucesso')
                print("Iniciou upload")

            if(message['upload'] == 'avisa_todos'):
                print("avisa todos")
                for client in clients:
                    client.write_message('avisa_todos')

        except:
            print("Erro na menssagem")
        self.write_message('Sucesso')

        print(self.id)


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        for client in clients:
            client.write_message('OK')
        self.write('OK')


url_patterns = [
    (r'/ws', WSHandler),
    (r'/update', MainHandler),
]

application = tornado.web.Application(
    url_patterns,
    debug=False
)

if __name__ == "__main__":
    application.listen(8081)
    tornado.ioloop.IOLoop.instance().start()