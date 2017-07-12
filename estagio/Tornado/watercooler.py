from urllib.parse import urlparse

import logging
import signal
import time
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler, WebSocketError, WebSocketClosedError
from tornado.options import define,parse_command_line,options
from tornado.httpserver import HTTPServer
from collections import defaultdict
define('debug',default=True,type=bool,help='Run in debug mode')
define('port',default=8080,type=int,help='Server port')
define('allowed_hosts',default="localhost:8080",multiple=True,help='Allowed hosts for cross domain connections')


class ScrumAplication(Application):
    def broadcast(self,message,channel=None,sender=None):
        if channel is None:
            for c in self.subscriptions.keys():
                self.broadcast(message,channel=c,sender=sender)
        else:
            peers = self.get_subscribers(channel)
            for peer in peers:
                for i in range(1,100000000):
                    if(i == 10000000-1):
                        print("fim")
                    # print(i)
                    pass
                if peer != sender:
                    try:
                        peer.write_message(message)
                    except WebSocketClosedError:
                        self.remove_subscriber(channel,peer)

    def __init__(self,**kwargs):
        routes =[
            (r'/(?P<sprint>[0-9]+)', SprintHandler),
        ]
        super().__init__(routes,**kwargs)
        self.subscriptions = defaultdict(list)

    def add_subscriber(self,channel,subscriber):
        self.subscriptions[channel].append(subscriber)

    def remove_subscriber(self,channel,subscriber):
        self.subscriptions[channel].remove(subscriber)

    def get_subscribers(self,channel):
        return self.subscriptions[channel]

def shutdown(server):
    ioloop = IOLoop.instance()
    logging.info('Stopping server.')
    server.stop()

    def finalise():
        ioloop.stop()
        logging.info('Stopped.')

    ioloop.add_timeout(time.time() + 1.5, finalise)

class SprintHandler(WebSocketHandler):

    def check_origin(self, origin):
        allowed = super().check_origin(origin)
        parsed = urlparse(origin.lower())
        matched = any(parsed.netloc == host for host in options.allowed_hosts)
        return options.debug or allowed or matched

    def open(self,sprint):
        self.sprint = sprint
        self.application.add_subscriber(self.sprint,self)

    def on_message(self, message):
        self.application.broadcast(message,channel=self.sprint,sender=self)

    def on_close(self):
        self.application.remove_subscriber(self.sprint,self)

if __name__ == "__main__":
    parse_command_line()
    application = ScrumAplication(debug=options.debug)
    # application.listen(8080)
    server = HTTPServer(application)
    server.listen(options.port)
    signal.signal(signal.SIGINT,lambda sig,frame:shutdown(server))
    logging.info('Starting server on localhost:{}'.format(options.port))
    IOLoop.instance().start()