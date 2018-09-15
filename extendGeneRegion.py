#!/usr/bin/env python3

'''
Take a protein coding GTF file and extend the start and stop position 
for each locus by 'baseExtend' bases. 
'''

import sys

baseExtend = int(sys.argv[1])
inGTF = sys.argv[2]

with open(inGTF, 'r') as infile:
	for line in infile:
		line = line.strip('\n').split('\t')
		newStart = int(line[3]) - baseExtend
		newEnd = int(line[4]) + baseExtend
		line[3] = str(newStart)
		line[4] = str(newEnd)
		print('\t'.join(line))
