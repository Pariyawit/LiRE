# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
from array import *
from collections import defaultdict


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
		split = cls.index('-')
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
	session1.execute("open lecteur")
	session2.execute("open historique")
	session3.execute("open bookref")

	#Get all User ID from Old_lecteur_brest
	findUser = '''/Document/Row/CARDNUMBER/text()'''
	queryUser = session1.query(findUser)

	#Get the classification rule
	classlist = []
	f = open('../classification.txt','r')
	buff = []
	for buff in f:
		i = buff.index(' ')
		classlist.append(buff[0:i])
	f.close()

	#Prepare the LoanFreqTable
	xml = '<Document>'
	xml += '<Row>'

	#Iterate through each user
	for typecode,ref in queryUser.iter():
		user = {}
		for c in classlist:
			user[c] = defaultdict(int)

		findBorrowed = '''for $trans in /historique/* 
						where $trans/codebarrelecteur="'''+ref+'''"
						return ($trans/noticekoha/text(),$trans/date/text(),"$")'''
		queryBorrowed = session2.query(findBorrowed)

		buff =[]
		xml += '<user id="'+ref+'">'

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

				#Find class of the borrowed book			
				for typecode,cls in queryClass.iter():
					if(cls[0] == 'C' or cls[0] =='D' or cls[0]=='A'):
						continue
					cls = classClean(cls)
					#Count the times of borrowing
					user[cls][season] += 1
				buff = []
			else:
				buff.append(loan)

		# write file
		for c in classlist:
			if(len(user[c]) == 0):
				continue
			xml += '<class category="'+c+'">'
			for j in user[c]:
				xml += '<count season="'+str(j)+'">'+str(user[c][j])+'</count>'
			xml += '</class>' 

		xml += '</user>'

	xml += '</Row>'
	xml += '</Document>'

	session2.close()
	session3.close()

	#print xml
	session1.add('loanfreqtable.xml',xml)
	xml = xmldom.parseString(xml)
	pretty_xml_as_string = xml.toprettyxml()
	
	with open('../loanfreqtable.xml','w') as f:
		f.write(pretty_xml_as_string.encode('utf8'))

	session1.close()
except IOError as e:
	# print exception
	print e

