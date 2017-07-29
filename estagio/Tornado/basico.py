import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.locks import Semaphore

sem = Semaphore(2)

def teste():
    for r in range(1,10000):
        pass

@gen.coroutine
def worker(worker_id):
    yield sem.acquire()
    try:
        print("Worker %d is working" % worker_id)
        yield teste()
    finally:
        print("Worker %d is done" % worker_id)
        sem.release()

@gen.coroutine
def runner():
    # Join all workers.
    yield [worker(i) for i in range(3)]



class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
        # IOLoop.current().run_sync(runner)
        for r in range(1,100000000):
            pass

    # IOLoop.current().run_sync(open())

    # @gen.coroutine
    def on_message(self, message):
        print ('message received:  %s' % message)
        # Reverse Message and send it back
        print ('sending back message: %s' % message[::-1])
        self.write_message(message[::-1])

    def on_close(self):
        print ('connection closed')

    def check_origin(self, origin):
        return True


application = tornado.web.Application([
    (r'/ws', WSHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    main_loop = tornado.ioloop.IOLoop.instance()
    main_loop.start()