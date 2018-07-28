from Handlers import BaseHandler

class PostsHandler(BaseHandler.BaseHandler):
    def get(self, id):
        self.write(id)