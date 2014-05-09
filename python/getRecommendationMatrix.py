# -*- coding: UTF-8 -*-
import BaseXClient
import Classification
import numpy
import Queue
from array import *

import os
if (os.path.isdir("../database/")):
	path = "../database/"
else:
	path = "database/"

try:
	session = BaseXClient.Session('localhost',1984,'admin','admin')
	session.execute("open historique")
	print session.info()
	# run query on database, get books that have borrowed
	codebarrelecteur="000014880"
	findref = '''for $x in historique/transaction
					where $x/codebarrelecteur="'''+codebarrelecteur+'''"
					return $x/noticekoha/text()'''

	query_ref = session.query(findref)
	
	loan_history = set()
	for typecode, out in query_ref.iter():
		loan_history.add(out)
	print loan_history

	key_noticekoha = dict()
	noticekoha_key = dict()
	with open(path+'book_keyref.txt',"r") as f:
		for line in f:
			tmp = line.split(',')
			tmp[1] = tmp[1].strip()
			#print "--",tmp[0],"--",tmp[1].strip()
			noticekoha_key[tmp[0]] = tmp[1]
			key_noticekoha[tmp[1]] = tmp[0]

	
	print "making relatedMatrix"
	relatedMatrix = numpy.loadtxt(path+"relatedMatrix.txt",delimiter=",",dtype="int32")
	dimension = relatedMatrix.shape
	

	print "making userMatrix"
	user_matrix = [0]*dimension[0]
	#user_matrix = [0]*12000

	
	for book in loan_history:
		#print type(tmp[0])
		if str(book) in noticekoha_key:
			print book,noticekoha_key[str(book)]
			user_matrix[int(noticekoha_key[str(book)])] = 1

	user_matrix = numpy.array(user_matrix)
	resultMatrix = relatedMatrix.dot(user_matrix)

	print "pushing top 10"
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
		resultList.append(tmp[1])

	print resultList
	print i,dimension,resultMatrix.shape
except IOError as e:
	print e