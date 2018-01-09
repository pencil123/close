#!/usr/bin/python
#-*- coding: UTF-8 -*-
import pyminizip
import zipfile
import os

class compress(object):
	@staticmethod
	def doit(srcpath,dstname,password='',compress_level=3):
		'''initialization object'''
		if os.path.exists(srcpath) is False:
			print srcpath
			print "source file not exist!"
			return False
		
		if os.path.exists(dstname):
			print "dst file is exist!"
			return False

		if os.path.exists(os.path.dirname(dstname)) is False:
			print "create dst file directory"
			os.makedirs(os.path.dirname(dstname))

		self.compress_withpw(srcpath,dstname,password,compress_level)

	def compress_withpw(self,srcpath,dstname,password='',compress_level=3):
		'''加密压缩'''

		#single file compress
		if os.path.isfile(srcpath) is True:
			pyminizip.compress(srcpath,dstname,password,compress_level)
			return True

		if os.path.isdir(srcpath) is True:
			files_list = []

			for root,dirs,files in os.walk(srcpath):
				if dirs:
					break
				for name in files:
					files_list.append(os.path.join(root,name).encode('utf-8'))
				#empty directory compress
				if files_list is False:
					return False
		#Single-level directory 
		if files_list:
			pyminizip.compress_multiple(files_list,dstname,password,compress_level)
			return True
		#Multi-level directory
		else:
			tmp_zip_file = "/tmp/tmp.zip"
			self.compress(srcpath,tmp_zip_file)
			pyminizip.compress(tmp_zip_file,dstname,password,compress_level)
			os.remove(tmp_zip_file)


	def compress(self,srcpath,dstname):
		'''多级目录压缩'''
		
		zipHandler=zipfile.ZipFile(dstname,'w')
		for dirpath,dirs,files in os.walk(srcpath):
			for filename in files:
				zipHandler.write(os.path.join(dirpath,filename))
		zipHandler.close()


#compress_withpw("/root/compress",'/root/hello/123.zip','')