import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--list",nargs="+",choices=['a','b','c'])
args = parser.parse_args()

l = args.list

for i in l:
	print i

