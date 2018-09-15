#!/usr/bin/env Rscript

# Example script 

# Read in normalized gene Alu counts .tsv file. 
# Plot density distribution for RPE vs non-RPE 
# associated genes. 

library(ggplot)

countFile <- '/path/to/counts/geneAluCounts.tsv'
alu.counts <- read.csv(file = countfile, sep = '\t')
alu.counts$Normalized <- alu.counts$rawAluCount / aluCounts$AluBasePairCount
alu.counts$LogNorm <- log(alu.counts$Normalized)

ggplot(alu.counts, aes(LogNorm, fill = Type)) # Type = RPE or non-RPE associated?
	+ geom_density(alpha=.2) 
	+ ggtitle('Density Plot Example Title')
	+ theme(plot.title = element_text(hjust = .5)) # Center title 
	+ labs(x = 'Log of Normalized Alu Count') 
