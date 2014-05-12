# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
import favCategories as favcat
import favKeywords as favkey
import bookselection as bookselect
from array import *
from collections import defaultdict
import operator

try:

	# have to receive UserID from PHP
	userID = 201221045

	FavCategories = favcat.findfavcategories(userID)

	I = favkey.findfavkeywords(userID)

	booklist = bookselect.bookselection(userID,I)

	# Sort the recommended book list, so we can select just the top most x books to recommend.
	slist = []
	for cat in booklist:
		slist = list(sorted(booklist[cat], key=booklist[cat].__getitem__, reverse=True))
		cnt = 0
		for book in slist:
			if(cnt==5): break
			cnt += 1
			print cat,book,booklist[cat][book]

except IOError as e:
	print e