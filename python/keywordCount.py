# -*- coding: UTF-8 -*-
import BaseXClient
import string
import os
if (os.path.isdir("../database/")):
	path = "../database/"
elif (os.path.isdir("/database/")):
	path = "database/"
else:
	path = "../../database/"

try:

	#create session
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("open keywordXML")
	print session.info()
	
	# run query on database, get all books
	findkeywords = '''for $keyword in /keywordXML/category/book/keyword
				return ($keyword/text())'''

	query_keywords = session.query(findkeywords)

	keywords = dict()
	#get each book
	for typecode, keyword in query_keywords.iter():
		if(keyword not in keywords):
			keywords[keyword] = 0
		keywords[keyword] = keywords[keyword]+1

	#print classifications
	f = open(path+"keywordCount.txt",'wb')
	for w in sorted(keywords, key=keywords.get, reverse=True):
		#print w.encode('UTF-8'),',',keywords[w]
		if (w.encode('UTF-8').isdigit()):
			continue
		s = w.encode('UTF-8')+','+str(keywords[w])+'\n'
		f.write(s)

except IOError as e:
	# print exception
	print e