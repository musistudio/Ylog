from Handlers import BaseHandler
import base64

#渲染后台管理页面
class AdminHandler(BaseHandler.BaseHandler):
    def get(self):
        self.render("admin/admin.html")


#渲染文章管理页面
class ArticalHandler(BaseHandler.BaseHandler):
    def get(self):
        self.table = 'artical'
        articals = self.getData()
        self.render("admin/artical.html", articals=articals)

    def getKeys(self):
        keys = []
        self.execute_sql = "desc %s;" % self.table
        results = self.executesDB()
        for result in results:
            keys.append(result[0])
        return keys

    def getData(self):
        res = []
        keys = self.getKeys()
        self.execute_sql = "SELECT * from %s limit 0,10;" % self.table
        datas = self.executesDB()
        self.table = 'tags'
        tags = self.selectDB()
        for data in datas:
            result = dict()
            for key in keys:
                if key == 'tags':
                    for tag in tags:
                        if tag['id'] == data[keys.index(key)]:
                            result[key] = tag['name']
                else:
                    result[key] = data[keys.index(key)]
            res.append(result)
        return res


class ArticalDelHandler(BaseHandler.BaseHandler):
    def get(self, id):
        self.table = 'artical'
        self.drop_sql = "id = %s" % id
        self.dropDB()
        self.render("status.html", info="删除成功", url="/admin/artical.html")


#渲染文章编写页面
class WriterHandler(BaseHandler.BaseHandler):
    def get(self):
        self.table = "tags"
        tags = self.selectDB()
        self.render("admin/writer.html", tags=tags)


#将文章写入数据库
class WriterPostHandler(BaseHandler.BaseHandler):
    def post(self, *args, **kwargs):
        tittle = self.get_argument("tittle")
        content = self.get_argument("content")
        date = self.get_argument("date")
        tags = self.get_argument("tags")
        self.table = 'artical'
        self.insert_sql = {
            "id": "null",
            "tittle": tittle,
            "content": base64.b64encode(content.encode(encoding="utf-8")).decode(), #将文章内容进行base64编码
            "thumbnail": "null",
            "public_time": date,
            "tags": int(tags)
        }
        self.insertDB()
        self.render("status.html", info="发布成功", url="/admin/artical.html")
        # self.write("<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body>发布成功!</body></html>")


#渲染标签管理页面
class TagsHandler(BaseHandler.BaseHandler):
    def get(self):
        tags = self.getCount()
        self.render("admin/tags.html", tags=tags)

    def getTags(self):
        self.table = "tags"
        return self.selectDB()

    def getCount(self):
        tags = self.getTags()
        for tag in tags:
            self.execute_sql = "select count(*) from artical where tags = %d" %tag["id"]
            tag["count"] = self.executeDB()[0]
        return tags


#添加标签实现
class TagsAddHandler(BaseHandler.BaseHandler):
    def post(self, *args, **kwargs):
        tags_name = self.get_argument("tagsname")
        self.table = 'tags'
        self.insert_sql = {
            "id": "null",
            "name": tags_name
        }
        self.insertDB()
        self.write("添加成功!")


#删除标签实现
class TagsDelHandler(BaseHandler.BaseHandler):
    def get(self, id):
        self.table = 'tags'
        self.drop_sql = "id = %s" % id
        self.dropDB()
        self.render("status.html", info="删除成功", url="/admin/tags.html")


#渲染登录页面
class LoginHandler(BaseHandler.BaseHandler):
    def get(self):
        self.render("admin/login.html")


#登录页面逻辑处理
class LoginPostHandler(BaseHandler.BaseHandler):
    pass