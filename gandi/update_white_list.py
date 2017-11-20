#!/usr/bin/python
#coding=utf-8
import socket
import commands
import os
def getIp(domain):
    myaddr = socket.getaddrinfo(domain,'http')[0][4][0]
    return myaddr
def readfile():
	Pre_file = file("file_of_ip","r")
	Pre_ip = Pre_file.read()
	Pre_file.close()
	return Pre_ip
def updatefile(new_ip):
	Pre_file = file("file_of_ip","w")
	Pre_ip = Pre_file.write(new_ip)
	Pre_file.close()

net_ip = getIp("www.loveu.com")
file_ip = readfile()
if net_ip != file_ip:
	updatefile(net_ip)

def update_nginx(pre_ip,new_ip):
	file_nginx = file("/usr/local/nginx/conf/nginx.conf","r+")
	d = file_nginx.read()
	d = d.replace(pre_ip,new_ip)
	print d
#	file_nginx.write(d)
	file_nginx.close()
def nginx_restart():
	nginx_test = os.system("/usr/local/nginx/sbin/nginx -t")
	if nginx_test == 0:
		return os.system("/usr/local/nginx/sbin/nginx -s reload")
update_nginx("gzip_http_version","mark")