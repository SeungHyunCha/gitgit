
import argparse

class A:
	def __init__(self):
		self.a = 1
		self.b = 2

	def printInfo(self):
		print "test"

def myprint():
	print "mom!"

def myprint2():
	print "mombfr"

parser = argparse.ArgumentParser()
#parser.add_argument("mom", type=str, help="print mom")
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action = 'store_true')
group.add_argument('-q', '--quiet', action = 'store_true')
group.add_argument('-a', '--add', action = 'store_true')
args = parser.parse_args()

if args.quiet:
	a = A()
	a.printInfo()
	print 'hi'
elif args.verbose:
	print 'hihihi'
elif args.add:
	print 'hi2'
else:
	print 'bye'

