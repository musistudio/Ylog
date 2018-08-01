import tornado.httpserver
import tornado.ioloop
import tornado.options
from Application import Application
from router import routers
from config import settings
from tornado.options import define, options


define("port", default=8000, help="the server's port", type=int)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application(
        handlers=routers,
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
