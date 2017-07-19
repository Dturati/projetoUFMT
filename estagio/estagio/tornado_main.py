from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os, sys
# Keep Python from creating .pyc files
sys.dont_write_bytecode = True
SITE_ROOT = os.path.dirname(os.getcwd())
PROJECT_NAME = os.path.basename(os.getcwd())
sys.path.append( SITE_ROOT )
os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT_NAME + '.settings'
import django
django.setup()
define('port', type=int, default=8080)

class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('now we are talking from tornado')

def main():
  parse_command_line()
  wsgi_app = tornado.wsgi.WSGIContainer(
  django.core.handlers.wsgi.WSGIHandler())
  settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=True,
            cookie_secret=")r&u2_gbw4%wiyrv!7#6u0a-_axtp!i5j=q*ph-)p))yn_dk61",
        )
  tornado_app = tornado.web.Application(
    [
      ('/', HelloHandler),
      ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
      ], **settings)
  tornado.options.parse_command_line()
  server = tornado.httpserver.HTTPServer(tornado_app)
  server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()