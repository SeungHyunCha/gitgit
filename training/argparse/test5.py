'''
import argparse

parser = argparse.ArgumentParser()

bar = parser.add_mutually_exclusive_group()
bar.add_argument('-a', action="store_false", default=None)
foo = parser.add_mutually_exclusive_group()

args = parser.parse_args()
print args.__dict__

if args.a:
	print args.__dict__
'''

import argparse

parser = argparse.ArgumentParser(prog='mydaemon')
sp = parser.add_subparsers()
sp_start = sp.add_parser('start', help='Starts %(prog)s daemon')
sp_stop = sp.add_parser('stop', help='Stops %(prog)s daemon')
sp_restart = sp.add_parser('restart', help='Restarts %(prog)s daemon')

args = parser.parse_args()
print args.__dict__


