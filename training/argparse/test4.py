import argparse

def main(opt):
	print opt

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	bar = parser.add_mutually_exclusive_group()
	bar.add_argument('-s', action='store_true', default=True)
	bar.add_argument('-m', action='store_true', default=False)
	#bar = parser.add_argument_group()
	bar = parser.add_mutually_exclusive_group()
	bar.add_argument('-y', metavar='year', type=int,
		            dest='iy', nargs='?', default=0)
	baz = bar.add_argument_group()
	g_13 = baz.add_mutually_exclusive_group()
	g_13.add_argument('-1', dest='i1',
		          help='Display single month output.',
		          action='store_true', default=True)
	g_13.add_argument('-3', dest='i3',
		          help='Display prev/current/next month output.',
		          action='store_true', default=False)
	#aaa = bar.add_argument_group()
	baz.add_argument(metavar='month', type=int,
		            choices=range(1, 13),
		            dest='mo', nargs='?', default=1)
	baz.add_argument(metavar='year', type=int,
		            dest='yr', nargs='?', default=2000)

	main(parser.parse_args())
