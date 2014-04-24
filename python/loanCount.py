# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
from array import *
classification = ["0.","0.1","0.2","0.3","0.4","1.","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.","2.1","2.2","2.3","2.4","2.5","2.6","2.7","3.","3.1","3.2","3.3","3.4","3.5","3.6","3.7","3.8","3.9","4.","4.1","4.2","4.3","4.4","4.5","4.6","5.","5.1","5.2","5.3","5.4","5.5","5.6","6.","6.1","6.2","6.3","6.4","6.5","6.6","6.7","6.8","6.9","7.","7.1","7.2","7.3","7.4","8.","8.1","8.2","8.3","8.4","8.5","8.6","8.7","9.","9.1","9.2","9.3","9.4","9.5","10.","10.1","10.2","10.3","10.4","10.5","10.6","10.7","11.","11.1","11.2","11.3","11.4","11.5","11.6","11.7","12.","12.1","12.2","12.3","12.4","12.5","12.6","12.7"]
try:

	#create session
	session1 = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	session2 = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session1.execute("open extraction")
	session2.execute("open historique")
	print session1.info()
	print session2.info()
	# run query on database, get all books
	findref = '''declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
				for $record in //marcxml:record/*
				where $record/marcxml:subfield[@code="e"]="BSTB"
				and contains($record/marcxml:subfield[@code="k"]/text(),".")
				return ($record/marcxml:subfield[@code="k"]/text(),
						$record/../marcxml:controlfield[@tag="001"]/text(),
						$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),
						"$")'''

	query_ref = session1.query(findref)
	buff = []


	loan = dict()

	#find number of borrows each book with distinct user by using set
	#buf[0] book's classification
	#buf[1] book's ref (noticekoha)
	#buf[2] book's name
	xml = "<Document>"
	for typecode, ref in query_ref.iter():
		if(ref=='$'):
			#print buff
			tmp = buff[0].split(".");
			ref = buff[1]
			book_name = buff[2]

			#xml += "<book class='"+str(tmp)+"'>"+str(ref)+"</book>"
			xml += '<book class="'+str(buff[0].encode('utf8'))+'">'+str(ref)+'</book>'

			find_loan_num = 'for $row in /historique/* where $row/noticekoha="'+ref+'" return $row/lecteurkoha/text()'
			query_loan = session2.query(find_loan_num)
			count_set = set()
			for t,loan_num in query_loan.iter():
				count_set.add(loan_num)

			main_class = str(tmp[0])

			if main_class not in loan:
				loan[main_class] = set()

			#in format (sub_class,book_ref,loan_num,book_name)
			loan[main_class].add((str(tmp[1][0]),str(buff[1]),len(count_set),book_name))
			#print tmp[0],loan[tmp[0]]
			#print "DONE"
			buff = []
			continue

		buff.append(ref);
	xml += "</Document>"

	session1.add("bookref.xml", xml)

	xml = xmldom.parseString(xml)
	pretty_xml_as_string = xml.toprettyxml()

	with open("../bookref.xml","w") as f:
		f.write(pretty_xml_as_string.encode('utf8'));
	# drop database
	#session.execute("drop db database")
	# close session
	session1.close()
	session2.close()

	#print loan['0']
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	session.execute('create db toploan')
	print session.info()

	xml = '<Document>'
	#find 5 most borrow in each classification
	i =0
	for classification in range(0,13):
		#print '---------------'+str(classification)+'---------------'
		main_class = str(classification)
		loan_list = sorted(loan[main_class],key = lambda x: (x[2]), reverse=True)
		i=0
		xml += '<class code="'+main_class+'.">'
		for l in loan_list :
			#print l[0],l[1],l[2],l[3].encode('utf8')
			xml += '<loan loanNum="'+str(l[2])+'" noticekoha="'+str(l[1])+'">'+l[3].encode('utf8')+'</loan>'
			i = i+1
			if i >= 5:
				break
		xml+= '</class>'

	#find 5 most borrow in each sub classification
	for classification in range(0,13):
		main_class = str(classification)
		#sorted by subclasssification and loanNum
		loan_list = sorted(loan[main_class],key = lambda x: (x[0], x[2]), reverse=True)
		top5_count=0
		mem = -1

		#l[0] = sub classification
		#l[1] = noticekoha//bookref
		#l[2] = loanNum
		#l[3] = book_name
		for l in loan_list:
			if mem != l[0] :
				if mem != -1 :
					xml+= '</class>'
				xml += '<class code="'+main_class+'.'+l[0]+'">'
				top5_count = 0
				mem = l[0]
			if(top5_count<5 and l[2]>0):
				xml += '<loan loanNum="'+str(l[2])+'" noticekoha="'+str(l[1])+'">'+l[3].encode('utf8')+'</loan>'
				#print l[0],l[1],l[2],l[3].encode('utf8')
				
			top5_count += 1
		xml+= '</class>'
	xml+= '</Document>'
	#print xml
	session.add("toploan.xml", xml)

	#print xml
	xml = xmldom.parseString(xml)
	pretty_xml_as_string = xml.toprettyxml()
	#print pretty_xml_as_string.encode('utf8')
	with open("../toploan.xml","w") as f:
		f.write(pretty_xml_as_string.encode('utf8'));

except IOError as e:
	# print exception
	print e
