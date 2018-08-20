#项目配置文件

import uuid
import base64
import os
import tornado.web

#数据库配置
DATABASE = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Lijinhui779956774",
    "dbname": "ylog" 
}

class NotFoundHandler(tornado.web.RequestHandler):
	"""docstring for NotFound
		捕获404异常并渲染404页面
	"""
	def get(self):
		self.render('404.html')
		
#tornado项目配置
cookie_secret = base64.b64encode(uuid.uuid4().bytes)
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"template_path": os.path.join(os.path.dirname(__file__), "Template"),
	"cookie_secret": cookie_secret,
	"login_url": '/admin/login.html',
	"autoescape": None,
	"default_handler_class": NotFoundHandler,
	"debug": True
}
