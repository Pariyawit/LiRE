# -*- coding: UTF-8 -*-
import BaseXClient
import numpy

import os
if (os.path.isdir("../database/")):
	path = "../database/"
else:
	path = "database/"

keyword_ref = dict()
lower_bound = 3
i=0
with open(path+'keywordcount_syn.txt',"r") as f:
	for line in f:
		keyword = line.split(',')
		keyword_ref[keyword[0]] = i
		i+=1
		#get number of keywords
		num = keyword[1].strip()
		if(int(num)<=lower_bound):
			break;

try:
	#create session
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("open bookref")
	print session.info()
	
	# run query on database, get all books noticekoha
	findbookref = '''for $book in /Document/book
						return ($book/text())'''
	query_bookref = session.query(findbookref)

	book_ref = dict()
	i=0
	for typecode, noticekoha in query_bookref.iter():
		if(noticekoha not in book_ref):
			book_ref[int(noticekoha)] = i
			i+=1

except IOError as e:
	# print exception
	print e

print 'keyword :',len(keyword_ref)
print 'book :',len(book_ref)

#table = [[0 for x in xrange(i)] for x in xrange(i)]

table = numpy.array([[0]*i]*i)
#table2 = numpy.array([[0]*i]*i)

print "calculate"
try:
	#create session
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("open keywordXML_syn")
	print session.info()
	
	# run query on database, get all books noticekoha
	findbookref = '''for $keyword in /keywordXML/classification/book
						return (data($keyword/@noticekoha),$keyword/keyword/text())'''
	query_bookref = session.query(findbookref)

	for typecode, out in query_bookref.iter():
		if(out.isdigit()):
			noticekoha = int(out)
			#print "NOTICE : ",noticekoha
			if noticekoha not in book_ref:
				noticekoha = False
		elif noticekoha:
			#print out.encode('UTF-8')
			if (out.encode('UTF-8') in keyword_ref):
				#print "key : ",keyword_ref[out.encode('UTF-8')]
				table[book_ref[noticekoha]][keyword_ref[out.encode('UTF-8')]] = 1
except IOError as e:
	print e

print "Calculating table x table.T..."

table = table.dot(table.T)
#print "calculating the second time"
#table = table.dot(table.T)
#result is matrix of book x book which [i][j] is number of common keyword of book i and book j

relatedBook = ElementTree.Element("relatedBook")
for noticekoha_row, ref_row in book_ref.iteritems():
	book = ElementTree.SubElement(relatedBook,"book")
	book.set('noticekoha',noticekoha_row)
	for noticekoha_col, ref_col in book_ref.iteritems():
		if(table[ref_row][ref_col]>0):
			relatedTo = ElementTree.SubElement(relatedTo,"relatedTo")
			relatedTo.set('score',table[ref][key_ref])
			relatedTo.text = noticekoha_col

#free memory of table
table = None

tree = ElementTree.ElementTree(relatedBook)
tree.write(path+'relatedBook.xml',encoding="UTF-8", xml_declaration=True)

xml = xmldom.parse(path+'relatedBook.xml')
pretty_xml_as_string = xml.toprettyxml()
#print pretty_xml_as_string
with open(outFile,"w") as f:
	f.write(pretty_xml_as_string.encode('utf8'));


'''
P = numpy.array(table)
print P

print "1 multiply matrix..."
P *= P.T

print "2 multiply matrix..."
P = numpy.dot(P,P.T)

print "3 multiply matrix..."
P = numpy.dot(P,P.T)

print "4 multiply matrix..."
P = numpy.dot(P,P.T)

print "5 multiply matrix..."
P = numpy.dot(P,P.T)

print P[0]
'''