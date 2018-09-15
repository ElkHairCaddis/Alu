#!/bin/bash

# Example script showing full mapping and gene count procedure
# with command line arguments. 

# Align raw fastqs to hg19 with STAR.
starGenome=''
fqDir=''
STAROutDir=''
./STAR --runThreadN 16 \
	--genomeDir ${starGenome} \
	--outFilterMismatchNMax 10 \
	--readFilesIn ${fqDir}/rawReads.fastq
	--outFileNamePrefix ${STAROutDir}/Alignment
	--outFilterMultiMapNmax 40 


# Map aligned reads to Alu regions. -M to count multi-aligned reads.
aluGTFDir=''
FCOutDir=''
./featureCounts -R SAM -T 16 -t exon -g alu_id -O -M \
	-a ${AluGTFDir}/Alus.gtf \
	-o ${FCOutDir}/alu.Counts \
	${STAROutDir}/Alignment.sam

# Retain only Alu-mapped, multi-aligned reads for further processing. 
grep 'XS:Z:Assigned' ${FCOutDir}/Alignments.featureCounts.sam > AluReads.tmp

./outputMultiMappers.py AluReads.tmp > MM_AluReads.tmp

# Cut file to only retain read ID, total number of alignments
# current alignment number, and subFamily mapping. 
cut -f1,12,13,16 MM_AluReads.tmp > MM_AluReads.cut

# Finally, count the number of multi-aligned reads that 
# map uniquely to one subfamily. 
./countUniqueMultiMaps.py MM_AluReads.cut > subFamMMCounts.tsv 
