# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
from array import *
try:
	session1 = BaseXClient.Session('localhost', 1894, 'admin', 'admin')
	session2 = BaseXClient.Session('localhost', 1894, 'admin', 'admin')
	session1.execute("open lecteur")
	session2.execute("open historique")
	findUser = '''for $row in //Row/*
				return ($row/../CARDNUMBER/text())'''
	queryUser = session1.query(findUser)
	print session1.info()

	classification = []
	with open('../classification.txt','r') as f:
		buff = f.readline()
		i = buff.index(' ')
		classification.append(buff[0:i])

	for typecode,ref in queryUser.iter():
		for findBorrowed = '''for $trans in /historique/* 
						where $trans/codebarrelecteur="'''+ref+'''"
						return $trans/noticekoha/text()'''
		queryBorrowed = session2.query(findBorrowed)
		print 

	session1.close()
	session2.close()

	sesson = BaseXClient.Session('localhost', 1894, 'admin', 'admin')
	session.add('loanfreqtable.xml',xml)
	#print xml
	xml = xmldom.parseString(xml)
	pretty_xml_as_string = xml.toprettyxml()
	
	with open('../loanfreqtable.xml','w') as f:
		f.write(pretty_xml_as_string.encode('utf8'))
except IOError as e:
	# print exception
	print e

