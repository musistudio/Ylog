from Handlers import BaseHandler
import base64

class IndexHandler(BaseHandler.BaseHandler):
    def get(self):
        datas = self.getData()
        for data in datas:
            for res in data:
                if res == 'ar_sketch':
                    try:
                        data[res] = base64.b64decode(data[res].encode("utf-8"))
                    except Exception:
                        print("the content is not base64")
        isLast = "true"
        page = self.getPage()
        if page > 1:
            isLast = "false"
        self.render("index.html", articals=datas, id=1, isLast=isLast)

    def getKeys(self):
        keys = []
        results = self.application.executesDB("desc artical;")
        for result in results:
            keys.append(result[0])
        return keys

    def getData(self):
        res = []
        keys = ['ar_id', 'ar_tittle', 'ar_date', 'ar_sketch', 'ar_thumbnail']
        datas = self.application.executesDB("SELECT ar_id,ar_tittle,ar_date,ar_sketch,ar_thumbnail from artical limit 0,5;")
        for data in datas:
            result = dict()
            for key in keys:
                result[key] = data[keys.index(key)]
            res.append(result)
        return res

    def getPage(self):
        count = self.application.executeDB("SELECT count(*) from artical;")[0]
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
        keys = ['ar_id', 'ar_tittle', 'ar_date', 'ar_sketch', 'ar_thumbnail']
        datas = self.application.executesDB("SELECT ar_id,ar_tittle,ar_date,ar_sketch,ar_thumbnail from {} limit {},5;".format(self.table, (int(self.id)-1)*5))
        for data in datas:
            result = dict()
            for key in keys:
                result[key] = data[keys.index(key)]
            res.append(result)
        return res

    def getPage(self):
        count = self.application.executeDB("SELECT count(*) from artical;")[0]
        if count % 5 == 0:
            page = (int(count / 5))
        else:
            page = (int(count / 5) + 1)
        return page