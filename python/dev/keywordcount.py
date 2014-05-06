# -*- coding: UTF-8 -*-
import BaseXClient
import nltk
import string
from nltk.corpus import stopwords
from xml.etree import ElementTree
import xml.dom.minidom as xmldom
import os
if (os.path.isdir("../database/")):
	outFile = "../database/keywordcount.txt"
else:
	outFile = "database/keywordcount.txt"

try:

	#create session
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("open keywordXML")
	print session.info()
	
	# run query on database, get all books
	findkeyword = '''for $x in /keywordXML
				return ($x/classification/book/keyword/text())'''

	query_keyword = session.query(findkeyword)

	keywords = dict()
	#get each book
	for typecode, output in query_keyword.iter():
		if output not in keywords:
			keywords[output]=0
		keywords[output]+=1

	#print classifications
	f = open(outFile,'w')
	for w in sorted(keywords, key=keywords.get, reverse=True):
		#print w.encode('UTF-8'),',',keywords[w]
		s = w.encode('UTF-8')+','+str(keywords[w])+'\n'
		f.write(s)

except IOError as e:
	# print exception
	print e