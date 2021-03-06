# -*- coding: UTF-8 -*-
#this code make keywordXML_syn.xml which extract keyword from each book
#very time consuming, run more that an hour
import BaseXClient
import nltk
import string
import Classification
#nltk.corpus stopwords download required
from nltk.corpus import stopwords
#nltk.corpus wordnet download required
from nltk.corpus import wordnet as wn
from xml.etree import ElementTree
import xml.dom.minidom as xmldom

import os
if (os.path.isdir("../database/")):
	path = "../database/"
else:
	path = "database/"

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

def isValid(token):
	for t in token:
		if t in string.punctuation:
			return False
	return True

#input is unstemmed word because nltk provide good englisth dictionary
def en_synonyms(word):
	synonyms = set()
	synsets = wn.synsets(word)
	for synset in synsets:
		synonyms.update(synset.lemma_names)
	synonyms.add(word)
	#print word,len(synonyms)
	return synonyms



#another method is used for french word becuase ntlk doesn't have french dictionary
#open database for french wordnet
session_wordnet = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
session_wordnet.execute("open wordnetfrench")
print session_wordnet.info()
#input is stemmed word and use starts_with to find the synonym
def fr_synonyms(stemmed_word):
	try:
		synonyms = set()
		synonyms.add(stemmed_word)
		if(len(stemmed_word)<5):
			return synonyms
		find_syn = '''for $synset in /WN/SYNSET/SYNONYM/LITERAL
						where starts-with($synset,"'''+stemmed_word+'''")
						let $nl := "&#10;"
						for $s in $synset/../../SYNONYM/LITERAL
						where $s/text() != "_EMPTY_"
						return ($s/text())'''
		synsets = session_wordnet.query(find_syn)
		for typecode, output in synsets.iter():
			if(' ' not in output):
				synonyms.add(output)
		#print stemmed_word.encode('UTF-8'),len(synonyms)
		return synonyms

	except IOError as e:
		print '!!!!!!error!!!!!!'
		#print e

try:
	#create session
	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	#open database an run query to get all books within 'BSTB'
	session.execute("open extraction")
	print session.info()
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
	#buf[0] book's languange (fre,eng,ger,ita,spa)
	#buf[1] book's classification
	#buf[2] book's ref (noticekoha)
	#buf[3] book's name
	#buf[4..n] book's details

	keywordXML = ElementTree.Element("keywordXML")
	books = dict()
	#get each book
	book_count = 1
	for typecode, output in query_ref.iter():
		if(output=='$'):
			print ''
			print '['+str(book_count)+'/10388]'
			book_count = book_count+1
			print buff
			#print '---------------------------'
			# sign '#' means end of language section of the book
			classes = buff[0:buff.index('#')]
			bookclass=""
			#print classes
			for cls in classes:
				try:
					cls = Classification.classtrim(cls)
					if(cls == ValueError): continue
					try:
						k = cls.index('.')
						if(k>2): continue
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

			code = str(Classification.classToCategory(bookclass).encode('utf8'))
			if code not in books :
				books[code] = dict()

			#keyword for a book of 'code'&'ref', set() for non-duplicate
			ref = buff[lang_offset+1]
			if ref not in books[code] :
				books[code][ref] = set()
			print code,ref
			for i in range(lang_offset+2,len(buff)):
				tokens = wpt.tokenize(buff[i])
				#remove stopwords before stem
				filtered_tokens = [w for w in tokens if not w in stopwords_list_encoded]
				for token in filtered_tokens:
					#use only token that doesn't have punctuation

					if (token not in string.punctuation) and (len(token)>1) and not token.isdigit():
						#different stem function for different lang
						#if both fre and eng appear in lang, use both stem function becuase the book's title/description language is unknown
						if("fre" in lang):
							synsets = fr_synonyms(fr_stem.stem(token))
							for syn in synsets:
								if(isValid(syn)):
									books[code][ref].add(fr_stem.stem(syn))
						if("eng" in lang):
							synsets = en_synonyms(token)
							for syn in synsets:
								if(isValid(syn)):
									books[code][ref].add(en_stem.stem(syn))
						elif("fre" not in lang):
							print '------NOT IN BOTH'
							synsets = en_synonyms(token)
							for syn in synsets:
								if(isValid(syn)):
									books[code][ref].add(en_stem.stem(syn))
			buff = []
			continue
		buff.append(output)

	print 'pushing xml...'
	#put all result to xml format
	xml = "<keywordXML>"
	for codes in books.iterkeys() :
		xml += '<category code="'+codes+'">'
		for ref in books[codes].iterkeys() :
			xml += '<book noticekoha="'+ref+'">'
			for token in books[codes][ref] :
				xml += '<keyword>'+token+'</keyword>'
			xml += '</book>'
		xml += '</category>'
	xml += '</keywordXML>'

	session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	# create empty database
	session.execute("create db keywordXML")
	session.add("keywordXML.xml", xml)
	session.close()

	with open(path+"keywordXML.xml","w") as f:
		f.write(xml.encode('utf8'));

	# -----------!!!-------------MEMORY ERROR after this...-----------!!!-------------
	xml = xmldom.parse(path+"keywordXML.xml")
	pretty_xml_as_string = xml.toprettyxml()
	#print pretty_xml_as_string
	with open(path+"keywordXML.xml","w") as f:
		f.write(pretty_xml_as_string.encode('utf8'));

	#print books

except IOError as e:
	# print exception
	print e