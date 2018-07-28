import tornado.web
import pymysql
from config import DATABASE


class BaseHandler(tornado.web.RequestHandler):

    def session_handler(self):
        self.session = dict()
        self.cookie = self.get_cookie('xr_cookie')

    def conDB(self):
        self.con = pymysql.connect(host=DATABASE["host"], user=DATABASE["user"], password=DATABASE["password"], db=DATABASE["dbname"], port=DATABASE["port"], charset="utf8")
        dbCon = self.con.cursor()
        return dbCon

    def insertDB(self):
        keys = ''
        values = ''
        for key in self.insert_sql.keys():
            keys += key + ','
        for value in self.insert_sql.values():
            if isinstance(value, str):
                if value == "null":
                    values += value + ","
                else:
                    values += "'" + value + "\',"
            else:
                values += str(value) + ','
        DB = self.conDB()
        DB.execute("INSERT INTO {}({}) VALUES ({});".format(self.table, keys[:-1], values[:-1]))
        DB.execute("commit")
        DB.close()

    def selectDB(self):
        DB = self.conDB()
        DB.execute("desc %s;" %self.table)
        results = DB.fetchall()
        keys = []
        res = []
        for result in results:
            keys.append(result[0])
        DB.execute("SELECT * from %s;" % self.table)
        datas = DB.fetchall()
        DB.close()
        for data in datas:
            result = dict()
            for key in keys:
                result[key] = data[keys.index(key)]
            res.append(result)
        return res

    def dropDB(self):
        DB = self.conDB()
        DB.execute("DELETE FROM {} WHERE {}".format(self.table, self.drop_sql))
        DB.execute("commit")
        DB.close()

    def updateDB(self):
        DB = self.conDB()
        DB.execute("UPDATA {} SET {} WHERE {}".format(self.table, self.update_sql, where))
        DB.close()

    def executesDB(self):
        DB = self.conDB()
        DB.execute(self.execute_sql)
        res = DB.fetchall()
        DB.close()
        return res

    def executeDB(self):
        DB = self.conDB()
        DB.execute(self.execute_sql)
        res = DB.fetchone()
        DB.close()
        return res