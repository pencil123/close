#!/usr/bin/python3
from urllib.request import urlopen
import re

class domain():
	'''
	访问whois服务页面，抓取域名的信息
	'''
	DoInfo = {}
	GetInfo = ""
	DomainName = ""
	def first(self,TDomain):
		self.GetInfo="https://reports.internic.net/cgi/whois?whois_nic=" + TDomain + "&type=domain"
		self.DomainName = TDomain
	def DownLoad(self):
		self.GetInfo = urlopen(self.GetInfo).read().decode("gb2312")
		start = self.GetInfo.index("information.") + len("information.")
		end = self.GetInfo.index(">>>")
		self.GetInfo = self.GetInfo[start:end]
		return 1
	def ExceptInfo(self):
		self.DoInfo['status'] = 'false'
		self.DoInfo['DomainName'] = self.DomainName
		return 1
	def CurlInfo(self):
		end1 = self.GetInfo.index("Name Server:")
		start2 = self.GetInfo.index("Status")
		self.GetInfo = self.GetInfo[:end1] + self.GetInfo[start2:]
		self.GetInfo = "{\'" + self.GetInfo.strip().replace(': ','\':\'').replace(' ','').replace('\n','\',\'') + "\'}"
		self.DoInfo = eval(self.GetInfo)
		return 1
	def Judge(self,TDomain):
		self.first(TDomain)
		self.DownLoad()
		if self.GetInfo.find("No match for domain") == -1:
			self.CurlInfo()
		else:
			self.ExceptInfo()
		return self.DoInfo


class Random():
	'''
	递归函数实现十进制转为37位；
	37=10+26+1
	'''
	BaseT = ('-','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0')
	RadTotal = 1
	def Rstring(self,YNum):
		TheResturn = self.RCount(YNum)
		if TheResturn.endswith('-'):
			return 0
		else:
			return TheResturn
	def RCount(self,YNum):
		if YNum == 0:
			return ''
		else:
			str1 = self.RCount(YNum//37)
			return str1 + self.BaseT[YNum%37]

def main():
	TheRandom = Random()
	TheDomain = domain()
	out = open("out.txt","w+")
	def WriteDict(Ydict):
		Fline = ""
		for KeyString in ("DomainName","CreationDate","UpdatedDate","ExpirationDate","Status","Registrar"):
			if KeyString in Ydict:
				Fline = Fline + Ydict[KeyString] + " "
			else:
				Fline = Fline + "- "
		Fline = Fline + '\n'
		out.write(Fline)
	for i in range(1,pow(37,5)):
		RanString = TheRandom.Rstring(i)
		if RanString:
			RanString = RanString + '.com'
			DomainInfo = TheDomain.Judge(RanString)
			print(DomainInfo)
			WriteDict(DomainInfo)

if __main__ == "__main__":
	main()