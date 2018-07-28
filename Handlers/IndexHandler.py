from Handlers import BaseHandler
import base64

class IndexHandler(BaseHandler.BaseHandler):
    def get(self):
        self.table = 'artical'
        datas = self.getData()
        # print(res)
        for data in datas:
            for res in data:
                if res == 'content':
                    try:
                        data[res] = base64.b64decode(data[res].encode("utf-8"))
                    except Exception:
                        print("the content is not base64")
        isLast = "false"
        page = self.getPage()
        if page >= 1:
            isLast = "true"
        self.render("index.html", articals=datas, id=1, isLast=isLast)

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
        self.execute_sql = "SELECT * from %s limit 0,5;" % self.table
        datas = self.executesDB()
        for data in datas:
            result = dict()
            for key in keys:
                result[key] = data[keys.index(key)]
            res.append(result)
        return res

    def getPage(self):
        self.execute_sql = "SELECT count(*) from artical;"
        count = self.executeDB()[0]
        if count % 5 == 0:
            page = (int(count / 5))
        else:
            page = (int(count / 5) + 1)
        return page


class ListHandler(IndexHandler):
    def get(self, id):
        self.table = 'artical'
        self.id = id
        res = self.getData()
        isLast = "false"
        page = self.getPage()
        if page < int(id):
            self.render("404.html")
        else:
            if page == int(id):
                isLast = "true"
            self.render("index.html", articals=res, id=self.id, isLast=isLast)

    def getData(self):
        res = []
        keys = self.getKeys()
        self.execute_sql = "SELECT * from {} limit {},5;".format(self.table, (int(self.id)-1)*5)
        datas = self.executesDB()
        for data in datas:
            result = dict()
            for key in keys:
                result[key] = data[keys.index(key)]
            res.append(result)
        return res