# -*- coding: UTF-8 -*-
import BaseXClient
import Classification
import xml.dom.minidom as xmldom
from array import *



class Categorytree(object):
	def getParent(nodename):
		return self.parentlist[nodename]
	def getChild(nodename):
		return self.childlist[nodename]
	def __init__(self):
		self.childlist = {}
		self.parentlist = {}
		self.categorylist = Classification.getclassificationrule()
		self.childlist['x'] = []
		for catnode in self.categorylist:
			if(Classification.isCat(catnode)):
				self.parentlist[catnode] = 'x'
				self.childlist['x'].append(catnode)
				self.childlist[catnode] = []
			elif(Classification.isSubcat(catnode)):
				self.parentnode = Classification.subcatToCat(catnode)
				self.parentlist[catnode] = self.parentnode
				self.childlist[self.parentnode].append(catnode) 

Cat = Categorytree()
