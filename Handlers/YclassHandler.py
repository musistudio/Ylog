from Handlers import BaseHandler
import tornado.httpclient
from tornado.websocket import WebSocketHandler
import json
import urllib


class IndexHandler(BaseHandler.BaseHandler):

	def get(self):
		self.render("yclass/index.html")



class YclassSearch(BaseHandler.BaseHandler):
	"""docstring for YclassSearch"""
	
	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):
		school   = self.get_argument('school')
		client   = tornado.httpclient.AsyncHTTPClient()
		body     = "search=%s" % school
		headers  = {}
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/common/org/search",\
			method="POST", headers=headers, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		res = json.loads(response.body)
		self.write(res)
		self.finish()
		


class YclassLogin(BaseHandler.BaseHandler):
	"""docstring for YclassLogin
		登陆实现，将信息存入cookie
	"""
	
	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):
		type = self.get_argument("type")
		client   = tornado.httpclient.AsyncHTTPClient()
		headers  = {}
		if type == 'xh':
			school = self.get_argument("school")
			username = self.get_argument("snum")
			password = self.get_argument("spwd")
			code = self.get_argument("code")
			body     = "orgId={}&password={}&rememberMe=true&type=studentNo&username={}".format(school, password, username)
		else:
			username = self.get_argument('username')
			password = self.get_argument('password')
			code = self.get_argument('code')
			body = "&password={}&rememberMe=true&type=account&username={}".format(password, username)
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/system/login",\
			method="POST", headers=headers, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		res = json.loads(response.body)
		try:
			if code is not '':
				codes = self.application.executeDB("select * from yclass_code where code='%s' and isuse='False'" % code)
				if codes is None:
					resp = {
						"status": 401,
						"msg": "授权码错误"
					}
					self.write(resp)
				else:
					insert_sql = {
						"ya_id": "null",
						"ya_username": res["data"]["username"]
					}
					self.application.insertDB('yallow_users', insert_sql)
					self.application.updateDB("yclass_code", "isuse='True'", "code='%s'" %code)
					self.set_secure_cookie("token", res["data"]["token"])
					self.set_secure_cookie("realname", urllib.parse.quote(res["data"]["realname"]))
					rep = {
						"status": 200,
						"token": res["data"]["token"],
						"realname": res["data"]["realname"]
					}
					self.write(rep)
			else:
				users = self.application.executeDB("select * from yclass_users where yu_username='%s'" %res["data"]["username"])
				allow = self.application.executeDB("select * from yallow_users where ya_username='%s'" %res["data"]["username"])
				if users is None:
					insert_sql = {
						"yu_id": "null",
						"yu_useranme": res["data"]["username"],
						"yu_realname": res["data"]["realname"],
						"yu_email": res["data"]["email"],
						"yu_phone": res["data"]["mobile"]
					}
					self.application.insertDB('yclass_users', insert_sql)
				if allow is not None:
					rep = {
						"status": 200,
						"token": res["data"]["token"],
						"realname": res["data"]["realname"]
					}
					self.set_secure_cookie("token", res["data"]["token"])
					self.set_secure_cookie("realname", urllib.parse.quote(res["data"]["realname"]))
					print(res["data"]["token"], res["data"]["realname"])
					self.write(rep)
				else:
					rep = {
						"status": 500,
						"msg": "该用户没有使用资格"
					}
					self.write(rep)
		except TypeError:
			rep = {
					"status": 401,
					"msg": "用户名或密码错误"
				}
			self.write(rep)
		self.finish()


class YclassLogout(BaseHandler.BaseHandler):
	"""docstring for YclassLogout
		退出登陆，清除cookie
	"""
	def get(self):
		self.clear_cookie("token")
		self.clear_cookie("realname")
		self.write("已退出登陆")


class YclassList(BaseHandler.BaseHandler):
	"""docstring for YclassList
		获取课程列表
	"""
	
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		token = str(self.get_secure_cookie("token"), 'utf-8')
		realname = str(self.get_secure_cookie("realname"), 'utf-8')
		header = {
			"cookie": "token-student-zjedu={}; realname-student-zjedu={}; avatar-student-zjedu=null".format(token, realname)
		}
		body = ""
		client   = tornado.httpclient.AsyncHTTPClient()
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/system/list",\
			method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		dataLists = json.loads(response.body)['data']['dataList']
		self.render('yclass/class.html', classes=dataLists)


class YclassPass(BaseHandler.BaseHandler, WebSocketHandler):
	"""docstring for YclassVideo
	"""
	
	def get(self, id):
		self.render('yclass/pass.html', id=id)


class MessageHandler(WebSocketHandler):
	"""docstring for MessageHandler
		云端看课逻辑实现
	"""

	
	def open(self):
		self.realname = str(self.get_secure_cookie("realname"), 'utf-8')
		self.token = str(self.get_secure_cookie("token"), 'utf-8')
		self.header = {
			"cookie": "token-student-zjedu={}; realname-student-zjedu={}; avatar-student-zjedu=null".format(self.token, self.realname)
		}

	def on_message(self, messgae):
		course_id = messgae
		self.getPdfs(course_id, self.header)
		self.getVideos(course_id, self.header)

	def on_close(self):
		print(self)

	@tornado.web.asynchronous
	@tornado.gen.engine
	def getPdfs(self, course_id, header):
		body =  "courseId=%s" %course_id
		client   = tornado.httpclient.AsyncHTTPClient()
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/plan/list",\
			method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		# print(response.body)
		datas = json.loads(response.body)
		for data in datas['data']:
			for sections in data['data']:
				for section in sections['data']:
					if section['type'] == 3:
						data = 'courseId={}&playPosition=0&unitId={}'.format(course_id, section['unitId']) 
						request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/uploadLearnRate",\
							method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
						response = yield client.fetch(request)
						self.write_message(section['name']+'  云端看课(pdf)已完成')

	@tornado.web.asynchronous
	@tornado.gen.engine
	def getVideos(self, course_id, header):
		body =  "courseId=%s" %course_id
		client   = tornado.httpclient.AsyncHTTPClient()
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/achievement/video",\
			method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		datas = json.loads(response.body)
		videos = datas['data']
		i = 0
		while(i<len(videos)):
		    tm = videos[i]['duration'].split(":")
		    t = int(tm[1]) * 60 + int(tm[2])
		    j = 0
		    tim = 0
		    try:
		    	while(j<int(t/20)+1):
		    		data = 'courseId={}&playPosition={}&unitId={}'.format(course_id, tim, videos[i]['catalogId']) 
		    		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/uploadLearnRate",\
		    			method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
		    		response = yield client.fetch(request)
		    		j += 1
		    		tim += 20
		    	i += 1
		    	self.write_message(videos[i]['catalogName']+'  云端看课(视频)已完成')
		    except IndexError as e:
		    	self.write_message("云端看课(所有)已完成")
		
