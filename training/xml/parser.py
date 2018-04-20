import xml.etree.ElementTree as ET
class MomParser():
	def __init__(self, name):
		self.name = name
	
	def parse(self):	
		for event, elem in ET.iterparse(self.name,events=('start','end')):
			print event, elem, elem.tag, elem.attrib, elem.text 

if __name__ == '__main__':
	file = 'sample.xml'
	a = MomParser(file)
	a.parse()
