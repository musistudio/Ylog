import tornado.web
import pymysql
from config import DATABASE

class Application(tornado.web.Application):
    """docstring for Application
        复写Application基类，用于注入mysql
    """
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = pymysql.connect(host=DATABASE["host"], user=DATABASE["user"], \
            password=DATABASE["password"], db=DATABASE["dbname"], port=DATABASE["port"], charset="utf8").cursor()

    def insertDB(self, table, insert_sql):
        keys = ''
        values = ''
        for key in insert_sql.keys():
            keys += key + ','
        for value in insert_sql.values():
            if isinstance(value, str):
                if value == "null":
                    values += value + ","
                else:
                    values += "'" + value + "\',"
            else:
                values += str(value) + ','
        self.db.execute("INSERT INTO {}({}) VALUES ({});".format(table, keys[:-1], values[:-1]))
        self.db.execute("commit")

    def selectDB(self, table):
        self.db.execute("desc %s;" %table)
        results = self.db.fetchall()
        keys = []
        res = []
        for result in results:
            keys.append(result[0])
        self.db.execute("SELECT * from %s;" % table)
        datas = self.db.fetchall()
        for data in datas:
            result = dict()
            for key in keys:
                result[key] = data[keys.index(key)]
            res.append(result)
        return res

    def dropDB(self, table, drop_sql):
        self.db.execute("DELETE FROM {} WHERE {}".format(table, drop_sql))
        self.db.execute("commit")

    def updateDB(self, table, update_sql, where):
        self.db.execute("UPDATE {} SET {} WHERE {}".format(table, update_sql, where))

    def executesDB(self, execute_sql):
        self.db.execute(execute_sql)
        res = self.db.fetchall()
        return res

    def executeDB(self, execute_sql):
        self.db.execute(execute_sql)
        res = self.db.fetchone()
        return res