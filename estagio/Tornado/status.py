import os
import logging
import tornado.httpserver
import tornado.ioloop
from  tornado import web,websocket
import json
clients = []
class WSHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def verificaDownload(self,attr):
        pass
    def open(self):
        clients.append(self)
        print('connection opened')

    def on_close(self):
        clients.remove(self)
        print('connection closed')

    def on_message(self, message):
        try:
            message = json.loads(message)
            if(message['upload'] == "iniciou"):
                self.write_message("Echo: " + 'Terminou')
        except:
            pass
        # self.write_message("Echo: " + message)
        self.write_message("Echo: " + 'Sucesso')
        # print('received:', message)


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