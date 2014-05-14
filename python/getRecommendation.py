# -*- coding: UTF-8 -*-
#provide recommend book from matrix multipication
import BaseXClient
from Classification import getNoticekohaInCategory
import numpy
import Queue
from season_score import cal_season_score
#from array import *

import os
if (os.path.isdir("../database/")):
	path = "../database/"
else:
	path = "database/"

import sys

try:
	codebarrelecteur = sys.argv[1]
	if len(sys.argv) == 3:
		category = sys.argv[2]
		category_books = getNoticekohaInCategory(category)
	#codebarrelecteur = "201321805"
except IOError as e:
	print e
	sys.exit(0)

try:
	session = BaseXClient.Session('localhost',1984,'admin','admin')
	session.execute("open historique")
	# run query on database, get books that have borrowed
	findref = '''for $x in historique/transaction
					where $x/codebarrelecteur="'''+codebarrelecteur+'''"
					return concat($x/noticekoha/text()," ",$x/date/text())'''

	query_ref = session.query(findref)
	
	loan_history = set()
	loan_date = dict()
	for typecode, out in query_ref.iter():
		buff = out.split(" ")
		loan_history.add(buff[0])
		if buff[0] not in loan_date:
			loan_date[buff[0]] = ""
		loan_date[buff[0]] = buff[1]

	key_noticekoha = dict()
	noticekoha_key = dict()
	with open(path+'book_keyref.txt',"r") as f:
		for line in f:
			tmp = line.split(',')
			tmp[1] = tmp[1].strip()
			noticekoha_key[tmp[0]] = tmp[1]
			key_noticekoha[tmp[1]] = tmp[0]

	user_matrix = []
	usecols = []
	for noticekoha in loan_history:
		if str(noticekoha) in noticekoha_key:
			matrix_ref = int(noticekoha_key[str(noticekoha)])
			usecols.append(matrix_ref)
			score = cal_season_score(loan_date[str(noticekoha)])
			user_matrix.append(score)

	#get relatedMatrix only column of book that the user have borrowed
	relatedMatrix = numpy.loadtxt(path+"relatedMatrix.txt",delimiter=",",usecols=usecols)
	dimension = relatedMatrix.shape

	user_matrix = numpy.array(user_matrix)
	resultMatrix = relatedMatrix.dot(user_matrix)
	
	resultQueue=Queue.PriorityQueue(maxsize=10)
	i = 0
	for score in numpy.nditer(resultMatrix):
		str_i = str(i)
		if(key_noticekoha[str_i] not in loan_history):
			if (len(sys.argv) == 3 and key_noticekoha[str_i] not in category_books):
				i=i+1
				continue
			item = (score,key_noticekoha[str_i])
			#print item
			try:
				resultQueue.put_nowait(item)
			except:
				tmp = resultQueue.get()
				if tmp[0] > item[0]:
					resultQueue.put_nowait(tmp)
				else:
					resultQueue.put_nowait(item)
		i=i+1

	resultList = []
	while (resultQueue.qsize() > 0):
		tmp = resultQueue.get()
		resultList.append(tmp[1])

	resultList.reverse()

	out_string = ""
	for result in resultList:
		out_string += result+","
	print out_string

except IOError as e:
	print e
	print "ERROR"
	sys.exit(0)