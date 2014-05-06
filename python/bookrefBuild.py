# -*- coding: UTF-8 -*-
import BaseXClient
import xml.dom.minidom as xmldom
from array import *

import os
if (os.path.isdir("../database/")):
	outFile = "../database/bookref.xml"
else:
	outFile = "database/bookref.xml"

classification = ["0.","0.1","0.2","0.3","0.4","1.","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.","2.1","2.2","2.3","2.4","2.5","2.6","2.7","3.","3.1","3.2","3.3","3.4","3.5","3.6","3.7","3.8","3.9","4.","4.1","4.2","4.3","4.4","4.5","4.6","5.","5.1","5.2","5.3","5.4","5.5","5.6","6.","6.1","6.2","6.3","6.4","6.5","6.6","6.7","6.8","6.9","7.","7.1","7.2","7.3","7.4","8.","8.1","8.2","8.3","8.4","8.5","8.6","8.7","9.","9.1","9.2","9.3","9.4","9.5","10.","10.1","10.2","10.3","10.4","10.5","10.6","10.7","11.","11.1","11.2","11.3","11.4","11.5","11.6","11.7","12.","12.1","12.2","12.3","12.4","12.5","12.6","12.7"]

# A method to clean the class received from query and transform to its category.
# for example, "1.66 PENN" -> "01.6"
def classToCategory(cls):
	tmp = cls
	try:
		split = cls.index(' ')
	except ValueError as v:
		try:
			split = cls.index('-')
		except ValueError as ve:
			split = len(cls)
	#print "--->" + cls.encode('utf8')
	cls = cls[0:split]
	try:
		split = cls.index('.')
	except ValueError as ve:
		return 'N'
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

try:
	session = BaseXClient.Session('localhost',1984,'admin','admin')
	session1 = BaseXClient.Session('localhost',1984,'admin','admin')
	session.execute("open extraction")
	session1.execute("create db bookref")
	print session.info()
	# run query on database, get all books
	findref = '''declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
 				for $record in //marcxml:record
				where $record/marcxml:datafield[@tag="995"]/marcxml:subfield[@code="e"]="BSTB"
				and $record/marcxml:datafield[@tag="995"]/marcxml:subfield[@code="r"]="OUV"
				and $record/marcxml:datafield[@tag="930"]/marcxml:subfield[@code="a"]/text()[contains(.,".")]
				return (distinct-values($record/marcxml:datafield[@tag="995"]/marcxml:subfield[@code="k"]/text()),
					distinct-values($record/marcxml:datafield[@tag="930"]/marcxml:subfield[@code="a"]/text()),"#",
					$record/marcxml:controlfield[@tag="001"]/text(),
					$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),"$")'''

	query_ref = session.query(findref)
	buff = []


	xml = '<Document>'
	for typecode, ref in query_ref.iter():
		#print ref.encode('utf8')
		if(ref=='$'):
			classes = buff[0:buff.index('#')]
			bookclass = ""
			noticekoha = buff[len(buff)-2]
			title = buff[len(buff)-1]


			# Clean book's class by comparing the 930/a subfields with 995/k subfields ( both 930/a and 995/k can be replicated)
			# because sometimes these fields are correspond to different value, even though it should always be the same
			# if they are different, finding the more suitable one to used as the book's class
			# for example, sometimes 930/a = D8 ENG/S, while 995/k = D 8.02 SIPP
			# from the above example, the 995/k subfield is preferred because it is in the right format (having '.')

			for cls in classes:
				try:
					cls = classtrim(cls)
					if(cls == ValueError): continue
					try:
						k = cls.index('.')
						try:
							k = cls.index('-')
							for j in cls:
								if(j=='-'): j==' '
							bookclass = cls
							break
						except ValueError as ve:
							bookclass = cls
					except ValueError as ve:
						continue
				except ValueError as ve:
					continue
			else:
				print classes
			#print bookclass.encode('utf8')
			
			#print buff
			buff = []
			xml += '<book class="'+str(bookclass.encode('utf8'))+'">'
			xml += '<title>'+str(title.encode('utf8'))+'</title>'
			xml += '<noticekoha>'+str(noticekoha.encode('utf8'))+'</noticekoha>'
			xml += '<category>'+str(classToCategory(bookclass).encode('utf8'))+'</category>'
			xml += '</book>'
		else:
			buff.append(ref);
	
	xml += '</Document>'

	session.close()
	#print xml
	session1.add("bookref.xml", xml)
	#print xml
	xml = xmldom.parseString(xml)
	pretty_xml_as_string = xml.toprettyxml()
	#print pretty_xml_as_string.encode('utf8')
	with open(outFile,"w") as f:
		f.write(pretty_xml_as_string.encode('utf8'));
	session1.close()
except IOError as e:
	print e