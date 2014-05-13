# -*- coding: UTF-8 -*-
#this python code make relatedBook.xml, relatedMatrix.txt
#very time consuming, run more than an hour
import BaseXClient
import numpy
import Queue
from xml.etree import ElementTree
import xml.dom.minidom as xmldom
import os
if (os.path.isdir("../database/")):
	path = "../database/"
else:
	path = "database/"

keyword_ref = dict()
lower_bound = 6
i=0
with open(path+'keywordCount.txt',"r") as f:
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
						return ($book/noticekoha/text())'''
	query_bookref = session.query(findbookref)

	book_ref = dict()
	i=0
	for typecode, noticekoha in query_bookref.iter():
		if(noticekoha not in book_ref):
			book_ref[noticekoha] = i
			i+=1

except IOError as e:
	# print exception
	print e

print "i = ",i
print 'keyword :',len(keyword_ref)
print 'book :',len(book_ref)

table = numpy.array([[0]*i]*i)
print "calculate"
try:
	#create session
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("open keywordXML")
	print session.info()
	
	# run query on database, get all books noticekoha
	findbookref = '''for $keyword in /keywordXML/category/book
						return (data($keyword/@noticekoha),$keyword/keyword/text())'''
	query_bookref = session.query(findbookref)

	for typecode, out in query_bookref.iter():
		if(out.isdigit()):
			noticekoha = out
		else:
			if (out.encode('UTF-8') in keyword_ref):
				if out.encode('UTF-8') not in keyword_ref :
					print "keyword not in"
				if noticekoha not in book_ref:
					print "noticekoha not in"
					print "==",noticekoha
					continue
				table[book_ref[noticekoha]][keyword_ref[out.encode('UTF-8')]] = 1
except IOError as e:
	print e

with open(path+"book_keyref.txt","w") as f:
	for noticekoha, ref in book_ref.iteritems():
		f.write(str(noticekoha)+","+str(ref)+"\n")

print "Calculating table x table.T..."
table = table.dot(table.T)

#result is matrix of book x book which [i][j] is number of common keyword of book i and book j
print "saving matrix"
numpy.savetxt(path+"relatedMatrix.txt",table,fmt="%d",delimiter=",",newline="\n",header=str(table.shape))

print "pushing top 10"
relatedBookResults = dict()
for noticekoha_row, ref_row in book_ref.iteritems():
	relatedBookResults[noticekoha_row]=Queue.PriorityQueue(maxsize=10)
	for noticekoha_col, ref_col in book_ref.iteritems():
		if(noticekoha_col!=noticekoha_row):
			item = (table[ref_row][ref_col],noticekoha_col)
			try:
				relatedBookResults[noticekoha_row].put_nowait(item)
			except:
				tmp = relatedBookResults[noticekoha_row].get()
				if tmp[0] > item[0]:
					relatedBookResults[noticekoha_row].put_nowait(tmp)
				else:
					relatedBookResults[noticekoha_row].put_nowait(item)

print "making xml"
relatedBook = ElementTree.Element("relatedBook")
for noticekoha, book_ref in relatedBookResults.iteritems():
	book = ElementTree.SubElement(relatedBook,"book")
	book.set('noticekoha',str(noticekoha))
	while (book_ref.qsize() > 0):
		tmp = book_ref.get()
		relatedTo = ElementTree.SubElement(book,"relatedTo")
		relatedTo.set('score',str(tmp[0]))
		relatedTo.text = str(tmp[1])

tree = ElementTree.ElementTree(relatedBook)

print "writing xml"
tree.write(path+'relatedBook.xml',encoding="UTF-8", xml_declaration=True)

xmlstr = ElementTree.tostring(tree.getroot(), encoding='utf8', method='xml')
session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
# create relatedBook database
session.execute("create db relatedBook")
session.add("relatedBook.xml", xmlstr)
session.close()

xml = xmldom.parse(path+'relatedBook.xml')
pretty_xml_as_string = xml.toprettyxml()

session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
session.add("relatedBook", pretty_xml_as_string)
with open(path+"keywordXML.xml","w") as f:
	f.write(pretty_xml_as_string.encode('utf8'));