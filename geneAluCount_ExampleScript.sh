#!/bin/bash

# Example script showing full mapping and gene count procedure
# with command line arguments. Eventually, produce a density
# plot of Alu expression for RPE vs non-RPE associated
# genes. 

# Align raw fastqs to hg19 with STAR
starGenome=''
fqDir=''
STAROutDir=''
./STAR --runThreadN 16 \
	--genomeDir ${starGenome} \
	--outFilterMismatchNMax 10 \
	--readFilesIn ${fqDir}/rawReads.fastq
	--outFileNamePrefix ${STAROutDir}/Alignment


# Map aligned reads to Alu regions
aluGTFDir=''
FCOutDir=''
./featureCounts -R SAM -T 16 -t exon -g alu_id -O \
	-a ${AluGTFDir}/Alus.gtf \
	-o ${FCOutDir}/alu.Counts \
	${STAROutDir}/Alignment.sam


# featureCounts outputs a SAM file with tags for the 
# mapping. If a read is assigned to an Alu region, it will 
# have the XS:Z:Assigned tag. We only want to retain 
# reads that are in fact mapped to an Alu region for downstream 
# analysis.
aluSamFile=''
grep 'XS:Z:Assigned' ${FCOutDir}/alu.featureCounts.sam > ${aluSamFile}


# Now, we will re-map these Alu reads to genomic loci. The input
# gene gtf was altered during the analysis to extend the loci 
# by specific numbers of base pairs. 
geneGTFDir=''
NUM_EXTEND=500
./extendGeneRegion.py ${NUM_EXTEND} ${geneGTFDir}/proteinCodingGenes.gtf > ${geneGTFDir}/${NUM_EXTEND}extend_proteinCodingGenes.gtf

FCOutDir=''
./featureCounts -R SAM -T 16 -t exon -g alu_id -O \
	-a ${geneGTFDir}/${NUM_EXTEND}extend_proteinCodingGenes.gtf \
	-o ${FCOutDir}/aluGene.Counts \
	${aluSamFile}


# We want to normalize the gene alu counts by number of alu bases
# per gene locus. We do this per chromosome. For example, chr14:
# Will need to be performed for chr1-22, X, Y. 
grep -P '^chr14\t' ${aluGTFDir}/Alus.gtf | cut -f4,5 > Alus_chr14.tmp
grep -P '\tchr14\t' ${FCOutDir}/aluGene.Counts > aluGene_chr14.Counts.tmp
./countAluBasePairsPerGene.py Alus_chr14.tmp aluGene_chr14.Counts.tmp > aluGene_chr14NormCounts.tmp

# Combine all output tsv files and clean directory.
cat aluGene_chr*NormCounts.tmp > aluGeneCounts.tsv
rm *.tmp

# This is the end of the analyis process. Now, just a simple R script to produce the
# density distribution plots.
./plotAluDistribution.R 
