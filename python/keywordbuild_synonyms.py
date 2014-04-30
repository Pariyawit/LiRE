# -*- coding: UTF-8 -*-
import BaseXClient
import nltk
import string
#nltk.corpus stopwords download required
from nltk.corpus import stopwords
#nltk.corpus wordnet download required
from nltk.corpus import wordnet as wn
from xml.etree import ElementTree
import xml.dom.minidom as xmldom


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

#input is unstemmed word because nltk provide good dictionary
def en_synonyms(word):
	synonyms = set()
	synsets = wn.synsets(word)
	for synset in synsets:
		synonyms.update(synset.lemma_names)
	synonyms.add(word)
	#print word,len(synonyms)
	return synonyms

#open database
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
	#open database
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
	book_count = 0
	for typecode, output in query_ref.iter():
		if(output=='$'):
			print ''
			print '['+str(book_count)+'/19628]'
			book_count = book_count+1
			print buff
			#print '---------------------------'
			# sign '#' means end of language section of the book
			lang_offset = buff.index("#")
			lang = []
			for i in range(0,lang_offset):
				lang.append(buff[i])
			tmp = buff[lang_offset+1].split(".")
			ref = buff[lang_offset+2]
			if tmp[0][0].isdigit():
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
							#if both fre and eng appear in lang, use both stem function becuase the book's title/description lanuage is unknown
							if("fre" in lang):
								synsets = fr_synonyms(fr_stem.stem(token))
								for syn in synsets:
									classifications[code][ref].add(fr_stem.stem(syn))
							if("eng" in lang):
								synsets = en_synonyms(token)
								for syn in synsets:
									classifications[code][ref].add(en_stem.stem(syn))
							elif("fre" not in lang):
								print '------NOT IN BOTH'
								synsets = en_synonyms(token)
								for syn in synsets:
									classifications[code][ref].add(en_stem.stem(syn))
			buff = []
			continue
		buff.append(output)

	print 'pushing xml...'
	#put all result to xml format
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


	print 'making xml file...'
	tree = ElementTree.ElementTree(keywordXML)
	tree.write("../database/keywordXML_syn.xml",encoding="UTF-8", xml_declaration=True)

	xml = xmldom.parse("../database/keywordXML_syn.xml")
	pretty_xml_as_string = xml.toprettyxml()
	#print pretty_xml_as_string
	with open("../database/keywordXML_syn.xml","w") as f:
		f.write(pretty_xml_as_string.encode('utf8'));

	#print classifications

except IOError as e:
	# print exception
	print e