import xml.etree.ElementTree as ET
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest ='file', action = 'store', type=argparse.FileType('r'))
parser.add_argument('-d', dest ='test', action = 'store_true')
args = parser.parse_args()
save = args.file
#print args.file.read()
print type(save)

for event, elem in ET.iterparse(args.file, events=('start', 'end')):
		if event == 'start':
			print event, elem


