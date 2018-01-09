#!/usr/bin/python
#-*- coding: UTF-8 -*-
import sys,os

class split():
	def __init__(self,size_bag=1):
		kilobytes = 1024
		megabytes = kilobytes*1024
		self.chunksize = int(size_bag*megabytes)

	def split(self,fromfile,todir):
		if os.path.exists(fromfile) is False:
			print "source file not exist!"
			return False
		todir = "/tmp/" + todir
		if not os.path.exists(todir):
			os.mkdir(todir)
		else:
			for fname in os.listdir(todir):
				os.remove(os.path.join(todir,fname))
		partnum = 0
		inputfile = open(fromfile,'rb')
		outputfiles = []
		while True:
			chunk = inputfile.read(self.chunksize)
			if not chunk: #check the chunk is empty
				break
			partnum += 1
			filename = os.path.join(todir,('part%04d'%partnum))
			fileobj = open(filename,'wb')#make partfile
			fileobj.write(chunk)         #write data into partfile
			fileobj.close()
			outputfiles.append(filename)
		return outputfiles