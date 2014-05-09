# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
import Classification
import Tree
from array import *
from collections import defaultdict
from sets import Set

def bookselection(userID, I):
	try:
		session1 = BaseXClient.Session('localhost',1984,'admin','admin')
		session1.execute('open keyword')
		print session1.info()

		recommend = {}
		categorylist = Classification.getclassificationrule()
		for cat in categorylist:
			recommend[cat] = defaultdict(float)

		for cat in I:
			find_ref = '''for $book in //keywordXML/classification/*
						where $book/../@code="'''+cat+'''"
						return (data($book/@noticekoha),$book/keyword/text(),'$')'''
			query_ref = session1.query(find_ref)
			buff = []
			for typecode,ref in query_ref.iter():
				if(ref=='$'):
					noticekoha = buff[0]
					for keyword in buff[1:len(buff)-1]:
						if(I[cat][keyword] > 4.0):
							if(I[cat][keyword] > recommend[cat][noticekoha]):
								recommend[cat][noticekoha] = I[cat][keyword]
								
					buff = []
				else:
					buff.append(ref)

		session1.close()

		return recommend
	except IOError as e:
		print e