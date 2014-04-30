import BaseXClient
import xml.dom.minidom as xmldom
from array import *
from collections import defaultdict
import time

import os
if (os.path.isdir("../database/")):
	db_path = "../database/"
else:
	db_path = "database/"

try:

	seasonList = []
	countList = []
	currentseason = ''
	oldestseason = ''

	# Read the season file
	f = open(db_path+"season.txt","r")
	for buff in f:
		if(buff[0]=='#'):
			try:
				if(buff.index('currentseason') != -1):
					currentseason = buff[buff.index('=')+2:len(buff)-1]
			except ValueError as v:
				oldestseason = buff[buff.index('=')+2:len(buff)-1]
		elif(buff[0]=='['):
			continue
		else:
			buff = buff.split('-')
			seasonList.append(buff[0])
			countList.append(buff[1])
	f.close()

	# Get Current Season
	date = str(time.strftime("%x"))
	currentmonth = int(date[0:2])
	currentyear = date[len(date)-2:len(date)]
	if(currentmonth <= 4):
		smonth = 1
	elif(currentmonth <= 8):
		smonth = 2
	else:
		smonth = 3
	thisseason = "20"+currentyear+"/"+str(smonth)

	# Check if the thisseason and the currentseason is the same. if not, an update is needed
	if(thisseason != currentseason):
		currentseason = thisseason
		seasonList.append(thisseason)
		for i in range(0,len(countList)):
			countList[i] = str(int(countList[i])+1)
		countList.append('1')
		with open(db_path+"season.txt","w") as f:
			f.write("#currentseason = "+currentseason+"\n")
			f.write("#oldestseason = "+oldestseason+"\n")
			f.write("[season-weightedscore]"+"\n")
			for i in range(0,len(countList)):
				f.write(seasonList[i]+'-'+countList[i]+"\n")

except IOError as e:
	print e
