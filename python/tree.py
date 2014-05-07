# -*- coding: UTF-8 -*-
import BaseXClient
import Classification
import xml.dom.minidom as xmldom
from array import *



class Categorytree(object):
	def getParent(self, nodename):
		return self.parentlist[nodename]
	def getChild(self, nodename):
		return self.childlist[nodename]
	def getSibling(self, nodename):
		self.parent = self.parentlist[nodename]
		self.sibling = self.getChild(self.parent)
		return self.sibling
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

