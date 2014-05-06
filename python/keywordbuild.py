# -*- coding: UTF-8 -*-
import BaseXClient
import nltk
import string
from nltk.corpus import stopwords
from xml.etree import ElementTree
import xml.dom.minidom as xmldom

import os
if (os.path.isdir("../database/")):
	outFile = "../database/keywordXML.xml"
else:
	outFile = "database/keywordXML.xml"

en_stem = nltk.stem.snowball.SnowballStemmer("english")
fr_stem = nltk.stem.snowball.SnowballStemmer("french")

wpt = nltk.WordPunctTokenizer()

stopwords_list = []
stopwords_list.extend(stopwords.words('english'))
stopwords_list.extend(stopwords.words('french'))
#ntlk doesn't have 'les' in stopwords... why?
stopwords_list.append('les')
stopwords_list_encoded = []

for word in stopwords_list:
	stopwords_list_encoded.append(word.decode('UTF-8'))

try:
	#create session
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("open extraction")
	print session.info()
	
	# run query on database, get all books
	findref = '''declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
				for $record in //marcxml:record/*
				where $record/marcxml:subfield[@code="e"]="BSTB"
				and contains($record/marcxml:subfield[@code="k"]/text(),".")
				return ($record/../marcxml:datafield[@tag="101"]/marcxml:subfield[@code="a"]/text(),"#",
						$record/marcxml:subfield[@code="k"]/text(),
						$record/../marcxml:controlfield[@tag="001"]/text(),
						$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),
						$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="e"]/text(),
						"$")'''

	query_ref = session.query(findref)
	buff = []
	#find number of borrows each book with distinct user by using set
	#buf[0] book's languange (fre,eng,ger,ita,spa)
	#buf[1] book's classification
	#buf[2] book's ref (noticekoha)
	#buf[3] book's name
	#buf[4..n] book's details

	keywordXML = ElementTree.Element("keywordXML")
	classifications = dict()
	books = dict()
	#get each book
	for typecode, output in query_ref.iter():
		if(output=='$'):
			lang_offset = buff.index("#")
			lang = []
			for i in range(0,lang_offset):
				lang.append(buff[i])
			if(lang_offset>1):
				print buff
			tmp = buff[lang_offset+1].split(".")
			ref = buff[lang_offset+2]
			if tmp[0][0].isdigit():
				if(len(tmp[0])==1):
					tmp[0] = '0'+tmp[0]
				code = tmp[0]+'.'+tmp[1][0]
				if code not in classifications :
					classifications[code] = dict()

				#keyword for a book of 'code'&'ref', set() for non-duplicate
				if ref not in classifications[code] :
					classifications[code][ref] = set()

				for i in range(lang_offset+3,len(buff)):
					tokens = wpt.tokenize(buff[i])
					#remove stopwords before stem
					filtered_tokens = [w for w in tokens if not w in stopwords_list_encoded]
					for token in filtered_tokens:
						if (token not in string.punctuation) and (len(token)>1) and not token.isdigit():
							#different stem function for different lang
							if("fre" in lang):
								classifications[code][ref].add(fr_stem.stem(token))
							if("eng" in lang):
								classifications[code][ref].add(en_stem.stem(token))
			buff = []
			continue
		buff.append(output)

	keywordXML = ElementTree.Element("keywordXML")
	for codes in classifications.iterkeys() :
		classification = ElementTree.SubElement(keywordXML,"classification")
		classification.set('code',codes)
		for ref in classifications[codes].iterkeys() :
			book = ElementTree.SubElement(classification,"book")
			book.set('noticekoha',ref)
			for token in classifications[codes][ref] :
				keyword = ElementTree.SubElement(book,"keyword")
				keyword.text = token



	tree = ElementTree.ElementTree(keywordXML)
	tree.write(outFile,encoding="UTF-8", xml_declaration=True)

	xml = xmldom.parse(outFile)
	pretty_xml_as_string = xml.toprettyxml()
	#print pretty_xml_as_string
	with open(outFile,"w") as f:
		f.write(pretty_xml_as_string.encode('utf8'));

	#print classifications

except IOError as e:
	# print exception
	print e