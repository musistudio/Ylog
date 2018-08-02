from Handlers import BaseHandler
import base64

class PostsHandler(BaseHandler.BaseHandler):
    def get(self, id):
    	isLast = 'False'
    	isFirst = 'False'
    	first = self.application.executeDB("SELECT count(*) from artical where ar_id <= %s;" % id)[0]
    	last = self.application.executeDB("SELECT count(*) from artical where ar_id >= %s;" % id)[0]
    	if first == 0:
    		self.render("404.html")
    	else:
        	if first == 1:
        		isFirst = "true"
    	if last == 0:
    		self.render("404.html")
    	else:
        	if last == 1:
        		isLast = "true"
    	keys = ['ar_tittle', 'ar_content', 'ar_date', 'ar_tags']
    	select_sql = 'select ar_tittle,ar_content,ar_date,ar_tags from artical where ar_id = %s' %id
    	datas = self.application.executesDB(select_sql)
    	tags = self.application.selectDB('tags')
    	for data in datas:
    		result = dict()
    		for key in keys:
    			result[key] = data[keys.index(key)]
    	result['ar_content'] = base64.b64decode(result['ar_content'].encode('utf-8'))
    	for tag in tags:
            if tag['tag_id'] == result['ar_tags']:
                result['ar_tags'] = tag['tag_name']
    	self.render("artical.html", artical=result, id=id, isFirst=isFirst, isLast=isLast)

    def getCount(self):
        count = self.application.executeDB("SELECT count(*) from artical;")[0]
        return count