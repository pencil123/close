#!/usr/bin/python
#-*- coding: UTF-8 -*-
import argparse
import yaml
import sys

from compress import compress

class cmd():
	def __init__(self):
		config_handler = open("config.yaml")
		config_info = yaml.load(config_handler)
		self.codes = config_info['dir_backup']
		self.databases = config_info['mysql_backup']
		self.mail_recive = config_info['mail_recive']
		self.compress = config_info['compress']

	def codes_backup(self):
		for key,value in self.codes.items():
			print key,value
			compress.doit(value,key,self.compress['password'])











parser = argparse.ArgumentParser(usage=None,description="backup files or databases according to config")
parser.add_argument("-run",help="run backup process",action='store_true')
args = parser.parse_args()

if args.run:
	handler = cmd()
	handler.codes_backup()