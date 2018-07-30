from Handlers import BaseHandler
import tornado.httpclient
import json
import urllib


class IndexHandler(BaseHandler.BaseHandler):

	def get(self):
		self.render("yclass/index.html")


class YclassLogin(BaseHandler.BaseHandler):
	"""docstring for YclassLogin
		登陆实现，将信息存入cookie
	"""
	
	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		print(username, password)
		self.table = "yclass_allow"
		allows = self.selectDB()
		client   = tornado.httpclient.AsyncHTTPClient()
		body     = "orgId=85&password={}&rememberMe=true&type=studentNo&username={}".format(password, username)
		headers  = {}
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/system/login",\
			method="POST", headers=headers, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		res = json.loads(response.body)
		for allow in allows:
			try:
				if res["data"]["username"] in allow["username"]:
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
					self.write("该用户没有使用资格")
			except TypeError:
				rep = {
					"status": 401,
					"msg": "用户名或密码错误"
				}
				self.write(rep)
		self.finish()


class YclassLogout(BaseHandler.BaseHandler):
	"""docstring for YclassLogout
		退出登陆，清楚cookie
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
		print(header)
		body = ""
		client   = tornado.httpclient.AsyncHTTPClient()
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/system/list",\
			method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		# dataLists = json.loads(response.body)['data']['dataList']
		self.write(response.body)
		self.finish()


class YclassPass(BaseHandler.BaseHandler):
	"""docstring for YclassVideo
		云端看课实现逻辑
	"""
	
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		# course_id = self.get_argument("course_id")
		course_id = "30002928"
		token = str(self.get_secure_cookie("token"), 'utf-8')
		realname = str(self.get_secure_cookie("realname"), 'utf-8')
		header = {
			"cookie": "token-student-zjedu={}; realname-student-zjedu={}; avatar-student-zjedu=null".format(token, realname)
		}
		self.getPdfs(course_id, header)
		self.getVideos(course_id, header)
		self.write("success")
		self.finish()

	@tornado.web.asynchronous
	@tornado.gen.engine
	def getPdfs(self, course_id, header):
		body =  "courseId=%s" %course_id
		client   = tornado.httpclient.AsyncHTTPClient()
		request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/plan/list",\
			method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
		response = yield client.fetch(request)
		datas = json.loads(response.body)
		# self.finish()
		for data in datas['data']:
			for sections in data['data']:
				for section in sections['data']:
					if section['type'] == 3:
						data = 'courseId={}&playPosition=0&unitId={}'.format(course_id, section['unitId']) 
						request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/uploadLearnRate",\
							method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
						response = yield client.fetch(request)
						print(section['name']+'  云端看课(pdf)已完成')

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
		    while(j<int(t/20)+1):
		        data = 'courseId={}&playPosition={}&unitId={}'.format(course_id, tim, videos[i]['catalogId']) 
		        request  = tornado.httpclient.HTTPRequest("http://student.zjedu.moocollege.com/nodeapi/3.0.1/student/course/uploadLearnRate",\
		        	method="POST", headers=header, body=body.encode("utf-8"), validate_cert=False)
		        response = yield client.fetch(request)
		        j += 1
		        tim += 20
		    i += 1
		    print(videos[i]['catalogName']+'  云端看课(视频)已完成')
