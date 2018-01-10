#!/usr/bin/python
#-*- coding: UTF-8 -*-
import argparse
import yaml
import sys
import os
import time

from compress import compress
from split import split
from sendmail import SendMailDIY

class cmd():
	def __init__(self):
		config_handler = open("config.yaml")
		config_info = yaml.load(config_handler)
		self.comp = compress()
		self.codes = config_info['dir_backup']
		self.databases = config_info['mysql_backup']
		self.mail_recive = config_info['mail_recive']
		self.compress = config_info['compress']
		self.size_bag =self.compress['size_bag']
		self.gmail =config_info['gmail_send']
		self.split = split(self.size_bag)

	def codes_backup(self):
		self.codes_dict = {}
		for key,value in self.codes.items():
			file_compress = self.comp.doit(value,key,self.compress['password'])
			if file_compress:
				self.codes_dict[key] = file_compress
		return True

	def database_backup(self):
		self.databases_dict = {}
		for key,value in self.databases.items():
			filename = "/tmp/" + key + ".sql"
			os.popen("/usr/local/mysql/bin/mysqldump --default-character-set=utf8 %s > %s"  % (value,filename))
			file_compress = self.comp.doit(filename,key,self.compress['password'])
			if file_compress:
				os.remove(filename)
				self.databases_dict[key] = file_compress
		return True

	def file_split(self):
		self.message_dict = {}
		compress_files = dict(self.codes_dict,**self.databases_dict)
		print compress_files
		for key,value in compress_files.items():
			if os.path.getsize(value) <= self.size_bag*1024*1024:
				self.message_dict[key] = value
			else:
				files_split = self.split.split(value,key)
				for num in range(len(files_split)):
					subject = key + str(num+1)
					self.message_dict[subject] = files_split[num]
				os.remove(value)

	def sendmail(self):
		for key,value in self.message_dict.items():
			self.mail = SendMailDIY()
			self.mail.login_gmail(self.gmail['user'],self.gmail['password'])
			self.mail.subject(key)
			self.mail.content(key)
			self.mail.receiver(self.mail_recive)
			self.mail.attach(value)
			self.mail.perform()
			self.mail.logout()
			os.remove(value)
			time.sleep(300)


parser = argparse.ArgumentParser(usage=None,description="backup files or databases according to config")
parser.add_argument("-run",help="run backup process",action='store_true')
args = parser.parse_args()

if args.run:
	handler = cmd()
	handler.codes_backup()
	handler.database_backup()
	handler.file_split()
	handler.sendmail()