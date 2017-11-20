#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import cookielib
import random
import string
import re
import time
import sys
import httplib
import mimetools
import mimetypes

httplib.HTTPConnection.debuglevel = 1

class DiscuzAPI:
	def __init__(self, forumUrl, proxy = None):
		''' 初始化论坛url代理服务器 '''
		self.forumUrl = forumUrl
		self.formhash = ''
		self.isLogon = False
		self.isSign = False
		self.xq = ''
		self.jar = cookielib.CookieJar()
		if not proxy:
			openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.jar))
		else:
			openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.jar), urllib2.ProxyHandler({'http' : proxy}))
		urllib2.install_opener(openner)
 
	def login(self,username,password):
		''' 登录论坛 '''
		url = self.forumUrl + "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&inajax=1";

		postData = urllib.urlencode({'username': username, 'password': password, 'answer': '', 'cookietime': '2592000', 'handlekey': 'ls', 'questionid': '0', 'quickforward': 'yes',  'fastloginfield': 'username'})
		req = urllib2.Request(url,postData)
		content = urllib2.urlopen(req).read()
		if username.encode('utf-8') in content:
			self.isLogon = True
			print 'logon success!'
			self.initFormhashXq()
			return 1
		else:
			print 'logon faild!'
			return 0
 
	def initFormhashXq(self):
		''' 获取formhash和心情 '''
		content = urllib2.urlopen(self.forumUrl + '/plugin.php?id=dsu_paulsign:sign').read().decode('utf-8')
		rows = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', content)
		if len(rows)!=0:
			self.formhash = rows[0]
			print 'formhash is: ' + self.formhash
		else:
			print 'none formhash!'
		rows = re.findall(r'<input id=.* type=\"radio\" name=\"qdxq\" value=\"(.*?)\" style=\"display:none\">', content)
		if len(rows)!=0:
			self.xq = rows[0]
			print 'xq is: ' + self.xq
		elif u'已经签到' in content:
			self.isSign = True
			print 'signed before!'
		else:
			print 'none xq!'
 
	def reply(self, tid, subject = u'',msg = u'支持~~~顶一下下~~嘻嘻'):
		''' 回帖 '''
		url = self.forumUrl + '/forum.php?mod=post&action=reply&fid=41&tid='+str(tid)+'&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1'
		postData = urllib.urlencode({'formhash': self.formhash, 'message': msg.encode('utf-8'), 'subject': subject.encode('utf-8'), 'posttime':int(time.time()) })
		req = urllib2.Request(url,postData)
		content = urllib2.urlopen(req).read().decode('utf-8')
		#print content
		if u'发布成功' in content:
			print 'reply success!'
		else:
			print 'reply faild!'

	def publish(self,fid,subject=u'发帖测试，主题',msg=u'发帖测试一下；内容~~~~~~~',imgId = "",attachId = ""):
		'''发帖'''

		url = self.forumUrl + '/forum.php?mod=post&action=newthread&fid=' + str(fid) + '&topicsubmit=yes&infloat=yes&handlekey=fastnewpost&inajax=1'
		refer = self.forumUrl + "/forum.php?mod=forumdisplay&fid=%d" % fid
		postData = urllib.urlencode(
			{'formhash':self.formhash,
			'message':msg,#.encode('utf-8'),
			'subject':subject,#.encode('utf-8'),
			'posttime':int(time.time()),
			'addfeed':'1', 
			'allownoticeauthor':'1', 
			'checkbox':'0', 
			'newalbum':'', 
			'readperm':'', 
			'rewardfloor':'', 
			'rushreplyfrom':'', 
			'rushreplyto':'', 
			'save':'', 
			'stopfloor':'', 
			#'typeid':typeid,
			'attachnew[%s][description]' % imgId: "",
			'attachnew[%s][description]' % attachId: "",
			'uploadalbum':'', 
			'usesig':'1', 
			'wysiwyg':'0' })
		req = urllib2.Request(url,postData)
		req.add_header('Referer',refer)
		content = urllib2.urlopen(req).read().decode('utf-8')
		if u"您的主题已发布" in content:
			print 'publish success!'
			return 1
		else:
			print 'publish faild!'
			print content
			exit()
			return 0

	def uploadImage(self,imageData, fid=48,imgname="default.jpg",imgtype="jpg"):
		imageId = None
		#上传图片

		url = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		data = urllib2.urlopen(url).read().decode('utf-8')

		pattern = re.compile(r'hash\":\"(.*?)\"',re.M)
		hash_list = pattern.findall(data)
		print hash_list
		# Upload the image
		uploadImageUrl = self.forumUrl + "/misc.php?mod=swfupload&operation=upload&simple=1&type=image"
		refer = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		randomStr = "7dd" + ''.join( random.sample(string.ascii_lowercase + string.digits, 8) )
		CRLF = '\r\n'
		#BOUNDARY = mimetools.choose_boundary()
		BOUNDARY = "---------------------------" + randomStr
		L = []
		L.append('--' + BOUNDARY)
		L.append("Content-Disposition: form-data; name=\"uid\""  )
		L.append("")
		L.append("2")
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"hash\"')
		L.append("")
		L.append(hash_list[0])
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"Filedata\"; filename=\"' + imgname + '\"')
		L.append("Content-Type: image/" + imgtype)
		L.append("")
		L.append( imageData )
		L.append('--' + BOUNDARY + '--')
		L.append("")
		postData = CRLF.join(str(a) for a in L)
		#print postData

		req = urllib2.Request(uploadImageUrl, postData) 
		req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % BOUNDARY )
		req.add_header('Content-Length',  len(postData) )
		req.add_header('Referer', refer )
		resp = urllib2.urlopen(req)
		body = resp.read().decode('utf-8')
		bodySp = body.split('|')
		if len(bodySp) == 0:
			return None
		if bodySp[0] == u'DISCUZUPLOAD' and bodySp[1] == u'0':
			imageId = bodySp[2]
		return imageId

	def uploadAttach(self,imageData, fid=48,btname="default.torrent"):
		imageId = None
		# 上传附件

		url = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		data = urllib2.urlopen(url).read().decode('utf-8')

		pattern = re.compile(r'hash\":\"(.*?)\"',re.M)
		hash_list = pattern.findall(data)
		print hash_list
		# Upload the image
		uploadImageUrl = self.forumUrl + "/misc.php?mod=swfupload&operation=upload&simple=1"
		refer = self.forumUrl + "/forum.php?mod=post&action=newthread&fid=%d&extra=" % fid
		randomStr = "7dd" + ''.join( random.sample(string.ascii_lowercase + string.digits, 8) )
		CRLF = '\r\n'
		#BOUNDARY = mimetools.choose_boundary()
		BOUNDARY = "---------------------------" + randomStr
		L = []
		L.append('--' + BOUNDARY)
		L.append("Content-Disposition: form-data; name=\"uid\""  )
		L.append("")
		L.append("2")
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"hash\"')
		L.append("")
		L.append(hash_list[0])
		L.append('--' + BOUNDARY)
		L.append('Content-Disposition: form-data; name=\"Filedata\"; filename=\"' + btname + '\"')
		L.append("Content-Type: application/torrent")
		L.append("")
		L.append( imageData )
		L.append('--' + BOUNDARY + '--')
		L.append("")
		postData = CRLF.join(str(a) for a in L)

		req = urllib2.Request(uploadImageUrl, postData) 
		req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % BOUNDARY )
		req.add_header('Content-Length',  len(postData) )
		req.add_header('Referer', refer )
		resp = urllib2.urlopen(req)
		body = resp.read().decode('utf-8')
		print body
		bodySp = body.split('|')
		if len(bodySp) == 0:
			return None
		if bodySp[0] == u'DISCUZUPLOAD' and bodySp[1] == u'0':
			imageId = bodySp[2]
		return imageId