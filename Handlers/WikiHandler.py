from Handlers import BaseHandler
import tornado.web
import base64
import hashlib


class WikiHandler(BaseHandler.BaseHandler):
	"""docstring for WikiHandler"""
	
	def get(self):
		info = ""
		self.wikis = self.getCate()
		for wiki in self.wikis:
			self.getWiki(wiki, wiki['nc_id'])
		self.render("wiki/index.html", info=info, wikis=self.wikis)

	def getCate(self):
		cates = self.application.selectDB('note_categories')
		return cates

	def getWiki(self, wiki, id):
		keys = ['nt_id', 'nt_tittle']
		wiki['lists'] = []
		results = self.application.executesDB('select nt_id,nt_tittle from notes where nt_cate=%s' % id)
		for result in results:
			res = dict()
			for key in keys:
				res[key] = result[keys.index(key)]
			wiki['lists'].append(res)


class WikiPostHandler(BaseHandler.BaseHandler):
	"""docstring for WikiPostHandler"""
	
	def get(self, id):
		wiki = dict()
		keys = ['nt_tittle', 'nt_content']
		result = self.application.executeDB('select nt_tittle,nt_content from notes where nt_id = %s' % id)
		print(result)
		for key in keys:
			wiki[key] = result[keys.index(key)]
		wiki['nt_content'] = base64.b64decode(wiki['nt_content'].encode("utf-8"))
		self.render('wiki.html', wiki=wiki)
		