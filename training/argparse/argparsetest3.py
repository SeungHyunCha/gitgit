import xml.etree.ElementTree as ET
import argparse
import os

path_dir = '/home/cha/Python_test/Mytest/training/argparse' 
file_list = os.listdir(path_dir)
for i in file_list:
	if i == 'sample.xml':
		filename = open(i, 'r')

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest ='file', action = 'store', type=argparse.FileType('r'))
#parser.add_argument('-p', dest ='file_dir', action = filename, type=argparse.FileType('r'))
parser.add_argument('-d', dest ='test', action = 'store_true')
args = parser.parse_args()

try:
	if args.file:
		f = open('mom', 'wb')
		f.write(args.file.read())
		f.close()
	else: fopen = open('mom','rb')	
	
except Exception as ex:
	if args.file:
		f = open('mom', 'wb')
		f.write(args.file.read())
		f.close()	
	else: print ex	



if args.test:
	for event, elem in ET.iterparse(fopen, events=('start', 'end')):
			if event == 'start':
				print event, elem


