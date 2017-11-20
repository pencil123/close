#!/usr/bin/python
#coding=utf-8
import rpyc
hi=rpyc.connect("www.example",12233)
hi.root.exposed_get_addr()
hi.close()
