import time

import os
if (os.path.isdir("../database/")):
	db_path = "../database/"
else:
	db_path = "database/"

#inputDate format is "YYYY/MM/DD"
def cal_season_score(inputDate):
	seasonList = []
	countList = []
	currentseason = ''
	oldestseason = ''
	season_count = 1;
	# Read the season file
	season_score = dict()
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
			season_score[buff[0]] = buff[1].strip()
			season_count +=1
	f.close()

	# Get inputDate Season
	date = inputDate
	currentmonth = int(date[5:7])
	currentyear = date[0:4]
	if(currentmonth <= 4):
		smonth = 1
	elif(currentmonth <= 8):
		smonth = 2
	else:
		smonth = 3
	thisseason = currentyear+"/"+str(smonth)
	if thisseason not in season_score:
		return 1
	else:
		#the most current season get the highest score
		return season_count-int(season_score[thisseason])