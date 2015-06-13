#!/usr/bin/python
import getopt,sys
try:
	opts,args = getopt.getopt(sys.argv[1:],"rscq:",['remix','short','cover','query='])
except:
	usage()
	exit()
print opts
print args