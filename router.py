#路由配置

from Handlers import IndexHandler
from Handlers import AdminHandler
from Handlers import YclassHandler
from Handlers import PostsHandler

routers = [
    (r"/", IndexHandler.IndexHandler),
    (r"/(\d+).html", IndexHandler.ListHandler),
    (r"/posts/(\d+).html", PostsHandler.PostsHandler),
    (r"/admin/", AdminHandler.AdminHandler),
    (r"/admin/artical.html", AdminHandler.ArticalHandler),
    (r"/admin/articaldel/(\d+)", AdminHandler.ArticalDelHandler),
    (r"/admin/writer.html", AdminHandler.WriterHandler),
    (r"/admin/WriterPost", AdminHandler.WriterPostHandler),
    (r"/admin/tags.html", AdminHandler.TagsHandler),
    (r"/admin/tagsadd", AdminHandler.TagsAddHandler),
    (r"/admin/tagsdel/(\d+)", AdminHandler.TagsDelHandler),
    (r"/admin/login.html", AdminHandler.LoginHandler),
    (r"/admin/login", AdminHandler.LoginPostHandler),
    (r"/admin/logout", AdminHandler.LogoutHandler),
    (r"/yclass/", YclassHandler.IndexHandler),
    (r"/yclass/login", YclassHandler.YclassLogin),
    (r"/yclass/logout", YclassHandler.YclassLogout),
    (r"/yclass/classlist", YclassHandler.YclassList),
    (r"/yclass/classpass", YclassHandler.YclassPass)
]