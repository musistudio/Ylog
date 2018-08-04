from Handlers import BaseHandler
import tornado.web
import base64
import hashlib
import string,random



# 渲染登录页面
class LoginHandler(BaseHandler.BaseHandler):

    def get(self):
        self.render("admin/login.html")


# 登录逻辑处理
class LoginPostHandler(BaseHandler.BaseHandler):
    """docstring for LoginPostHandler"""

    def post(self):
        md5 = hashlib.md5()
        username = self.get_argument('username')
        password = md5.update(self.get_argument('password').encode('utf-8'))
        try:
            db_password = self.application.executeDB(
                "select ad_pwd from admin where ad_user='%s'" % username)[0]
            if md5.hexdigest() == db_password:
                self.set_secure_cookie('admin', db_password)
                rsp = {
                    'status': 200,
                    'msg': '登陆成功'
                }
            else:
                rsp = {
                    'status': 401,
                    'msg': '用户名或密码错误'
                }
        except TypeError:
            rsp = {
                'status': 403,
                'msg': '用户名不存在'
            }
        self.write(rsp)


# 退出登陆
class LogoutHandler(BaseHandler.BaseHandler):
    """docstring for Logout"""

    def get(self):
        print(self.get_secure_cookie('admin'))
        self.set_secure_cookie('admin', '')
        self.write('已退出登陆')


# 渲染后台管理页面
class AdminHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("admin/admin.html")


# 渲染文章管理页面
class ArticalHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        articals = self.getData()
        self.render("admin/artical.html", articals=articals)

    def getKeys(self):
        keys = []
        results = self.application.executesDB("desc artical;")
        for result in results:
            keys.append(result[0])
        return keys

    def getData(self):
        res = []
        keys = self.getKeys()
        execute_sql = "SELECT * from artical limit 0,10;"
        datas = self.application.executesDB(execute_sql)
        tags = self.application.selectDB('tags')
        for data in datas:
            result = dict()
            for key in keys:
                if key == 'ar_tags':
                    for tag in tags:
                        if tag['tag_id'] == data[keys.index(key)]:
                            result[key] = tag['tag_name']
                else:
                    result[key] = data[keys.index(key)]
            res.append(result)
        return res


#文章删除逻辑实现
class ArticalDelHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def get(self, id):
        drop_sql = "ar_id = %s" % id
        self.application.dropDB('artical', drop_sql)
        self.render("status.html", info="删除成功", url="/admin/artical.html")


# 渲染文章编写页面
class WriterHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        tags = self.application.selectDB('tags')
        self.render("admin/writer.html", tags=tags)


#文章编辑页面
class EditorHandler(BaseHandler.BaseHandler):
    """docstring for EditorHandler"""
    
    @tornado.web.authenticated
    def get(self, id):
        keys = ['ar_id', 'ar_tittle', 'ar_source', 'ar_date', 'ar_sketch', 'ar_thumbnail', 'ar_tags']
        tags = self.application.selectDB('tags')
        result = self.application.executeDB('select ar_id,ar_tittle,ar_source,ar_date,ar_sketch,ar_thumbnail,ar_tags from artical where ar_id = %s' % id)
        artical = dict()
        for key in keys:
            artical[key] = result[keys.index(key)]
        artical['ar_sketch'] = base64.b64decode(artical['ar_sketch'].encode("utf-8"))
        artical['ar_source'] = base64.b64decode(artical['ar_source'].encode("utf-8"))
        self.render("admin/editor.html", artical=artical, tags=tags)



#编辑文章提交实现
class EditorPostHandler(BaseHandler.BaseHandler):
    """docstring for EditorPostHandler"""
    
    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id")
        tittle = self.get_argument("tittle")
        sketch = self.get_argument("sketch")
        content = self.get_argument("content")
        date = self.get_argument("date")
        tags = self.get_argument("tags")
        source = self.get_argument("source")
        thumbnail = self.get_argument("thumbnail")
        update_sql = "ar_tittle='{}',ar_sketch='{}',ar_content='{}',ar_date='{}',\
            ar_tags='{}',ar_source='{}',ar_thumbnail='{}'".format(tittle, base64.b64encode(sketch.encode(encoding="utf-8")).decode(),\
             base64.b64encode(content.encode(encoding="utf-8")).decode(), date, tags, \
             base64.b64encode(source.encode(encoding="utf-8")).decode(), thumbnail)
        self.application.updateDB('artical', update_sql, 'ar_id=%s' % id)
        resp = {
            "status": 200,
            "msg": "更新成功"
        }
        self.write(resp)
        


# 新建文章提交实现代码
class WriterPostHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        tittle = self.get_argument("tittle")
        sketch = self.get_argument("sketch")
        content = self.get_argument("content")
        date = self.get_argument("date")
        tags = self.get_argument("tags")
        source = self.get_argument("source")
        thumbnail = self.get_argument("thumbnail")
        insert_sql = {
            "ar_id": "null",
            "ar_tittle": tittle,
            "ar_content": base64.b64encode(content.encode(encoding="utf-8")).decode(),  # 将文章内容进行base64编码
            "ar_source": base64.b64encode(source.encode(encoding="utf-8")).decode(),    # 将文章md源码进行base64编码
            "ar_date": date,
            "ar_sketch": base64.b64encode(sketch.encode(encoding="utf-8")).decode(),    # 将文章简介进行base64编码
            "ar_thumbnail": thumbnail,
            "ar_tags": int(tags)
        }
        self.application.insertDB('artical', insert_sql)
        self.write("发布成功")


# 渲染标签管理页面
class TagsHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        tags = self.getCount()
        self.render("admin/tags.html", tags=tags)

    def getTags(self):
        return self.application.selectDB("tags")

    def getCount(self):
        tags = self.getTags()
        for tag in tags:
            tag["count"] = self.application.executeDB("select count(*) from artical where ar_tags = %d" % tag["tag_id"])[0]
        return tags


# 添加标签实现
class TagsAddHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        tags_name = self.get_argument("tagsname")
        insert_sql = {
            "tag_id": "null",
            "tag_name": tags_name
        }
        self.application.insertDB('tags', insert_sql)
        self.write("添加成功!")


# 删除标签实现
class TagsDelHandler(BaseHandler.BaseHandler):

    @tornado.web.authenticated
    def get(self, id):
        drop_sql = "tag_id = %s" % id
        self.application.dropDB('tags', drop_sql)
        self.render("status.html", info="删除成功", url="/admin/tags.html")



#渲染wiki管理页面
class WikiManagerHandler(BaseHandler.BaseHandler):
    """docstring for WikiManagerHandler"""
    
    def get(self):
        wikis = self.application.selectDB('notes')
        self.render('admin/wiki.html', wikis=wikis)
        


#渲染wiki保存页面
class WikiWriteHander(BaseHandler.BaseHandler):
    """docstring for WikiWriteHander"""
    
    def get(self):
        categories = self.application.selectDB('note_categories')
        self.render('admin/wwriter.html', categories=categories)



#保存wiki实现
class WWritePostHander(BaseHandler.BaseHandler):
    """docstring for WWritePostHander"""
    
    def post(self):
        tittle = self.get_argument('tittle')
        content = self.get_argument('content')
        source = self.get_argument('source')
        cate = self.get_argument('cate')
        insert_sql = {
            "nt_id": "null",
            "nt_tittle": tittle,
            "nt_content": base64.b64encode(content.encode(encoding="utf-8")).decode(),
            "nt_source": base64.b64encode(source.encode(encoding="utf-8")).decode(),
            "nt_cate": int(cate)
        }
        self.application.insertDB("notes", insert_sql)
        resp = {
            "status": 200,
            "msg": "保存成功"
        }
        self.write(resp)
        
        

#wiki删除实现
class WikiDelHandler(BaseHandler.BaseHandler):
    """docstring for WikiDelHandler"""
    
    def get(self, id):
        self.application.dropDB('notes', 'nt_id=%s' %id)
        self.render("status.html", info="删除成功", url="/admin/wiki.html")


#渲染wiki分类管理页面
class WcategoriesHandler(BaseHandler.BaseHandler):
    """docstring for WcategoriesHandler"""
    
    def get(self):
        datas = self.application.selectDB('note_categories')
        for data in datas:
            data['count'] = self.getCount(data['nc_id'])[0]
        self.render('admin/wcategories.html', categories=datas)

    def getCount(self, id):
        res = self.application.executeDB('select count(*) from notes where nt_cate=%s' % id)
        return res



#渲染wiki修改页面
class WikiUpHandler(BaseHandler.BaseHandler):
    """docstring for WikiUpHandler"""
    
    def get(self, id):
        keys = ['nt_id', 'nt_tittle', 'nt_source', 'nt_cate']
        cate = self.application.selectDB('note_categories')
        result = self.application.executeDB('select nt_id,nt_tittle,nt_source,nt_cate from notes where nt_id = %s' % id)
        wiki = dict()
        for key in keys:
            wiki[key] = result[keys.index(key)]
        wiki['nt_source'] = base64.b64decode(wiki['nt_source'].encode("utf-8"))
        self.render("admin/weditor.html", wiki=wiki, cates=cate)



class WikiUpPostHandler(BaseHandler.BaseHandler):
    """docstring for WikiUpPostHandler"""
    
    def post(self):
        id = self.get_argument('id')
        tittle = self.get_argument('tittle')
        content = self.get_argument('content')
        source = self.get_argument('source')
        cate = self.get_argument('cate')
        # insert_sql = {
        #     "nt_id": "null",
        #     "nt_tittle": tittle,
        #     "nt_content": base64.b64encode(content.encode(encoding="utf-8")).decode(),
        #     "nt_source": base64.b64encode(source.encode(encoding="utf-8")).decode(),
        #     "nt_cate": int(cate)
        # }
        update_sql = "nt_id=null,nt_tittle='{}',nt_content='{}',nt_source='{}',nt_cate={}".format(tittle, \
            base64.b64encode(content.encode(encoding="utf-8")).decode(),base64.b64encode(source.encode(encoding="utf-8")).decode(),int(cate))
        self.application.updateDB('notes', update_sql, 'nt_id=%s' %id)
        resp = {
            "status": 200,
            "msg": "保存成功"
        }
        self.write(resp)
        


#添加wiki分类实现
class WcategoriesAddHandler(BaseHandler.BaseHandler):
    """docstring for WcategoriesHandler"""
    
    def post(self):
        name = self.get_argument('categoriesname')
        insert_sql = {
            "nc_id": "null",
            "nc_name": name
        }
        self.application.insertDB('note_categories', insert_sql)
        resp = {
            "status": 200,
            "msg": "添加成功"
        }
        self.write(resp)


#渲染yclass授权码管理页面
class YclassHandler(BaseHandler.BaseHandler):
    """docstring for ClassName"""
    
    def get(self):
        codes = self.application.selectDB('yclass_code')
        self.render('admin/ycode.html', codes=codes)



#yclass授权码添加
class YclassCodeHandler(BaseHandler.BaseHandler):
    """docstring for ClassName"""
    
    def post(self):
        code = ''
        words = ''.join((string.ascii_letters,string.digits))
        for i in range(6):
            code += random.choice(words)
        insert_sql = {
            "yc_id": "null",
            "code": code,
            "isuse": "False"
        }
        self.application.insertDB('yclass_code', insert_sql)
        resp = {
            "status": 200,
            "msg": code
        }
        self.write(resp)


class YcodeDelHandler(BaseHandler.BaseHandler):
    """docstring for YcodeDelHandler"""
    
    def get(self, id):
        drop_sql = "yc_id=%s" % id
        self.application.dropDB('yclass_code', drop_sql)
        self.render("status.html", info="删除成功", url="/admin/ycode.html")
        