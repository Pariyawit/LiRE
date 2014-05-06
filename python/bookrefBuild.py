# -*- coding: UTF-8 -*-
import BaseXClient
import Classification
import xml.dom.minidom as xmldom
from array import *

import os
if (os.path.isdir("../database/")):
	outFile = "../database/bookref.xml"
else:
	outFile = "database/bookref.xml"

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
			noticekoha = buff[buff.index('#')+1]
			title = buff[buff.index('#')+2]

			# Clean book's class by comparing the 930/a subfields with 995/k subfields ( both 930/a and 995/k can be replicated)
			# because sometimes these fields are correspond to different value, even though it should always be the same
			# if they are different, finding the more suitable one to be used as the book's class
			# for example, sometimes 930/a = D8 ENG/S, while 995/k = D 8.02 SIPP for the same book
			# from the above example, the 995/k subfield is preferred because it is in the right format (having '.')

			for cls in classes:
				try:
					cls = Classification.classtrim(cls)
					if(cls == ValueError): continue
					try:
						k = cls.index('.')
						try:
							k = cls.index('-')
							for j in cls:
								if(j=='-'): j=' '
							bookclass = cls
							break
						except ValueError as ve:
							bookclass = cls
							break
					except ValueError as ve:
						continue
				except ValueError as ve:
					continue
			else:
				print classes
			#print bookclass.encode('utf8')
			
			if(noticekoha == "2109"): print classes

			#print buff
			buff = []
			xml += '<book class="'+str(bookclass.encode('utf8'))+'">'
			xml += '<title>'+str(title.encode('utf8'))+'</title>'
			xml += '<noticekoha>'+str(noticekoha.encode('utf8'))+'</noticekoha>'
			xml += '<category>'+str(Classification.classToCategory(bookclass).encode('utf8'))+'</category>'
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