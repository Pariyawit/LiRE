# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
from array import *
from collections import defaultdict

def subcatToCat(category):
	try:
		buff = category.index('.')
		buff = category.split('.')
		return buff[0]
	except ValueError as v:
		return -1

try:
	session1 = BaseXClient.Session('localhost',1984,'admin','admin')
	session1.execute('open loanfreq')
	print session1.info()
	userID = 10023

	#Prepare the dictionary F (F stands for Favourite Categories)
	F = {}
	F = defaultdict(float)

	#Declare an 2-dim dictionary used to store amount of time the user borrows a level-1 category's book during season
	parentcatcount = {}

	#Get a list of categories from file
	categorylist = []
	f = open('../database/classification.txt','r')
	for buff in f:
		i = buff.index(' ')
		catcode = buff[0:i]
		if(subcatToCat(catcode) == -1): #This mean if it is not a subcategory
			parentcatcount[catcode] = defaultdict(int)
		categorylist.append(catcode)
	f.close()

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
	for typecode,ref in query_ref.iter():
		if(ref=='$'):
			category = buff[0]
			parentcategory = subcatToCat(category)
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
				totalcount += parentcatcount[cat][k]
			F[cat] += float(totalcount)*(float(1)/2)**float(seasonscaling[k])
			
	#for cat in F:
	#	print cat,'---',F[cat]

	session1.close()
except IOError as e:
	print e