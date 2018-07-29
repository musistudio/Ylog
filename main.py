import tornado.httpserver
import tornado.ioloop
import tornado.options
import router
import os

from tornado.options import define, options
define("port", default=8000, help="the server's port", type=int)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=router.routers,
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "Template"),
        debug=True,
        autoescape=None
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()