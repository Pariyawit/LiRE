# -*- coding: UTF-8 -*-
import BaseXClient
import nltk
import string
from xml.etree import ElementTree
import xml.dom.minidom as xmldom

fr_stem = nltk.stem.snowball.FrenchStemmer(ignore_stopwords=False)
wpt = nltk.WordPunctTokenizer()

'''
à
après
avant
avec
chez
contre
dans
de
depuis
derrière
devant
durant
en
dehors
face
entre
envers
environ
hors
jusque
loin
malgré
par
parmi
pendant
pour
près
quant
sans
selon
sous
suivant
sur
vers

car
donc
ensuite
et
mais
or
ou
puis
'''

commonwords = ['de','et','and','la','le','l','d','of','à','du','en','pour','in','for','']

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
				return ($record/marcxml:subfield[@code="k"]/text(),
						$record/../marcxml:controlfield[@tag="001"]/text(),
						$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),
						$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="e"]/text(),
						"$")'''

	query_ref = session.query(findref)
	buff = []
	#find number of borrows each book with distinct user by using set
	#buf[0] book's classification
	#buf[1] book's ref (noticekoha)
	#buf[2] book's name
	#buf[3..n] book's details

	keywordXML = ElementTree.Element("keywordXML")
	classifications = dict()
	books = dict()
	keywords = dict()
	#get each book
	for typecode, output in query_ref.iter():
		if(output=='$'):
			tmp = buff[0].split(".");
			ref = buff[1]
			if tmp[0][0].isdigit():
				code = tmp[0]+'.'+tmp[1][0]
				if code not in classifications :
					classifications[code] = dict()

				if ref not in classifications[code] :
					classifications[code][ref] = set()

				for i in range(2,len(buff)):
					tokens = wpt.tokenize(buff[i])
					for token in tokens:
						if (token not in string.punctuation) and (len(token)>1):
							token_stem = fr_stem.stem(token)
							classifications[code][ref].add(token_stem)
							if token_stem not in keywords:
								keywords[token_stem] = 0
							keywords[token_stem] = keywords[token_stem]+1
			buff = []
			continue
		buff.append(output)

	#print classifications
	f = open('keywordcount.txt','w')
	for w in sorted(keywords, key=keywords.get, reverse=True):
		#print w.encode('UTF-8'),',',keywords[w]
		s = w.encode('UTF-8')+','+str(keywords[w])+'\n'
		f.write(s)

except IOError as e:
	# print exception
	print e