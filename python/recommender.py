# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
import Classification
import favCategories as favcat
import favKeywords as favkey
import bookselection as bookselect
from array import *
from collections import defaultdict


try:

	# have to receive UserID from PHP
	userID = 10000

	FavCategories = favcat.findfavcategories(userID)

	I = favkey.findfavkeywords(userID)

	booklist = bookselect.bookselection(userID,I)

	for cat in booklist:
		for book in booklist[cat]:
			print cat,book,booklist[cat][book]

except IOError as e:
	print e