#!/usr/bin/python

'''
This program parses information from fasta files and gff files for the location,
sequence and functional information for annotated gene models and RxLRs.
'''

#-----------------------------------------------------
# Step 1
# Import variables & load input files
#-----------------------------------------------------

import sys
import argparse
import re
from sets import Set
from collections import defaultdict
from operator import itemgetter
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('--gff_format',required=True,type=str,choices=['gff3', 'gtf'],help='Gff file format')
ap.add_argument('--gene_gff',required=True,type=str,help='Gff file of predicyted gene models')
ap.add_argument('--gene_fasta',required=True,type=str,help='amino acid sequence of predicted proteins')
ap.add_argument('--SigP2',required=True,type=str,help='fasta file of genes testing positive for signal peptide using SigP2.0')
ap.add_argument('--SigP4',required=True,type=str,help='fasta file of genes testing positive for signal peptide using SigP4.1')
ap.add_argument('--phobius',required=True,type=str,help='txt file of headers from gene testing positive for signal peptide using phobius')
ap.add_argument('--trans_mem',required=True,type=str,help='txt file of headers from gene testing positive for tranmembrane proteins by TMHMM')
ap.add_argument('--GPI_anchor',required=True,type=str,help='txt file of headers from gene testing positive for GPI anchors as identified by GPI-SOM')
#ap.add_argument('--RxLR_motif',required=True,type=str,help='fasta file of genes testing positive for RxLR-EER motifs')
#ap.add_argument('--RxLR_Hmm',required=True,type=str,help='fasta file of genes testing positive for RxLR-EER domains using an hmm model')
#ap.add_argument('--RxLR_WY',required=True,type=str,help='fasta file of genes testing positive for WY domains using an hmm model')
ap.add_argument('--RxLR_total',required=True,type=str,help='fasta file of all transcripts considered RxLRs')
#ap.add_argument('--CRN_LFLAK',required=True,type=str,help='fasta file of genes testing positive for LFLAK domains using an hmm model')
#ap.add_argument('--CRN_DWL',required=True,type=str,help='fasta file of genes testing positive for DWL domains using an hmm model')
ap.add_argument('--CRN_total',required=True,type=str,help='fasta file of all transcripts considered CRNs')
#ap.add_argument('--ortho_name',required=True,type=str,help='the name used for the organism during orthology analysis')
#ap.add_argument('--ortho_file',required=True,type=str,help='txt file of ortholog groups')
ap.add_argument('--DEG_files',required=True,nargs='+',type=str,help='space spererated list of files containing DEG information')
ap.add_argument('--raw_counts',required=True,type=str,help='raw count data as output from DESeq')
ap.add_argument('--fpkm',required=True,type=str,help='normalised fpkm count data as output from DESeq')
ap.add_argument('--InterPro',required=True,type=str,help='The Interproscan functional annotation .tsv file')
ap.add_argument('--Swissprot',required=True,type=str,help='A parsed table of BLAST results against the Swissprot database. Note - must have been parsed with swissprot_parser.py')
ap.add_argument('--SNP',required=True,nargs='+',type=str,help='A list of annotated .vcf with information on synonymous and non-synonymous SNPs in comparisons to the reference. Note - each of these files should be contained within a sepperate directory which is named on the comparison to be made.')
ap.add_argument('--indel',required=True,type=str,help='An of annotated .vcf with indel information.')
ap.add_argument('--struct_variants',required=True,type=str,help='An of annotated .vcf with indel information.')

ap.add_argument('--gene_conversion',required=True,type=str,help='Conversion of gene ids of effector genes prior to ncbi-renaming for RxLRs, secreted genes and CRNs.')

conf = ap.parse_args()



with open(conf.gene_gff) as f:
    gene_lines = f.readlines()

with open(conf.gene_fasta) as f:
    prot_lines = f.readlines()

with open(conf.SigP2) as f:
    sigP2_lines = f.readlines()

with open(conf.SigP4) as f:
    sigP4_lines = f.readlines()

with open(conf.phobius) as f:
    phobius_lines = f.readlines()

with open(conf.trans_mem) as f:
    trans_mem_lines = f.readlines()

with open(conf.GPI_anchor) as f:
    gpi_lines = f.readlines()

# with open(conf.RxLR_motif) as f:
#     RxLR_motif_lines = f.readlines()

# with open(conf.RxLR_Hmm) as f:
#     RxLR_hmm_lines = f.readlines()

# with open(conf.RxLR_WY) as f:
#     RxLR_WY_lines = f.readlines()

with open(conf.RxLR_total) as f:
    RxLR_total_lines = f.readlines()

# with open(conf.CRN_LFLAK) as f:
#     CRN_LFLAK_lines = f.readlines()

# with open(conf.CRN_DWL) as f:
#     CRN_DWL_lines = f.readlines()

with open(conf.CRN_total) as f:
    CRN_total_lines = f.readlines()

#with open(conf.ortho_file) as f:
#    ortho_lines = f.readlines()

DEG_files = conf.DEG_files
DEG_dict = defaultdict(list)
for DEG_file in DEG_files:
    with open(DEG_file) as f:
        filename = DEG_file
        DEG_lines = f.readlines()
        for line in DEG_lines:
            if line.startswith('baseMean'):
                continue
            else:
                split_line = line.split()
                gene_name = split_line[0]
                log_change = split_line[2]
                P_val = split_line[6]
                entryname = "_".join([filename, gene_name])
                DEG_dict[entryname].extend([log_change, P_val])

with open(conf.raw_counts) as f:
    raw_count_lines = f.readlines()

with open(conf.fpkm) as f:
    fpkm_lines = f.readlines()

with open(conf.InterPro) as f:
    InterPro_lines = f.readlines()

with open(conf.Swissprot) as f:
    swissprot_lines = f.readlines()

SNP_files = conf.SNP
SNP_dict = defaultdict(list)
for SNP_file in SNP_files:
    comparison = SNP_file.split("/")[-2]
    with open(SNP_file) as f:
        filename = SNP_file
        SNP_lines = f.readlines()
        for line in SNP_lines:
            if line.startswith('#'):
                continue
            else:
                split_line = line.split()
                SNP_info = split_line[7]
                split_info = SNP_info.split("|")
                effect = split_info[1]
                # print effect
                transcript_id = split_info[6]
                if 'missense_variant' in effect:
                    AA_change = split_info[10]
                    SNP_dict[transcript_id].append("_".join([effect, AA_change]))
                elif 'nonsense_variant' in effect:
                    AA_change = "stop"
                    SNP_dict[transcript_id].append("_".join([effect, AA_change]))
                    # print effect

with open(conf.indel) as f:
    indel_lines = f.readlines()

indel_dict = defaultdict(list)
for line in indel_lines:
    if line.startswith('#'):
        continue
    else:
        split_line = line.split()
        indel_info = split_line[7]
        split_info = indel_info.split("|")
        effect = split_info[1]
        # print effect
        transcript_id = split_info[6]
        AA_change = split_info[10]
        # print "_".join([transcript_id, effect, AA_change])
        indel_dict[transcript_id].append("_".join([effect, AA_change]))

with open(conf.struct_variants) as f:
    sv_lines = f.readlines()

sv_dict = defaultdict(list)
for line in sv_lines:
    if line.startswith('#'):
        continue
    else:
        split_line = line.split()
        variant_info = split_line[7]
        split_info = variant_info.split("|")
        effect = split_info[1]
        # print effect
        transcript_id = split_info[6]
        AA_change = split_info[10]
        # print "_".join([transcript_id, effect, AA_change])
        indel_dict[transcript_id].append("_".join([effect, AA_change]))

with open(conf.gene_conversion) as f:
    conversion_lines = f.readlines()


#-----------------------------------------------------
# Load protein sequence data into a dictionary
#-----------------------------------------------------

prot_dict = defaultdict(list)
for line in prot_lines:
    line = line.rstrip()
    if line.startswith('>'):
        header = line.replace('>', '')
    else:
        prot_dict[header] += line

#-----------------------------------------------------
# Load signalP2.0 files into a set
#-----------------------------------------------------

SigP2_set = Set()
for line in sigP2_lines:
    line = line.rstrip()
    if line.startswith('>'):
        split_line = line.split()
        header = split_line[0].replace('>', '')
        SigP2_set.add(header)

#-----------------------------------------------------
# Load signalP4.0 files into a set
#-----------------------------------------------------

SigP4_set = Set()
for line in sigP4_lines:
    line = line.rstrip()
    if line.startswith('>'):
        split_line = line.split()
        header = split_line[0].replace('>', '')
        SigP4_set.add(header)

#-----------------------------------------------------
# Load phobius files into a set
#-----------------------------------------------------

phobius_set = Set()
for line in phobius_lines:
    header = line.rstrip()
    phobius_set.add(header)

#-----------------------------------------------------
# Load TMHMM headers into a set
#-----------------------------------------------------

trans_mem_set = Set()
for line in trans_mem_lines:
    header = line.rstrip()
    trans_mem_set.add(header)

#-----------------------------------------------------
# Load GPI-anchored proteins into a set
#-----------------------------------------------------

gpi_set = Set()
for line in gpi_lines:
    header = line.rstrip()
    gpi_set.add(header)
#
# #-----------------------------------------------------
# # Load RxLR motif +ve proteins into a set
# #-----------------------------------------------------
#
# RxLR_motif_set = Set()
# for line in RxLR_motif_lines:
#     line = line.rstrip()
#     if line.startswith('>'):
#         split_line = line.split()
#         header = split_line[0].replace('>', '')
#         RxLR_motif_set.add(header)
#
# #-----------------------------------------------------
# # Load RxLR hmm +ve proteins into a set
# #-----------------------------------------------------
#
# RxLR_hmm_set = Set()
# for line in RxLR_hmm_lines:
#     line = line.rstrip()
#     if line.startswith('>'):
#         split_line = line.split()
#         header = split_line[0].replace('>', '')
#         RxLR_hmm_set.add(header)
#
# #-----------------------------------------------------
# # Load RxLR hmm +ve proteins into a set
# #-----------------------------------------------------
#
# RxLR_WY_set = Set()
# for line in RxLR_WY_lines:
#     line = line.rstrip()
#     if line.startswith('>'):
#         split_line = line.split()
#         header = split_line[0].replace('>', '')
#         RxLR_WY_set.add(header)

#-----------------------------------------------------
# Load RxLR total +ve proteins into a set
#-----------------------------------------------------

RxLR_total_set = Set()
for line in RxLR_total_lines:
    header = line.rstrip()
    RxLR_total_set.add(header)
    # line = line.rstrip()
    # if line.startswith('>'):
    #     split_line = line.split()
    #     header = split_line[0].replace('>', '')
    #     RxLR_total_set.add(header)
#
# #-----------------------------------------------------
# # Load CRN LFLAK hmm +ve proteins into a set
# #-----------------------------------------------------
#
# CRN_LFLAK_set = Set()
# for line in CRN_LFLAK_lines:
#     line = line.rstrip()
#     if line.startswith('>'):
#         split_line = line.split()
#         header = split_line[0].replace('>', '')
#         CRN_LFLAK_set.add(header)
#
# #-----------------------------------------------------
# # Load CRN DWL hmm +ve proteins into a set
# #-----------------------------------------------------
#
# CRN_DWL_set = Set()
# for line in CRN_DWL_lines:
#     line = line.rstrip()
#     if line.startswith('>'):
#         split_line = line.split()
#         header = split_line[0].replace('>', '')
#         CRN_DWL_set.add(header)

#-----------------------------------------------------
# Load CRN total proteins into a set
#-----------------------------------------------------

CRN_total_set = Set()
for line in CRN_total_lines:
    header = line.rstrip()
    CRN_total_set.add(header)
    # line = line.rstrip()
    # if line.startswith('>'):
    #     split_line = line.split()
    #     header = split_line[0].replace('>', '')
    #     CRN_total_set.add(header)

#-----------------------------------------------------
# Store genes and their ortholog groups in a dictionary
#-----------------------------------------------------

# organism_name = conf.ortho_name
# ortho_dict = defaultdict(list)
# for line in ortho_lines:
#     line = line.rstrip()
#     split_line = line.split()
#     orthogroup = split_line[0]
#     orthogroup = orthogroup.replace(":", "")
#     genes_in_group = [ x for x in split_line if organism_name in x ]
#     for gene in genes_in_group:
#         gene = gene.replace(organism_name, '').replace('|', '')
#         # print gene
#         ortho_dict[gene] = orthogroup

#-----------------------------------------------------
#
# Build a dictionary of raw count data
#
#-----------------------------------------------------

raw_read_count_dict = defaultdict(list)

line1 = raw_count_lines.pop(0)
line1 = line1.rstrip("\n")
count_treatment_list = line1.split("\t")
count_treatment_list = list(filter(None, count_treatment_list))
# print count_treatment_list

for line in raw_count_lines:
    line = line.rstrip("\n")
    split_line = line.split("\t")
    transcript_id = split_line.pop(0)
    # if not len(count_treatment_list) == len(split_line):
    #     print "error"
    # print len(count_treatment_list)
    # print len(split_line)
    for i, treatment in enumerate(count_treatment_list):
        # i = i-1
        raw_read_count = float(split_line[i])
    # for treatment, raw_read_count in zip(count_treatment_list, split_line):
        dict_key = "_".join([transcript_id, treatment])
        raw_read_count_dict[dict_key].append(raw_read_count)

#-----------------------------------------------------
#
# Build a dictionary of normalised fpkm data
#
#-----------------------------------------------------

fpkm_dict = defaultdict(list)

line1 = fpkm_lines.pop(0)
line1 = line1.rstrip("\n")
fpkm_treatment_list = line1.split("\t")
fpkm_treatment_list = list(filter(None, fpkm_treatment_list))

for line in fpkm_lines:
    line = line.rstrip("\n")
    split_line = line.split("\t")
    transcript_id = split_line.pop(0)
    for i, treatment in enumerate(fpkm_treatment_list):
        fpkm = float(split_line[i])
        dict_key = "_".join([transcript_id, treatment])
        fpkm_dict[dict_key].append(fpkm)

#-----------------------------------------------------
#
# Build a dictionary of interproscan annotations
# Annotations first need to be filtered to remove
# redundancy. This is done by first loading anntoations
# into a set.
#-----------------------------------------------------

interpro_set =  Set([])
interpro_dict = defaultdict(list)

for line in InterPro_lines:
    line = line.rstrip("\n")
    split_line = line.split("\t")
    interpro_columns = []
    index_list = [0, 4, 5, 11, 12]
    for x in index_list:
        if len(split_line) > x:
            interpro_columns.append(split_line[x])
    set_line = ";".join(interpro_columns)
    if set_line not in interpro_set:
        gene_id = interpro_columns[0]
        interpro_feat = ";".join(interpro_columns[1:])
        interpro_dict[gene_id].append(interpro_feat)
    interpro_set.add(set_line)


#-----------------------------------------------------
#
# Build a dictionary of Swissprot annotations
#-----------------------------------------------------

swissprot_dict = defaultdict(list)

for line in swissprot_lines:
    line = line.rstrip("\n")
    split_line = line.split("\t")
    gene_id = split_line[0]
    swissprot_columns = itemgetter(14, 12, 13)(split_line)

    swissprot_dict[gene_id].extend(swissprot_columns)


#-----------------------------------------------------
#
# Build a dictionary of Swissprot annotations
#-----------------------------------------------------

conversion_dict = defaultdict(list)

for line in conversion_lines:
    line = line.rstrip("\n")
    split_line = line.split("\t")
    old_id = split_line[0]
    new_id = split_line[2]
    conversion_dict[new_id] = old_id
    # print "-".join([new_id, old_id])


#-----------------------------------------------------
# Step 3
# Itterate through genes in file, identifying if
# they ahve associated information
#-----------------------------------------------------

# Print header line:
header_line = ['transcript_id']
header_line.extend(['contig', 'start', 'stop', 'strand'])
#header_line.extend(['sigP2', 'sigP4', 'phobius', 'RxLR_motif', 'RxLR_hmm', 'WY_hmm', 'RxLR_total', 'CRN_LFLAK', 'CRN_DWL', 'CRN_total', 'orthogroup'])
header_line.extend(['sigP2', 'sigP4', 'phobius', 'TMHMM', 'GPI_anchor', 'secreted', 'RxLR_total', 'CRN_total'])
for treatment in set(count_treatment_list):
    treatment = "raw_count_" + treatment
    header_line.append(treatment)

for treatment in set(fpkm_treatment_list):
    treatment = "fpkm_" + treatment
    header_line.append(treatment)

for DEG_file in DEG_files:
    file_name = DEG_file.split('/')[-1]
    header_line.append("LFC_" + file_name)
    header_line.append("P-val_" + file_name)
header_line.append('prot_seq')
header_line.append('Non-syn_SNP')
header_line.append('InDel')
print ("\t".join(header_line))

transcript_lines = []

if conf.gff_format == 'gff3':
    for line in gene_lines:
        line = line.rstrip()
        if line.startswith('#'):
            continue
        split_line = line.split()
        if 'transcript' in split_line[2] or 'mRNA' in split_line[2]:
            transcript_lines.append("\t".join(split_line))

if conf.gff_format == 'gtf':
    prev_id = 'first'
    transcript_line = ''

    for line in gene_lines:
        line = line.rstrip()
        if line.startswith('#'):
            continue
        split_line = line.split("\t")
        if 'CDS' in split_line[2]:
            transcript_id = split_line[8]
            split_col9 = split_line[8].split(';')
            # print split_col9
            transcript_id = "".join([ x for x in split_col9 if 'transcript_id' in x ])
            # print transcript_id
            transcript_id = transcript_id.replace(' ','').replace('transcript_id', '').replace('"', '')
            # print transcript_id
            if transcript_id != prev_id:
                # if prev_id == 'first':
                #     continue
                transcript_lines.append("\t".join(transcript_line))
                transcript_line = split_line
                transcript_line[2] = "mRNA"
                transcript_line[8] = transcript_id
                # print split_line
                # print transcript_line
            elif split_line[6] == '+':
                transcript_line[4] = split_line[4]
            elif split_line[6] == '-':
                transcript_line[3] = split_line[3]
            # print "\t".join([prev_id, transcript_id])
            prev_id = transcript_id
            # print transcript_id
    del transcript_lines[0]

# print "\n".join(transcript_lines)

for line in transcript_lines:
    split_line = line.split("\t")
    useful_cols = [split_line[0],  split_line[3], split_line[4], split_line[6]]
    # Set defaults
    sigP2 = ''
    sigP4 = ''
    phobius = ''
    trans_mem = ''
    gpi = ''
    # RxLR_motif = ''
    # RxLR_hmm = ''
    # WY_hmm = ''
    RxLR_total = ''
    # CRN_LFLAK = ''
    # CRN_DWL = ''
    CRN_total = ''
    # orthogroup = ''
    prot_seq = ''
    swissprot_cols = []
    interpro_col = []
    # Identify gene id
    if 'ID' in split_line[8]:
        split_col9 = split_line[8].split(';')
        transcript_id = "".join([ x for x in split_col9 if 'ID' in x ])
        transcript_id = transcript_id.replace('ID=', '')
    else:
        transcript_id = split_line[8]
    gene_id = transcript_id.split(".")[0]
    old_gene = "".join(conversion_dict[gene_id])
    old_id = transcript_id.replace(gene_id, old_gene)

    if old_id in SigP2_set:
        sigP2 = 'Yes'
    if old_id in SigP4_set:
        sigP4 = 'Yes'
    if old_id in phobius_set:
        phobius = 'Yes'
    if old_id in trans_mem_set:
        trans_mem = 'Yes'
    if old_id in gpi_set:
        gpi = 'Yes'
    if any([sigP2 == 'Yes', sigP4 == 'Yes']) and all([trans_mem == '', gpi == '']):
        secreted = 'Yes'
    else:
        secreted = ''
    # if transcript_id in RxLR_motif_set:
    #     RxLR_motif = 'Yes'
    # if transcript_id in RxLR_hmm_set:
    #     RxLR_hmm = 'Yes'
    # if transcript_id in RxLR_WY_set:
    #     WY_hmm = 'Yes'
    # gene_id = transcript_id.split('.')[0]
    if old_id in RxLR_total_set:
        RxLR_total = 'Yes'
    # if transcript_id in CRN_LFLAK_set:
    #     CRN_LFLAK = 'Yes'
    # if transcript_id in CRN_DWL_set:
    #     CRN_DWL = 'Yes'
    if old_id in CRN_total_set:
        CRN_total = 'Yes'
    # if ortho_dict[transcript_id]:
    #     orthogroup = ortho_dict[transcript_id]
    DEG_out = []
    for DEG_file in DEG_files:
        entryname = "_".join([DEG_file, transcript_id])
        if DEG_dict[entryname]:
            DEG_out.append(DEG_dict[entryname][0])
            DEG_out.append(DEG_dict[entryname][1])
        else:
            DEG_out.append('.')
            DEG_out.append('.')

    # # Add in read count data:
    mean_count_cols = []
    for treatment in set(count_treatment_list):
        dict_key = "_".join([transcript_id, treatment])
        expression_values = raw_read_count_dict[dict_key]
        # print expression_values
        mean_count = np.mean(expression_values)
        mean_count = np.round_(mean_count, decimals=0)
        mean_count_cols.append(mean_count.astype(str))
    # print mean_count_cols
    mean_fpkm_cols = []
    for treatment in set(fpkm_treatment_list):
        dict_key = "_".join([transcript_id, treatment])
        # print dict_key
        expression_values = fpkm_dict[dict_key]
        # print expression_values
        mean_fpkm = np.mean(expression_values)
        # print mean_fpkm
        mean_fpkm = np.round_(mean_fpkm, decimals=0)
        mean_fpkm_cols.append(mean_fpkm.astype(str))
        # print mean_fpkm_cols

    # # Add in Swissprot info
    if swissprot_dict[transcript_id]:
        swissprot_cols = swissprot_dict[transcript_id]
    else:
        swissprot_cols = ['.','.','.']
    # Add in interproscan info
    if interpro_dict[transcript_id]:
        interpro_col = "|".join(interpro_dict[transcript_id])
    else:
        interpro_col = '.'

    # Add in SNP info
    if SNP_dict[transcript_id]:
        # print(SNP_dict[transcript_id])
        non_syn_col = "|".join(SNP_dict[transcript_id])
    else:
        non_syn_col = ""

    if indel_dict[transcript_id]:
        indel_col = "|".join(indel_dict[transcript_id])
    else:
        indel_col = ""

    prot_seq = "".join(prot_dict[transcript_id])
    # outline = [transcript_id, sigP2, phobius ,RxLR_motif, RxLR_hmm, WY_hmm, CRN_LFLAK, CRN_DWL, orthogroup]
    outline = [transcript_id]
    outline.extend(useful_cols)
    # outline.extend([sigP2, sigP4, phobius, RxLR_motif, RxLR_hmm, WY_hmm, RxLR_total, CRN_LFLAK, CRN_DWL, CRN_total, orthogroup])
    outline.extend([sigP2, sigP4, phobius])
    outline.extend([trans_mem, gpi, secreted])
    outline.extend([RxLR_total, CRN_total])
    # outline.append(orthogroup)
    outline.extend(mean_count_cols)
    outline.extend(mean_fpkm_cols)
    outline.extend(DEG_out)
    outline.append(non_syn_col)
    outline.append(indel_col)
    outline.append(prot_seq)
    outline.extend(swissprot_cols)
    outline.append(interpro_col)


    print "\t".join(outline)
    # print DEG_out
