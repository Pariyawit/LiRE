# -*- coding: UTF-8 -*-
import BaseXClient
import numpy
import Queue
from array import *

import os
if (os.path.isdir("../database/")):
	path = "../database/"
else:
	path = "database/"

import sys

#MUST comment all 'print' except the last one for php result
try:
	codebarrelecteur = sys.argv[1]
	#codebarrelecteur="201221459"
except:
	print "UserID not found"
	exit()

try:
	session = BaseXClient.Session('localhost',1984,'admin','admin')
	session.execute("open historique")
	#print session.info()
	# run query on database, get books that have borrowed
	findref = '''for $x in historique/transaction
					where $x/codebarrelecteur="'''+codebarrelecteur+'''"
					return $x/noticekoha/text()'''

	query_ref = session.query(findref)
	
	loan_history = set()
	for typecode, out in query_ref.iter():
		loan_history.add(out)
	#print loan_history

	key_noticekoha = dict()
	noticekoha_key = dict()
	with open(path+'book_keyref.txt',"r") as f:
		for line in f:
			tmp = line.split(',')
			tmp[1] = tmp[1].strip()
			##print "--",tmp[0],"--",tmp[1].strip()
			noticekoha_key[tmp[0]] = tmp[1]
			key_noticekoha[tmp[1]] = tmp[0]

	user_matrix = []
	usecols = []
	for book in loan_history:
		if str(book) in noticekoha_key:
			matrix_ref = int(noticekoha_key[str(book)])
			usecols.append(matrix_ref)
			user_matrix.append(1)

	#get relatedMatrix only column of book that the user have borrowed
	relatedMatrix = numpy.loadtxt(path+"relatedMatrix.txt",delimiter=",",dtype="int32",usecols=usecols)
	dimension = relatedMatrix.shape

	user_matrix = numpy.array(user_matrix)
	resultMatrix = relatedMatrix.dot(user_matrix)
	
	#print "pushing top 10"
	resultQueue=Queue.PriorityQueue(maxsize=10)
	i = 0
	for score in numpy.nditer(resultMatrix):
		str_i = str(i)
		if(key_noticekoha[str_i] not in loan_history):
			item = (score,key_noticekoha[str_i])
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
		#print tmp
		resultList.append(tmp[1])

	#print resultList
	out_string = ""
	for result in resultList:
		out_string += result+","
	print out_string

except IOError as e:
	print e