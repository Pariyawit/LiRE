# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
import Classification
from array import *
from collections import defaultdict

def findfavkeywords(uesrID):
	try:
		session1 = BaseXClient.Session('localhost',1984,'admin','admin')
		session2 = BaseXClient.Session('localhost',1984,'admin','admin')
		session1.execute('open distinctness')
		session2.execute('open loankeyfreq')
		print session1.info()

		# get a classification schema 
		categorylist = Classification.getclassificationrule()

		# declare a user's level of interest dictinary
		I = {}
		for cat in categorylist:
			I[cat] = defaultdict(float)

		find_ref = '''for $class in //Document/Row/user/*
					where $class/../@id="'''+str(userID)+'''"
					return (data($class/@category),$class/keyword/text(),data($class/keyword/@count),'$')'''
		query_ref = session2.query(find_ref)

		buff = []
		for typecode,ref in query_ref.iter():
			if(ref=='$'):
				category = buff[0]
				keyword = buff[1:(len(buff)/2)]
				count = buff[len(buff)/2+1:len(buff)-1]
				for j in range(0,len(keyword)):
					find_dtn = '''for $key in //Document/category/*
								where $key/../@code="'''+category+'''"
								and $key/text()="'''+keyword[j]+'''"
								return data($key/@distinctness)'''
					query_dtn = session1.query(find_dtn)
					for typecode,dtn in query_dtn.iter():
						I[category][keyword[j]] = float(count[j]) * float(dtn)
				buff = []
			else:
				buff.append(ref)
		
		for cat in categorylist:
			for key in I[cat]:
				print cat,key.encode('utf8')," - ",I[cat][key]
		session1.close()
		session2.close()

		return I
	except IOError as e:
		print e