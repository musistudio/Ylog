#项目配置文件

import uuid
import base64
import os

#数据库配置
DATABASE = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "dbname": "ylog"
}

#tornado项目配置
cookie_secret = base64.b64encode(uuid.uuid4().bytes)
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"template_path": os.path.join(os.path.dirname(__file__), "Template"),
	"cookie_secret": cookie_secret,
	"debug": True,
	"login_url": '/admin/login.html',
	"autoescape": None
}