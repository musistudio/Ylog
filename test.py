import pymysql
from config import DATABASE

# db = pymysql.connect(host=DATABASE["host"], user=DATABASE["user"], password=DATABASE["password"], db=DATABASE["dbname"], port=DATABASE["port"])
# dbs = db.cursor()
# dbs.execute("desc user;")
# results = dbs.fetchall()
# keys = []
# res = []
# for result in results:
#     keys.append(result[0])
# dbs.execute("select * from user;")
# datas = dbs.fetchall()
# db.close()
# for data in datas:
#     result = dict()
#     for key in keys:
#         result[key] = data[keys.index(key)]
#     res.append(result)
#
# print(res)

# sqls = {
#     "a": "1",
#     "b": 2,
#     "c": "3",
#     "d": 4
# }
# keys = ''
# values = ''
# for key in sqls.keys():
#     keys += key + ','
# for value in sqls.values():
#     if isinstance(value, str):
#         values += "'" + value + "\',"
#     else:
#         values += str(value) + ','
#
# print("INSERT INTO EMPLOYEE({}) VALUES ({})".format(keys[:-1], values[:-1]))

count = 11
if count % 5 == 0:
    print(int(count / 5))
else:
    print(int(count / 5)+1)
