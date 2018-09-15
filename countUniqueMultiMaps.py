#!/usr/bin/env python3

'''
Considering only multi-aligned reads, we are searching for reads
with all alignments mapped to the same Alu sub family. We will 
count how many such reads map to each sub family. 
'''

import sys

'''
Here, the sam file is a cut form of the featureCounts sam output. 
We have only retained the read ID, total number of alignments, 
alignment ID, and sub family assignment. 
'''
samFile = sys.argv[1]
aluFile = sys.argv[2]

'''
Check if all alignments mapped to same sub family. 
If so, increment read count for that family. 
'''
def checkForUniqueAssignment(famList, subFamCountDict):
	numDistinctFam = len(set(famList))
	if numDistinctFam == 1:
		subFam = famList[0]
		subFamCountDict[subFam] += 1

'''
Create dictionary to store Alu sub family read count.
'''
subFamCounts = {}
with open(aluFile, 'r') as infile:
	for line in infile:
		subFamCounts[line.strip('\n')] = 0

'''
Iterate through list of multi-aligned reads. The file has been 
sorted by read ID. 
'''
currentID = 0
currentSubFamList = ['AluY'] # Hack instead of dealing with key error. Remember to remove 1 from value
with open(samFile, 'r') as infile:
	for line in infile:
		cols = line.strip('\n').split('\t')
		readID = int(cols[0].split(':')[2])
		readFamily = cols[3]

		# We have encountered a new read. 
		# Analyze old read and reset initial values.
		if readID != currentID:
			checkForUniqueAssignment(currentSubFamList, subFamCounts)
			currentID = readID
			currentSubFamList.clear()

		# Add new sub family to list. 
		currentSubFamList.append(readFamily)

'''
Write results to standard out.
'''
print('subFamily\tuniqueMultiMapCount')
for fam in subFamCounts:
	print(fam + '\t' + str(aluDict[fam]))
