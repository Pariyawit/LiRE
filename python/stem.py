# -*- coding: UTF-8 -*-
import Stemmer
import nltk
from nltk.corpus import stopwords
fr_stem = nltk.stem.snowball.FrenchStemmer(ignore_stopwords=False)

wpt = nltk.WordPunctTokenizer()

stemmer = Stemmer.Stemmer('french')

sentence = """Lea Led Lee Leg Lei Lek Les Let Leu Lev Lex Ley Lez""".decode('UTF-8')

tokens = nltk.word_tokenize(sentence)
tokens2 = wpt.tokenize(sentence)

print tokens
print tokens2

for i in range(0,len(tokens2)):
	print fr_stem.stem(tokens2[i])

#filtered_words = [w for w in word_list if not w in stopwords.words('english')]
#print stopwords.words('english')
#print len(stopwords.words('english'))
print stopwords.words('french')
print len(stopwords.words('french'))
if 'que' in stopwords.words('french'):
	print 'yes'
else:
	print 'no'