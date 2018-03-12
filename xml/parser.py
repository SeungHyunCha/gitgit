#!/usr/bin/python
import xml.etree.ElementTree as ET
#nsmap = {}

for event, elem in ET.iterparse('sample.xml',events=('start','end','start-ns')):
	print event, elem
#	print locals()
print elem.__dict__
#	ns, url = elem
#	nsmap[ns] = url
#print nsmap
#print vars()
