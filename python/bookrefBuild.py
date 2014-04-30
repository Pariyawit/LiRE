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
try:
	session = BaseXClient.Session('localhost',1984,'admin','admin')
	session1 = BaseXClient.Session('localhost',1984,'admin','admin')
	session.execute("open extraction")
	session1.execute("create db bookref")
	print session.info()
	# run query on database, get all books
	findref = '''declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
				for $record in //marcxml:record/*
				where $record/marcxml:subfield[@code="e"]="BSTB"
				and contains($record/marcxml:subfield[@code="k"]/text(),".")
				and $record/marcxml:subfield[@code="r"]="OUV"
				return ($record/marcxml:subfield[@code="k"]/text(),
						$record/../marcxml:controlfield[@tag="001"]/text(),
						"$")'''

	query_ref = session.query(findref)
	buff = []

	xml = '<Document>'
	for typecode, ref in query_ref.iter():
		if(ref=='$'):
			classes = buff[0]
			noticekoha = buff[1]
			xml += '<book class="'+str(classes.encode('utf8'))+'">'+str(noticekoha)+'</book>'
			buff = []
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