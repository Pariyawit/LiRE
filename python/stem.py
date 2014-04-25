# -*- coding: UTF-8 -*-
import Stemmer
import nltk
fr_stem = nltk.stem.snowball.FrenchStemmer(ignore_stopwords=False)

wpt = nltk.WordPunctTokenizer()

stemmer = Stemmer.Stemmer('french')

sentence = """cate cat""".decode('UTF-8')

tokens = nltk.word_tokenize(sentence)
tokens2 = wpt.tokenize(sentence)

print tokens
print tokens2

for i in range(0,len(tokens2)):
	print fr_stem.stem(tokens2[i])