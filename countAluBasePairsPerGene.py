#!/usr/bin/env python3

'''
Count the number of base pairs within each gene locus that belongs to an 
Alu region. Accomplish this task one chromosome at a time. 

The input files are cut forms (subset by chromosome) of the 'featureCounts'
counts file. We will add the number of Alu bases as an additional column and 
remove some meaningless columns. 
'''

import sys
import os

origAluGTF = sys.argv[1] # Cut Alu GTF file e.x. chr13Alus.gtf
geneList = '/path/to/cut/featureCounts/output' + sys.argv[2]
rpeGeneList = '/path/to/RPE/geneList/rpeGeneList.txt'


'''
Read list of RPE genes.
'''
rpeGenes = []
with open(rpeGeneList, 'r') as infile:
	for line in infile:
		rpeGenes.append(line.strip('\n'))	


'''
Read a cut form of GTF file with only start and end positions for each Alu segment.  
'''
aluPositions = []
totalAlus = 0
with open(origAluGTF, 'r') as infile:
	for line in infile:
		line = line.strip('\n').split('\t')
		aluPositions.append( [int(line[0]), int(line[1])] )
		totalAlus += 1


'''
Parse through list of genes (all genes from same chromosome) and alu regions. First, check if alu region
falls within gene. If so, add length of alu region to the count of gene's total number of Alu bases.

Also output whether the gene is associated with RPE or not
'''
with open(geneList, 'r') as infile:
	for line in infile:
		aluIndex = 0
		line = line.strip('\n').split('\t')
		aluBPCount = 0
		aluCount = 0

		# Ignore genes with count of 0
		if ';' not in line[2] and int(line[6]) > 0:
			geneStartPos = int(line[2])
			geneEndPos = int(line[3])

			# While current Alu region occurs before gene region, move to next Alu  
			while ( geneStartPos - aluPositions[aluIndex][1] > -1 ): 
				aluIndex += 1
				# Searched through all possible Alu regions, move to next gene
				if aluIndex == totalAlus: 
					break

			# Now, Alu either occurs within gene region (increment counts)
			# Or Alu is entirely past region (finished with this gene, no more possible Alus to count)
			while ( geneEndPos - aluPositions[aluIndex][0] > -1 ):
				aluCount += 1
				aluBPCount += (aluPositions[aluIndex][1] - aluPositions[aluIndex][0])
				aluIndex += 1
				if aluIndex == totalAlus:
					break

			line.append(str(aluCount)) # Add total number of Alu regions in locus
			line.append(str(aluBPCount)) # Add total number of Alu base pairs in locus

			# This line is for downstream R analysis. We will partition the genes 
			# according to this identifier and create two density curves. 
			if line[0] in rpeGenes:
				line.append('RPE')
			else:
				line.append('NoRPE')
			print('\t'.join(line))
