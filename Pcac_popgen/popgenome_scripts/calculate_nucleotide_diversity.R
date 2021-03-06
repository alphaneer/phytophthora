
setwd("/Users/armita/Downloads/popstats/summary_stats")
library("PopGenome")
library("ggplot2")
######################## BEFORE RUNNING ################################
#Assign individuals to appropriate populations (or just 1!)
#However, if using just 1 populations, interpopulation statistic (Dxy)
#of genetic variation cannot be calculated, and need to carry out only analyses
#A, B  but not C, D.
#When all coding sites input, use E to calculate Pi(nonsyn)/Pi(syn) sites.
#Output files either per contig or the entire genome (prefix genome_)
Pop1 <- c("12420_1", "15_13_1", "15_7_1", "2003_3_1", "4032_1", "404_1", "4040_1", "414_1", "415_1", "416_1", "P421_1", "PC13_15_1",
  "12420_2", "15_13_2", "15_7_2", "2003_3_2", "4032_2", "404_2", "4040_2", "414_2", "415_2", "416_2", "P421_2", "PC13_15_2",
  "11-40_1", "11-40_2")
Pop2 <- c("62471_1", "P295_1", "R36_14_1",
  "62471_2", "P295_2", "R36_14_2",
  "17-21_1", "17-21_2")
Pop3 <- c("371_1", "SCRP370_1", "SCRP376_1",
  "371_2", "SCRP370_2", "SCRP376_2")
#In the output for pairwise FST, pop1, pop2 etc. refer to the order in which the populations have been listed here:
populations <- list(Pop1, Pop2, Pop3)
#Number of populations assigned above.
population_no <- length(populations)
pairs <- choose(population_no, 2)
# population_names <- c("Pop1", "Pop2", "Pop3")
population_names <- c("Pcac_Fa", "Pcac_Md", "Pcac_Ri")
#Given in the same order, as above.
#Interval and jump size used in the sliding window analysis
#For graphical comparison of nucleotide diversity in choice populations, amend Addendum B) and E) below.
interval <-  10000
jump_size <-  interval / 10
#########################################################################

#Folder containing FASTA alignments in the current dir
gff <- "gff"
all_folders <- list.dirs("contigs", full.names = FALSE)
#Remove the gff folder from PopGenome contig analysis
contig_folders <- all_folders[all_folders != "gff"]

###Loop through each contig containing folder to calculate stats on each contig separately.
for (dir in contig_folders[contig_folders != ""]){
#for (dir in contig_folders[contig_folders == "contig_10"]){
contig_folder <- paste("contigs/", dir, sep = "")
GENOME.class <- readData(contig_folder, gffpath = gff, include.unknown = TRUE)
GENOME.class <- set.populations(GENOME.class, populations)

#########################################################
#A) calculate Pi (Nei, 1987) for all sites in a given gene.

#Split by and retain only genes for the analysis
GENOME.class.split <- splitting.data(GENOME.class, subsites = "gene")
GENOME.class.split <- diversity.stats(GENOME.class.split, pi = TRUE)

#Divide Pi per number of sites in the gene to calculate value per site
Pi <- GENOME.class.split@Pi / GENOME.class.split@n.sites
Pi_d <- as.data.frame(Pi)

#Loop over each population: print figure and table with raw data to file
for (i in seq_along(population_names)){
file_hist <- paste(dir, "_", population_names[i], "_Pi_per_gene.pdf", sep = "")
pi_plot <- ggplot(Pi_d, aes(x = Pi_d[, i])) +
geom_histogram(colour = "black", fill = "blue") + ggtitle(dir) +
xlab(expression(paste("Average ", pi, " per site"))) +
ylab("Number of genes") + scale_x_continuous(breaks = pretty(Pi_d[, i], n = 10))
analysis <- "Pi"
outdir <- paste("results/", dir, "/", analysis, sep = "")
dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
ggsave(paste(outdir, file_hist, sep="/"), pi_plot)
file_table <- paste(dir, "_", population_names[i], "_Pi_per_gene.txt", sep = "")
file_table2 <- paste("genome_", population_names[i],
"_Pi_per_gene_all.txt", sep = "")
current_gff <- paste(gff, "/", dir, ".gff", sep = "")
gene_ids <- get_gff_info(GENOME.class.split, current_gff, chr = dir,
    feature = FALSE, extract.gene.names = TRUE)
Pi_table <- cbind(gene_ids, Pi[, i])
write.table(Pi_table, file = paste(outdir, file_table, sep="/"), sep = "\t", quote = FALSE,
col.names = FALSE)
#Table with genome-wide results:
write.table(Pi_table, file = file_table2, sep = "\t", quote = FALSE,
col.names = FALSE, append = TRUE)
}
###########################################################
#B) calculate Pi (Nei, 1987) in a sliding window for
#all sites over a given interval
GENOME.class.slide <- sliding.window.transform(GENOME.class, width = interval,
    jump = jump_size, type = 2, whole.data = TRUE)
GENOME.class.slide <- diversity.stats(GENOME.class.slide, pi = TRUE)
#plot the results for all populations over one figure
Pi_persite <- GENOME.class.slide@Pi / interval
Pi_persite_d <- as.data.frame(Pi_persite)
#x axis
ids <- length(GENOME.class.slide@region.names)
xaxis <- seq(from = 1, to = ids, by = 1)

#Plot individual populations
for (i in seq_along(population_names)){
file_slide <- paste(dir, "_", population_names[i], "_Pi_sliding_window.pdf",
sep = "")
slide_plot <- ggplot(Pi_persite_d, aes(x = xaxis, y = Pi_persite_d[, i])) +
geom_smooth(colour = "black", fill = "red") + ggtitle(dir) +
xlab("Contig coordinate (kbp)") +
ylab(expression(paste("Average ", pi, " per site"))) +
scale_x_continuous(breaks = pretty(xaxis, n = 10))
analysis <- "Pi"
outdir <- paste("results/", dir, "/", analysis, sep = "")
dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
ggsave(paste(outdir, file_slide, sep="/"), slide_plot)
#write table with raw data
slide_table <- paste(dir, "_", population_names[i],
"_Pi_per_sliding_window.txt", sep = "")
write.table(Pi_persite[, i], file = paste(outdir, slide_table, sep = "/"), sep = "\t", quote = FALSE,
col.names = FALSE)
}

#B) Addendum
#Plot two populations for comparison
#(here population 1 and 2, but can be changed to reflect the analysis)
#To change populations
#need to change data frame indexes (1 and 2) in the lines below.
title <- paste(dir, "Comparison of", population_names[1], "vs",
population_names[2], sep = ", ")
comp_slide_file <- paste(dir, "_Pi_sliding_window_comparison.pdf", sep = "")
slide_comparison <- ggplot(Pi_persite_d, aes(x = xaxis)) +
geom_smooth(aes(y = Pi_persite_d[, 1]), colour = "red") +
geom_smooth(aes(y = Pi_persite_d[, 2]), colour = "blue") + ggtitle(title) +
xlab("Contig coordinate (kbp)") +
ylab(expression(paste("Average ", pi, " per site"))) +
scale_x_continuous(breaks = pretty(xaxis, n = 10))
analysis <- "Pi"
outdir <- paste("results/", dir, "/", analysis, sep = "")
dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
ggsave(paste(outdir, comp_slide_file, sep="/"), slide_comparison)

############################################################
#C) Calculate Dxy for all sites in a given gene
#if more than 1 population analysed.
#All possible pairwise contrasts

GENOME.class.split <- F_ST.stats(GENOME.class.split)
FST_results <- get.F_ST(GENOME.class.split)
dxy <- GENOME.class.split@nuc.diversity.between / GENOME.class.split@n.sites
current_gff <- paste(gff, "/", dir, ".gff", sep = "")
gene_ids <- get_gff_info(GENOME.class.split, current_gff, chr = dir,
    feature = FALSE, extract.gene.names = TRUE)

#print a histogram of Dxy distribution
#write table with raw data
for (i in seq(pairs)){
dxy_d <- as.data.frame(as.vector(dxy[i, ]))
dxy_table <- cbind(GENOME.class.split@region.names, gene_ids,
    as.vector(dxy[i, ]))
labelling <- gsub("/", "_vs_", row.names(dxy)[i])
file_hist <- paste(dir, "_", labelling, "_dxy_per_gene.pdf", sep = "")
dxy_plot <- ggplot(dxy_d, aes(x = dxy_d[, 1])) +
geom_histogram(colour = "black", fill = "green") + ggtitle(dir) +
xlab("Average Dxy per gene") + ylab("Number of genes") +
scale_x_continuous(breaks = pretty(dxy_d[, 1], n = 10))
analysis <- "Dxy"
outdir <- paste("results/", dir, "/", analysis, sep = "")
dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
ggsave(paste(outdir, file_hist, sep = "/"), dxy_plot)
file_table <- paste(dir, "_", labelling, "_dxy_per_gene.txt", sep = "")
file_table2 <- paste("genome_", labelling, "_dxy_per_gene.txt", sep = "")
write.table(dxy_table, file = paste(outdir, file_table, sep = "/"), sep = "\t", quote = FALSE,
row.names = FALSE, col.names = FALSE)
write.table(dxy_table, file = file_table2, sep = "\t", quote = FALSE,
row.names = FALSE, col.names = FALSE, append = TRUE)
}
############################################################
#D) Calculate Dxy for all sites in a sliding window analysis
#if more than 1 population analysed.
#All possible pairwise contrasts
GENOME.class.slide <- F_ST.stats(GENOME.class.slide)
FST_results <- get.F_ST(GENOME.class.slide)
dxy <- GENOME.class.slide@nuc.diversity.between / GENOME.class.slide@n.sites

#Plot Dxy across the intervals
#write table with raw data
for (i in seq(pairs)){
dxy_d <- as.data.frame(as.vector(dxy[i, ]))
labelling <- gsub("/", "_vs_", row.names(dxy)[i])
file_slide <- paste(dir, "_", labelling, "_dxy_per_sliding_window.pdf",
sep = "")
dxy_plot <- slide_plot <- ggplot(dxy_d, aes(x = xaxis, y = dxy_d[, 1])) +
geom_smooth(colour = "black", fill = "green") + ggtitle(dir) +
xlab("Contig coordinate (kbp)") +
ylab(paste("Average Dxy per ", interval, " bp")) +
scale_x_continuous(breaks = pretty(xaxis, n = 10))
analysis <- "Dxy"
outdir <- paste("results/", dir, "/", analysis, sep = "")
dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
ggsave(paste(outdir, file_slide, sep = "/"), dxy_plot)
file_table <- paste(dir, "_", labelling, "_dxy_per_sliding_window.txt",
sep = "")
write.table(dxy[1, ], file = paste(outdir, file_table, sep = "/"), sep = "\t", quote = FALSE,
col.names = FALSE)
}
##############################################################
#E) When a dataset containing all types of coding sites loaded
#calculate Pi(nonsyn)/Pi(syn) over each
# gene and over a given interval in the genome.
#Gene based
GENOME.class.split.nonsyn <- diversity.stats(GENOME.class.split, pi = TRUE,
    subsites = "nonsyn")
GENOME.class.split.syn <- diversity.stats(GENOME.class.split, pi = TRUE,
    subsites = "syn")
#Interval based
GENOME.class.slide.nonsyn <- diversity.stats(GENOME.class.slide, pi = TRUE,
    subsites = "nonsyn")
GENOME.class.slide.syn <- diversity.stats(GENOME.class.slide, pi = TRUE,
    subsites = "syn")

#Print output, gene-based
#Plot individual populations, gene-based
#Divide Pi per number of sites in the gene to calculate value per site
Pi_ns <- GENOME.class.split.nonsyn@Pi /
GENOME.class.split.syn@Pi / GENOME.class.split@n.sites
Pi_ns_d <- as.data.frame(Pi_ns)

#Loop over each population: print figure and table with raw data to file
for (i in seq_along(population_names)){
  #Check in case all values 0
  Pi_ns_len <- length(Pi_ns[, i])
  Pi_ns_len_na <- sum(sapply(Pi_ns[, i], is.na))
  if (Pi_ns_len > Pi_ns_len_na){
  file_hist <- paste(dir, "_", population_names[i], "_Pi_n_s_per_gene.pdf",
  sep = "")
  pi_plot <- ggplot(Pi_ns_d, aes(x = Pi_ns_d[, i])) +
  geom_histogram(colour = "black", fill = "coral") + ggtitle(dir) +
  xlab(expression(paste("Average ", pi, "ns/", pi, "s", " per site"))) +
  ylab("Number of genes") +
  scale_x_continuous(breaks = pretty(Pi_ns_d[, i], n = 10))
  analysis <- "Pi"
  outdir <- paste("results/", dir, "/", analysis, sep = "")
  dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
  ggsave(paste(outdir, file_hist, sep = "/"), pi_plot)
}
  file_table <- paste(dir, "_", population_names[i], "_Pi_n_s_per_gene.txt",
  sep = "")
  file_table2 <- paste("genome_", population_names[i],
  "_Pi_n_s_per_gene_all.txt", sep = "")
  current_gff <- paste(gff, "/", dir, ".gff", sep = "")
  gene_ids <- get_gff_info(GENOME.class.split, current_gff, chr = dir,
      feature = FALSE, extract.gene.names = TRUE)
  Pi_table <- cbind(gene_ids, Pi_ns[, i])
  write.table(Pi_table, file = paste(outdir, file_table, sep = "/"), sep = "\t", quote = FALSE,
  col.names = FALSE)
  write.table(Pi_table, file = file_table2, sep = "\t", quote = FALSE,
  col.names = FALSE, append = TRUE)
}

#Print output interval based
#plot the results for all populations over one figure
Pi_ns_persite <- GENOME.class.slide.nonsyn@Pi /
GENOME.class.slide.syn@Pi / interval
Pi_ns_persite_d <- as.data.frame(Pi_ns_persite)
#x axis
ids <- length(GENOME.class.slide@region.names)
xaxis <- seq(from = 1, to = ids, by = 1)

#Plot individual populations
for (i in seq_along(population_names)){
  file_slide <- paste(dir, "_", population_names[i],
  "_Pi_n_s_sliding_window.pdf", sep = "")
  Pi_ns_len <- length(Pi_ns_persite[, i])
  Pi_ns_len_na <- sum(sapply(Pi_ns_persite[, i], is.na))
  if (Pi_ns_len > Pi_ns_len_na){
  slide_plot <- ggplot(Pi_ns_persite_d,
      aes(x = xaxis, y = Pi_ns_persite_d[, i])) +
      geom_smooth(colour = "black", fill = "darkviolet") + ggtitle(dir) +
      xlab("Contig coordinate (kbp)") +
      ylab(expression(paste("Average ", pi, "ns/", pi, "s", " per site"))) +
      scale_x_continuous(breaks = pretty(xaxis, n = 10))
  analysis <- "Pi"
  outdir <- paste("results/", dir, "/", analysis, sep = "")
  dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
  ggsave(paste(outdir,file_slide, sep="/"), slide_plot)
}
  #write table with raw data
  slide_table <- paste(dir, "_", population_names[i],
  "_Pi_n_s_per_sliding_window.txt", sep = "")
  write.table(Pi_ns_persite[, i], file = paste(outdir, slide_table, sep="/"), sep = "\t",
  quote = FALSE, col.names = FALSE)
}

#E) Addendum
#Plot two populations for comparison
#here population 1 and 2, but can be changed to reflect the analysis
#To change populations
#need to change data frame indexes (1 and 2) in the lines below.
#Plot both populations for comparison
title <- paste(dir, "Comparison of", population_names[1], "ver.",
population_names[2], sep = ", ")

comp_slide_file <- paste(dir, "_Pi_n_s_sliding_window_comparison.pdf", sep = "")
if (Pi_ns_len > Pi_ns_len_na){
slide_comparison <- ggplot(Pi_ns_persite_d, aes(x = xaxis)) +
geom_smooth(aes(y = Pi_ns_persite_d[, 1]), colour = "deeppink") +
geom_smooth(aes(y = Pi_ns_persite_d[, 2]), colour = "lightskyblue") +
ggtitle(title) + xlab("Contig coordinate (kbp)") +
ylab(expression(paste("Average ", pi, "ns/", pi, "s", " per site"))) +
scale_x_continuous(breaks = pretty(xaxis, n = 10))
analysis <- "Pi"
outdir <- paste("results/", dir, "/", analysis, sep = "")
dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
ggsave(paste(outdir, comp_slide_file, sep="/"), slide_comparison)
}

}

###Plot genome wide histograms
for (i in seq_along(population_names)){
#Pi table
file_table2 <- paste("genome_", population_names[i], "_Pi_per_gene_all.txt",
sep = "")
x <- as.data.frame(read.delim(file_table2))
file_hist <- paste("genome_", population_names[i], "_Pi_per_gene_all.pdf",
sep = "")
pi_plot <- ggplot(x, aes(x = x[, 3])) +
geom_histogram(colour = "black", fill = "blue") +
xlab(expression(paste("Average ", pi, " per site"))) +
ylab("Number of genes") + scale_x_continuous(breaks = pretty(x[, 3], n = 10))
analysis <- "Pi"
outdir <- paste("results/genome/", analysis, sep = "")
dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
ggsave(paste(outdir, file_hist, sep = "/"), pi_plot)

#Pi nonsyn/syn
file_table2 <- paste("genome_", population_names[i], "_Pi_n_s_per_gene_all.txt",
sep = "")
x <- as.data.frame(read.delim(file_table2))
file_hist <- paste("genome_", population_names[i], "_Pi_n_s_per_gene_all.pdf",
sep = "")
pi_plot <- ggplot(x, aes(x = x[, 3])) +
geom_histogram(colour = "black", fill = "coral") +
xlab(expression(paste("Average ", pi, "ns/", pi, "s", " per site"))) +
ylab("Number of genes") + scale_x_continuous(breaks = pretty(x[, 3], n = 10))
ggsave(paste(outdir, file_hist, sep = "/"), pi_plot)
}

#Dxy table
for (i in seq(pairs)){
  labelling <- gsub("/", "_vs_", row.names(dxy)[i])
  file_table2 <- paste("genome_", labelling, "_dxy_per_gene.txt", sep = "")
  x <- as.data.frame(read.delim(file_table2))
  file_hist <- paste("genome_", labelling, "_dxy_per_gene.pdf", sep = "")
  dxy_plot <- ggplot(x, aes(x = x[, 3])) +
  geom_histogram(colour = "black", fill = "green") +
  xlab("Average Dxy per gene") + ylab("Number of genes") +
  scale_x_continuous(breaks = pretty(x[, 3], n = 10))
  analysis <- "Dxy"
  outdir <- paste("results/genome/", analysis, sep = "")
  dir.create(outdir,recursive = TRUE, showWarnings = FALSE)
  ggsave(paste(outdir, file_hist, sep = "/"), dxy_plot)
}
