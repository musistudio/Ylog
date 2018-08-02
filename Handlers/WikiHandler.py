from Handlers import BaseHandler
import tornado.web
import base64
import hashlib


class WikiHandler(BaseHandler.BaseHandler):
	"""docstring for WikiHandler"""
	
	def get(self):
		self.render("wiki/index.html")
