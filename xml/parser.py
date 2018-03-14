import xml.etree.ElementTree as ET
#nsmap = {}
class MomParser():
	def __init__(self, name):
		self.name = name
		for event, elem in ET.iterparse('sample.xml',events=('start','end','start-ns')):
			print event, elem

			print elem.__dict__


