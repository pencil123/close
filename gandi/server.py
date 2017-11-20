#!/usr/bin/python
#coding=utf-8
import time
import os
import xmlrpclib
from rpyc import Service
from rpyc.utils.server import ThreadedServer
class monitor_call_func(Service):
	def __init__(self,conn_info):
		self.Domain_addr = os.environ.get('Domain_addr')
		self._conn=conn_info
	def change_domain_a(self,domain_addr):
		#update the os environ variable
		os.environ['Domain_addr'] = domain_addr
		print domain_addr
		api = xmlrpclib.ServerProxy('https://rpc.gandi.net/xmlrpc/')
		apikey = '-----------------'
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
		api.domain.zone.record.update(apikey,zone_work_id,update_version,{'id':update_record_id},{'ttl': 840, 'type': 'A', 'name': 'www', 'value': domain_addr})

		api.domain.zone.version.set(apikey,zone_work_id,update_version)

	def exposed_get_addr(self):
		s_ClientAdress, s_ClientPort=self._conn._config['endpoints'][1]
		if self.Domain_addr != s_ClientAdress:
			self.change_domain_a(s_ClientAdress)
			self.Domain_addr = s_ClientAdress
s=ThreadedServer(monitor_call_func,port=12233,auto_register=False)
s.start()