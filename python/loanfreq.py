# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
from array import *
from collections import defaultdict

import os
if (os.path.isdir("../database/")):
	outFile = "../database/loankeywordfreqtable.xml"
	path = "../database/"
else:
	outFile = "database/loankeywordfreqtable.xml"
	path = "database/"

# A method to transform the date into the season format.
# for example, "2013/05/22" -> "2013/2"
def findSeason(date):
	year = date[0:4]
	if(int(date[5]) != 0):
		month = int(date[5:7])
	else:
		month = int(date[6])
	if(month <= 4): 
		return year + "/1"
	elif(month <= 8):
		return year + "/2"
	else: 
		return year + "/3"

# A method to clean the class received from query and transform to its category.
# for example, "1.66 PENN" -> "01.6"
def classClean(cls):
	try:
		split = cls.index(' ')
	except ValueError as v:
		try:
			split = cls.index('-')
		except ValueError as ve:
			split = len(cls)
	cls = cls[0:split]
	if(cls.index('.') == 1 ):
		cls = "0" + cls
	pointIndex = cls.index('.')
	cls = cls[0:pointIndex+2]
	return cls


try:
	session1 = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	session2 = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	session3 = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	session4 = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	sessionLF = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	sessionLKF = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	session1.execute("open lecteur")
	session2.execute("open historique")
	session3.execute("open bookref")
	session4.execute("open keyword")
	sessionLF.execute("create db loanfreq")
	sessionLKF.execute("create db loankeyfreq")

	#Get all User ID from Old_lecteur_brest
	findUser = '''for $user in /Document/*
				return $user/CARDNUMBER/text()'''
	queryUser = session1.query(findUser)

	#Get the category list
	classlist = []
	f = open(path+'classification.txt','r')
	buff = []
	for buff in f:
		i = buff.index(' ')
		classlist.append(buff[0:i])
	f.close()

	#Prepare the LoanFreqTable
	xmlLF = '<Document>'
	xmlLF += '<Row>'

	#Prepare the LoanKeywordFreqTable
	xmlLKF = '<Document>'
	xmlLKF += '<Row>'

	u = defaultdict(int)
	#Iterate through each user
	for typecode,ref in queryUser.iter():
		#userLF is a dictionary used for counting Loan Frequency (during Season)
		#userLKF is a dictionary used for counting Loan Keyword Frequency
		u[ref] += 1
		userLF = {}
		userLKF = {}

		#initialize both table value to 0, so it can be firstly refrenced by adding value to it directly.
		for c in classlist:
			userLF[c] = defaultdict(int)
			userLKF[c] = defaultdict(int)

		#get all the books borrowed by user with user id = ref
		findBorrowed = '''for $trans in /historique/* 
						where $trans/codebarrelecteur="'''+ref+'''"
						return ($trans/noticekoha/text(),$trans/date/text(),"$")'''
		queryBorrowed = session2.query(findBorrowed)

		buff =[]
		xmlLF += '<user id="'+ref+'">'
		xmlLKF += '<user id="'+ref+'">'

		#Iterate through each book the user borrowed
		for typecode, loan in queryBorrowed.iter():
			if(loan=='$'):
				bookid = buff[0]
				date = buff[1]
				season = findSeason(date)

				findClass = '''for $b in /Document/*
							where $b/text()="'''+bookid+'''"
							return data($b/@class)'''
				queryClass = session3.query(findClass)

				findKeyword = '''for $c in /keywordXML/classification/*
								where $c/@noticekoha="'''+bookid+'''"
								return ($c/keyword/text(),data($c/../@code),'$')'''
				queryKeyword = session4.query(findKeyword)

				#Find keyword of the borrowed book
				tmp = []
				for typecode,key in queryKeyword.iter():
					if(key=='$'):
						cls = tmp[len(tmp)-1]
						cls = classClean(cls)
						for keyword in range(0,len(tmp)-1):
							userLKF[cls][tmp[keyword]] += 1
						tmp = []
					else:
						#print key
						tmp.append(key)

				#Find class of the borrowed book			
				for typecode,cls in queryClass.iter():
					if(cls[0] == 'C' or cls[0] =='D' or cls[0]=='A'):
						continue
					cls = classClean(cls)
					#Count the times of borrowing
					userLF[cls][season] += 1
				buff = []
			else:
				buff.append(loan)

		# Write File (Loan Frequency Table)
		for c in classlist:
			if(len(userLF[c]) == 0):
				continue
			xmlLF += '<class category="'+c+'">'
			for j in userLF[c]:
				xmlLF += '<count season="'+str(j)+'">'+str(userLF[c][j])+'</count>'
			xmlLF += '</class>' 

		# Write File (Loan Keyword Frequency Table)
		for c in classlist:
			if(len(userLKF[c]) == 0):
				continue
			xmlLKF += '<class category="'+c+'">'
			for j in userLKF[c]:
				xmlLKF += '<keyword count="'+str(userLKF[c][j])+'">'+str(j.encode('utf8')).decode('utf8')+'</keyword>'
			xmlLKF += '</class>'

		xmlLF += '</user>'
		xmlLKF += '</user>'

	xmlLF += '</Row>'
	xmlLF += '</Document>'
	xmlLKF += '</Row>'
	xmlLKF += '</Document>'

	for e in u:
		if(u[e]>1): print e, u[e]

	session1.close()
	session2.close()
	session3.close()
	session4.close()

	#print xml LF
	sessionLF.add('loanfreqtable.xml',xmlLF)
	xmlLF = xmldom.parseString(xmlLF)
	pretty_xml_as_string = xmlLF.toprettyxml()
	
	with open(path+'loanfreqtable.xml','w') as f:
		f.write(pretty_xml_as_string.encode('utf8'))

	sessionLF.close()

	#print xml LKF
	sessionLKF.add('loankeywordfreqtable.xml',xmlLKF)
	xmlLKF = xmldom.parseString(xmlLKF.encode('utf8'))
	pretty_xml_as_string = xmlLKF.toprettyxml()
	
	with open(outFile,'w') as f:
		f.write(pretty_xml_as_string.encode('utf8'))

	sessionLKF.close()

except IOError as e:
	# print exception
	print e

