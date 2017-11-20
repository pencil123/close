#!/usr/bin/env python
#-*- coding: utf-8 -*-
import xmlrpclib
import pycurl
import re
import StringIO
import socket
import sys
api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')

apikey = '------------------'

def GetIP():
	#Get the host IP
	ipcontent = StringIO.StringIO()
	curl = pycurl.Curl()
	curl.setopt(pycurl.WRITEFUNCTION,ipcontent.write)
	curl.setopt(pycurl.USERAGENT,"curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.19.1 Basic ECC zlib/1.2.3 libidn/1.18 libssh2/1.4.2")
	curl.setopt(pycurl.URL,"http://ip.cn")
	curl.perform()
	reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
	Theip = reip.findall(ipcontent.getvalue())[0]
	return Theip

DomainIP = socket.getaddrinfo('www.loveu.com','http')[0][4][0]
myaddr = GetIP()
if myaddr == DomainIP:
	sys.exit(0)
# Now you can call API methods.
# You must authenticate yourself by passing
# the API key as the first method's argument
version = api.version.info(apikey)
#print version

#Get the work domain id
domain_infos = api.domain.info(apikey,'loveu.com')
zone_work_id = domain_infos['zone_id']

#Get the work domain record version id
zones = api.domain.zone.list(apikey)
print zones
for zone_id in zones:
	if zone_id['id'] == zone_work_id:
		zone_work_tag = zone_id
zone_record_version = zone_work_tag['version']

#update the other record version

if zone_record_version == 8:
	update_version = 7
else:
	update_version = 8

#get the record version www domain id
record_infos = api.domain.zone.record.list(apikey,zone_work_id,update_version)
for record_info in record_infos:
	if record_info['name'] == 'www':
		update_record_id = record_info['id']
print update_record_id

#execute the domain record update
api.domain.zone.record.update(apikey,zone_work_id,update_version,{'id':update_record_id},{'ttl': 840, 'type': 'A', 'name': 'www', 'value': myaddr})

api.domain.zone.version.set(apikey,zone_work_id,update_version)


