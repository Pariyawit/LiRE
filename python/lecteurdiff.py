# -*- coding: utf-8 -*-
import csv
import sys

lecteur = set()

with open('historique_pret.csv', 'rU') as f:
	reader = csv.DictReader(f)
	for row in reader:
		lecteur.add(row['Code barre lecteur'])

#print lecteur

cardnumber = set()
with open('old_lecteur_brest20140313.csv','rU') as f:
	reader = csv.DictReader(f)
	for row in reader:
		cardnumber.add(row['CARDNUMBER'])

missing = []

for l in lecteur:
	if l not in cardnumber:
		missing.append(l)

missing = sorted(missing)

with open('missing_cardnumber.txt','w') as f:
	for m in missing:
		f.write(m+'\n')

cardnumber = set()
with open('old_lecteur_brest20140313.csv','rU') as f:
	reader = csv.DictReader(f)
	for row in reader:
		cardnumber.add(row['CARDNUMBER'])
print 'loaner : '+str(len(lecteur))
print 'all : '+str(len(cardnumber))
print len(missing)
print 'done'