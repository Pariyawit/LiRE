# -*- coding: UTF-8 -*-
import Stemmer
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
fr_stem = nltk.stem.snowball.FrenchStemmer(ignore_stopwords=False)
en_stem = nltk.stem.snowball.SnowballStemmer("english")
fr_stem = nltk.stem.snowball.SnowballStemmer("french")

wpt = nltk.WordPunctTokenizer()

words="theoretically"
sentence = words.decode('UTF-8')

tokens = nltk.word_tokenize(sentence)
tokens2 = wpt.tokenize(sentence)

#print tokens
#print tokens2

#for i in range(0,len(tokens2)):
#	print fr_stem.stem(tokens2[i])

#filtered_words = [w for w in word_list if not w in stopwords.words('english')]
#print stopwords.words('english')
#print len(stopwords.words('english'))


words = 'applications'
print words
print 'en_stem : '+en_stem.stem(words)
print 'fr_stem : '+fr_stem.stem(words)
synonyms = set()

synsets = wn.synsets(words)
for synset in synsets:
	synonyms.update(synset.lemma_names)
print '------------------------------------'
for s in synonyms:
	print s