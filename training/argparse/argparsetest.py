import argparse

a = argparse.ArgumentParser()
a.add_argument(dest='mo', nargs = '?')
a.add_argument(dest='attr', nargs = '?')
args = a.parse_args()

if args.mo:
    print args.mo

if args.attr:
    print args.attr
