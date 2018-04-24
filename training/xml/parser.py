import xml.etree.ElementTree as ET
from cStringIO import StringIO
import os
class MomParser():
	def __init__(self, name):
		self.name = name
	
	def parse(self):	
		for event, elem in ET.iterparse(self.name,events=('start','end')):
			print event, elem, elem.tag, elem.attrib, elem.text 

if __name__ == '__main__':
	file = '''<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
</data>
'''
	test = StringIO(file)
	a = MomParser(StringIO(test))
# 	a = MomParser(StringIO(file))
	a.parse()
