from Handlers import BaseHandler

class IndexHandler(BaseHandler.BaseHandler):
    def get(self):
        self.render("yclass/index.html")