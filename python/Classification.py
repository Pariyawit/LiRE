# -*- coding: UTF-8 -*-
import BaseXClient
import xml.dom.minidom as xmldom
from array import *
from collections import defaultdict


# This method returns true if the input string is in the right format for a subcategory
# for example, cls = '10.1'
def isSubcat(cls):
	if(len(cls)>2): return True
	else: return False

# This method returns true if the input string is in the right format for a category
# for example, cls = '10'
def isCat(cls):
	if(len(cls)==2): return True
	else: return False

# This method returns a category list derived from classification schema.
def getclassificationrule():
	f = open("../database/classification.txt","r")
	categorylist = []
	for buff in f:
		i = buff.index(' ')
		catcode = buff[0:i]
		categorylist.append(catcode)
	return categorylist

# This method transform a subcategory to its parent category
# for example, "01.6" -> "01"
def subcatToCat(category):
	try:
		buff = category.index('.')
		buff = category.split('.')
		return buff[0]
	except ValueError as v:
		return -1

# A method to clean the class received from query and transform to its category.
# for example, "1.66 PENN" -> "01.6"
def classToCategory(cls):
	try:
		split = cls.index(' ')
	except ValueError as v:
		try:
			split = cls.index('-')
		except ValueError as ve:
			split = len(cls)
	cls = cls[0:split]
	try:
		split = cls.index('.')
	except ValueError as ve:
		return 'ERROR'
	if(cls.index('.') == 1 ):
		cls = "0" + cls
	pointIndex = cls.index('.')
	cls = cls[0:pointIndex+2]
	return cls

# There are some issues with book's class started with an character like 'D 10.02 COHE', 'ARCH. C7.4 EMC/91', 'C2.701 RUD'
# This method is used to trim out the redundant characters positioned before the number
# for example, 'C2.701 RUD' -> '2.701 RUD'
def classtrim(cls):
	for i in range(0,len(cls)):
		if(cls[i].isdigit()):
			cls = cls[i:len(cls)]
			return cls
	#print "notrim" + cls
	return ValueError

