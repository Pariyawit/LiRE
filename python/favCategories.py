# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
import Classification
import Tree
from array import *
from collections import defaultdict

try:
	session1 = BaseXClient.Session('localhost',1984,'admin','admin')
	session1.execute('open loanfreq')
	print session1.info()
	userID = 1385

	#Prepare the dictionary F (F stands for Favourite Categories)
	F = defaultdict(float)

	#Get a list of categories 
	categorylist = Classification.getclassificationrule()

	#Declare an 2-dim dictionary used to store amount of time the user borrows a level-1 category's book during season
	parentcatcount = {}
	for cat in categorylist:
		parentcatcount[cat] = defaultdict(int)

	#Get the season scaling array
	seasonscaling = {}
	f = open("../database/season.txt","r")
	for buff in f:
		if(buff[0]=='#'):
			continue
		elif(buff[0]=='['):
			continue
		else:
			buff = buff.split('-')
			seasonscaling[buff[0]]=int(buff[1])
	f.close()

	#Set the XPATH query for search the requested user with user id in loanfreqtable.xml
	findref = '''for $user in //Document/Row/user/*
				where $user/../@id="'''+str(userID)+'''"
				return (data($user/@category),data($user/count/@season),$user/count/text(),'$')'''

	#XPATH query execution
	query_ref = session1.query(findref)

	#Get the results and do the computation for subcategories
	buff = []
	cattree = Tree.Categorytree()
	for typecode,ref in query_ref.iter():
		if(ref=='$'):
			category = buff[0]
			parentcategory = cattree.getParent(category)
			season = buff[1:(len(buff)/2)+1]
			count = buff[(len(buff)/2)+1:len(buff)]
			#Store the computed value into dictionary F
			for i in range(0,len(count)):
				F[category] += float(count[i])*(float(1)/2)**float(seasonscaling[season[i]])
				parentcatcount[parentcategory][season[i]] += int(count[i])
				#print i, category, season[i], F[category]
			buff = []
			season = []
			count = []
		else:
			buff.append(ref)

	#do the computation for level-1 categories
	for cat in parentcatcount:
		if(parentcatcount[cat]!={}):
			totalcount = 0
			for k in parentcatcount[cat]:
				F[cat] += float(parentcatcount[cat][k])*(float(1)/2)**float(seasonscaling[k])
			
	for cat in categorylist:
		print cat," - ",F[cat]

	session1.close()
except IOError as e:
	print e