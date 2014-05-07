# -*- coding: UTF-8 -*-
import BaseXClient
import nltk
import string
import Classification
from nltk.corpus import stopwords
from xml.etree import ElementTree
import xml.dom.minidom as xmldom
import xml

import os
if (os.path.isdir("../database/")):
	outFile = "../database/keywordXML.xml"
else:
	outFile = "database/keywordXML.xml"

def isValid(token):
	for t in token:
		if t in string.punctuation:
			return False
	return True

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
	session.execute("open extraction")
	print session.info()
	
	# run query on database, get all books
	findref = '''declare namespace marcxml = "http://www.loc.gov/MARC21/slim";
					for $record in //marcxml:record
					where $record/marcxml:datafield[@tag="995"]/marcxml:subfield[@code="e"]="BSTB"
					and $record/marcxml:datafield[@tag="995"]/marcxml:subfield[@code="r"]="OUV"
					and $record/marcxml:datafield[@tag="930"]/marcxml:subfield[@code="a"]/text()[contains(.,".")]
					return (distinct-values($record/marcxml:datafield[@tag="995"]/marcxml:subfield[@code="k"]/text()),
					distinct-values($record/marcxml:datafield[@tag="930"]/marcxml:subfield[@code="a"]/text()),"#",
					$record/marcxml:datafield[@tag="101"]/marcxml:subfield[@code="a"]/text(),"##",
					$record/marcxml:controlfield[@tag="001"]/text(),
					$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),
					$record/marcxml:datafield[@tag="200"]/marcxml:subfield[@code="e"]/text(),
					"$")'''

	query_ref = session.query(findref)
	buff = []
	#find number of borrows each book with distinct user by using set
	#buf[0..#] book's classification
	#buf[#..#] book's languange (fre,eng,ger,ita,spa)
	#buf[#+1] book's ref (noticekoha)
	#buf[#+2] book's name
	#buf[#+3..n] book's details

	keywordXML = ElementTree.Element("keywordXML")
	classifications = dict()
	books = dict()
	#get each book
	for typecode, output in query_ref.iter():
		if(output=='$'):
			#print buff
			classes = buff[0:buff.index('#')]
			bookclass=""
			#print classes
			for cls in classes:
				try:
					cls = Classification.classtrim(cls)
					if(cls == ValueError): continue
					try:
						k = cls.index('.')
						try:
							k = cls.index('-')
							for j in cls:
								if(j=='-'):
									j = ' '
							bookclass = cls
							break
						except ValueError as ve:
							bookclass = cls
							break
					except ValueError as ve:
						continue
				except ValueError as ve:
					continue

			#print bookclass
			lang_offset = buff.index("##")
			lang = []
			for i in range(0,lang_offset):
				lang.append(buff[i])
			#if(lang_offset>1):
			#	print buff
			ref = buff[lang_offset+1]
			code = str(Classification.classToCategory(bookclass).encode('utf8'))
			if code not in classifications :
				classifications[code] = dict()

			#keyword for a book of 'code'&'ref', set() for non-duplicate
			if ref not in classifications[code] :
				classifications[code][ref] = set()

			for i in range(lang_offset+2,len(buff)):
				tokens = wpt.tokenize(buff[i])
				#remove stopwords before stem
				filtered_tokens = [w for w in tokens if not w in stopwords_list_encoded]
				for token in filtered_tokens:
					if (len(token)>1) and not token.isdigit() and isValid(token):
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

	xmlstr = ElementTree.tostring(tree.getroot(), encoding='utf8', method='xml')
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("create db keywordXML")
	session.add("keywordXML.xml", xmlstr)
	session.close()

except IOError as e:
	# print exception
	print e