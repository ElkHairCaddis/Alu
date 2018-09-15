#!/usr/bin/env python3

import sys 

'''
Subset the featureCounts sam file output to only include
multi-aligned reads. 
'''

inSam = sys.argv[1]

with open(inSam, 'r') as infile:
	for line in infile:
		if line[0] != '@':
			multiTag = line.split('\t')[11]
			if int(multiTag.split(':')[2]) > 1:
				print(line.strip('\n'))
		else:
			print(line.strip('\n'))
