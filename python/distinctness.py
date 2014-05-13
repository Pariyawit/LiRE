# -*- coding: UTF-8 -*-

import BaseXClient
import Classification
import Tree
import math
import xml.dom.minidom as xmldom
from array import *
from collections import defaultdict

try:
	session1 = BaseXClient.Session('localhost',1984,'admin','admin')
	session2 = BaseXClient.Session('localhost',1984,'admin','admin')
	session1.execute('open keyword')
	session2.execute('create db distinctness')

	categorylist = Classification.getclassificationrule()

	# Prepare dictionaries
	kf = {}
	siblingcount = {}
	siblingkeyword = {}
	distinctness = {}

	# Create a Category Tree. this will be later used for finding sibling of the category.
	cattree = Tree.Categorytree()

	# Count the amount of sibling categories for each category
	for cat in categorylist:
		siblingcount[cat] = len(cattree.getSibling(cat))

	# Calculate keyword frequency in a category, store it to the kf table
	for cat in categorylist:
		kf[cat] = defaultdict(int)
		if(Classification.isSubcat(cat)):
			parentcat = cattree.getParent(cat)
			findcount = '''for $class in //keywordXML/*
						where data($class/@category)="'''+cat+'''"
						return $class/book/keyword/text()'''
			querycount = session1.query(findcount)
			for typecode,ref in querycount.iter():
				kf[parentcat][ref.encode('utf8')] += 1
				kf[cat][ref.encode('utf8')] += 1

	# Calculate keyword frequency in sibling's categories, store it to siblingkeyword table
	for cat in categorylist:
		siblingkeyword[cat] = defaultdict(int)
		siblingcats = cattree.getSibling(cat)
		for ref in kf[cat]:
			for scat in siblingcats:
				if(kf[scat][ref] > 0 and kf[cat][ref]>0):
					siblingkeyword[cat][ref] += 1


	# Calculate Distinctness value of keywords in a category, store it to distinctness table
	# Also write to file at the time

	xml = '<Document>'
	for cat in categorylist:
		distinctness[cat] = defaultdict(float)
		xml += '<category code="'+cat+'">'
		for ref in kf[cat]:
			if(kf[cat][ref] == 0): continue
			print cat,ref,float(kf[cat][ref]),"-",float(siblingcount[cat]),"-",float(siblingkeyword[cat][ref]),"-",math.log(float(siblingcount[cat])/float(siblingkeyword[cat][ref]))
			distinctness[cat][ref] = float(kf[cat][ref]) * math.log(float(siblingcount[cat])/float(siblingkeyword[cat][ref]))
			xml += '<keyword distinctness="'+str(distinctness[cat][ref]).encode('utf8')+'">'+str(ref)+'</keyword>'
		
		xml += '</category>'

	xml += '</Document>'
	session1.close()

	session2.add('distinctnesstable.xml',xml)
	xml = xmldom.parseString(xml)
	pretty_xml_as_string = xml.toprettyxml()

	with open('../database/distinctnesstable.xml','w') as f:
		f.write(pretty_xml_as_string.encode('utf8'))

	session2.close()
except IOError as e:
	print e