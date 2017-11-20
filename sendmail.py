#!/usr/bin/python
#-*- coding: UTF-8 -*-
import types

import smtplib
import email.mime.multipart
import email.mime.application
import email.mime.text

class SendMailDIY(object):
	""" Code sendmail class object
	发送邮件"""

	def __init__(self):

		self.msg = email.mime.multipart.MIMEMultipart()

	def login_gmail(self,username,password):
		'''use gmail account'''
		self.smtp=smtplib.SMTP('smtp.gmail.com',587)
		#smtp.set_debuglevel(1)
		self.smtp.ehlo()
		self.smtp.starttls()
		self.mail_from = username
		try:
			self.smtp.login(username,password)
			self.login = True
			return True
		except:
			self.login = False
			return False

	def anonymous(self):
		'''anonymous user'''
		self.smtp = smtplib.SMTP('localhost')
		self.mail_from = "user@anonymous.com"

	def subject(self,subject):
		self.msg['subject'] = subject

	def content(self,content='',content_file=''):
		'''content or contentfile'''
		if content != '':
			msg_content = email.mime.text.MIMEText(content,'html','utf-8')
		else:
			content = file(content_file).read()
			msg_content = email.mime.text.MIMEText(content,'html','utf-8')
		self.msg.attach(msg_content)

	def receiver(self,receiver):
		'''mail receiver user'''
		if isinstance(receiver,types.StringType):
			self.mailto = receiver
		if isinstance(receiver,types.ListType):
			self.mailto = receiver


	def attach(self,filename):
		'''add mail attachment'''
		if isinstance(filename,types.StringType):
			msg_attach = email.mime.application.MIMEApplication(open(filename,'rb').read())
			msg_attach.add_header('Content-Disposition', 'attachment', filename=filename)
			self.msg.attach(msg_attach)
			return True
		if isinstance(filename,types.ListType):
			for name in range(len(filename)):
				self.attach(name)
			return True

	def perform(self):
		'''send mail'''
		if self.login is False:
			self.anonymous()

		self.smtp.sendmail(self.mail_from,self.mailto,str(self.msg))

		self.smtp.quit()

# handler = mail()
# handler.login_gmail("user@gmail.com","password")
# handler.subject("test")
# handler.content("test content")
# handler.receiver("dst@dst.com")
# handler.attach("/root/123.zip")
# handler.perform()
