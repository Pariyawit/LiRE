# -*- coding: UTF-8 -*-
import BaseXClient
import nltk
import string

fr_stem = nltk.stem.snowball.FrenchStemmer(ignore_stopwords=False)
wpt = nltk.WordPunctTokenizer()

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
				and $record/../marcxml:controlfield[@tag="001"]="27980"
				return ($record/marcxml:subfield[@code="k"]/text(),
						$record/../marcxml:controlfield[@tag="001"]/text(),
						$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="a"]/text(),
						$record/../marcxml:datafield[@tag="200"]/marcxml:subfield[@code="e"]/text(),
						"$")'''

	query_ref = session.query(findref)
	buff = []

	loan = dict()

	#find number of borrows each book with distinct user by using set
	#buf[0] book's classification
	#buf[1] book's ref (noticekoha)
	#buf[2] book's name
	#buf[3..n] book's details
	for typecode, ref in query_ref.iter():
		if(ref=='$'):
			#print buff
			tmp = buff[0].split(".");
			ref = buff[1]
			book_name = buff[2]
			stems = []
			for i in range(2,len(buff)):
				print buff[i]
				tokens = wpt.tokenize(buff[i])
				for token in tokens:
					if token not in string.punctuation:
						stems.append(fr_stem.stem(token))
			print stems
			print '-------'

			buff = []
			continue

		buff.append(ref)

except IOError as e:
	# print exception
	print e