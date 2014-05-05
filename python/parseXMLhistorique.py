# -*- coding: utf-8 -*-
#python parseXMLhistorique.py historique_file.csv
import csv
import sys

from xml.etree import ElementTree
import xml.dom.minidom as xmldom

historique = ElementTree.Element("historique")

subfield_name = ['noticekoha','codebarrelecteur','type','date','lecteurkoha','titre','exemplairekoha']

with open(sys.argv[1], 'rU') as f:
	reader = csv.DictReader(f)
	for row in reader:
		transaction = ElementTree.SubElement(historique,"transaction")
		colnum = 0
		#print row
		for item in row:
			subfield = ElementTree.SubElement(transaction,subfield_name[colnum])
			subfield.text = row[item].decode("utf8")
			colnum = colnum+1
	
	tree = ElementTree.ElementTree(historique)
	tree.write("../database/historique.xml",encoding="UTF-8", xml_declaration=True)

	xml = xmldom.parse("../database/historique.xml")
	pretty_xml_as_string = xml.toprettyxml()
	with open("../database/historique.xml","w") as f:
		f.write(pretty_xml_as_string.encode('utf8'));
