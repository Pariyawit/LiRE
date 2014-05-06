# -*- coding: UTF-8 -*-

import BaseXClient
import xml.dom.minidom as xmldom
from array import *
from collections import defaultdict

try:
	session1 = BaseXClient.Sesssion('localhost',1984,'admin','admin')
	session2 = BaseXClient.Sesssion('localhost',1984,'admin','admin')
	session3 = BaseXClient.Sesssion('localhost',1984,'admin','admin')
	session1.execute('open keyword')
	session2.execute('open bookref')
except IOError as e:
	print e