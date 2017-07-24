
# 1. Alignment of Pcac raw reads vs the 414 genome

Alignment of reads from a single run:

```bash
  Reference=$(ls repeat_masked/P.cactorum/414_v2/filtered_contigs_repmask/414_v2_contigs_unmasked.fa)
  for StrainPath in $(ls -d qc_dna/paired/P.*/* | grep -v -e '10300' -e '404' -e '414' -e '415' -e '416' -e 'PC13_15' -e '2003_3' | grep -e 'P.cactorum' -e 'P.idaei'); do
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/spades
    Strain=$(echo $StrainPath | rev | cut -f1 -d '/' | rev)
    Organism=$(echo $StrainPath | rev | cut -f2 -d '/' | rev)
    F_Read=$(ls $StrainPath/F/*_trim.fq.gz)
    R_Read=$(ls $StrainPath/R/*_trim.fq.gz)
    echo $F_Read
    echo $R_Read
    OutDir=analysis/genome_alignment/bowtie/$Organism/$Strain/vs_414
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/genome_alignment
    qsub $ProgDir/bowtie/sub_bowtie.sh $Reference $F_Read $R_Read $OutDir
  done
```

Alignment of reads from multiple sequencing runs:

For isolates with two runs of data:

```bash
  Reference=$(ls repeat_masked/P.cactorum/414_v2/filtered_contigs_repmask/414_v2_contigs_unmasked.fa)
  for StrainPath in $(ls -d qc_dna/paired/P*/* | grep -e 'P.cactorum' -e 'P.idaei' | grep -w -e '2003_3' -e '415' -e '416' -e 'PC13_15'); do
    echo $StrainPath
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/spades/multiple_libraries
    Strain=$(echo $StrainPath | rev | cut -f1 -d '/' | rev)
    Organism=$(echo $StrainPath | rev | cut -f2 -d '/' | rev)
    echo $Strain
    echo $Organism
    F1_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n1 | tail -n1);
    R1_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n1 | tail -n1);
    F2_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n2 | tail -n1);
    R2_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n2 | tail -n1);
    echo $F1_Read
    echo $R1_Read
    echo $F2_Read
    echo $R2_Read
    OutDir=analysis/genome_alignment/bowtie/$Organism/$Strain/vs_414
    ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/genome_alignment
    qsub $ProgDir/bowtie/sub_bowtie_2lib.sh $Reference $F1_Read $R1_Read $F2_Read $R2_Read $OutDir
  done
```

for isolates with three runs of data:

```bash
  Reference=$(ls repeat_masked/P.cactorum/414_v2/filtered_contigs_repmask/414_v2_contigs_unmasked.fa)
  for StrainPath in $(ls -d qc_dna/paired/P*/* | grep -e 'P.cactorum' -e 'P.idaei' | grep -w -e '404' -e '414'); do
      echo $StrainPath
      ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/assemblers/spades/multiple_libraries
      Strain=$(echo $StrainPath | rev | cut -f1 -d '/' | rev)
      Organism=$(echo $StrainPath | rev | cut -f2 -d '/' | rev)
      echo $Strain
      echo $Organism
      F1_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n1 | tail -n1);
      R1_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n1 | tail -n1);
      F2_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n2 | tail -n1);
      R2_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n2 | tail -n1);
      F3_Read=$(ls $StrainPath/F/*_trim.fq.gz | head -n3 | tail -n1);
      R3_Read=$(ls $StrainPath/R/*_trim.fq.gz | head -n3 | tail -n1);
      echo $F1_Read
      echo $R1_Read
      echo $F2_Read
      echo $R2_Read
      echo $F3_Read
      echo $R3_Read
      OutDir=analysis/genome_alignment/bowtie/$Organism/$Strain/vs_414
      ProgDir=/home/armita/git_repos/emr_repos/tools/seq_tools/genome_alignment
      qsub $ProgDir/bowtie/sub_bowtie_3lib.sh $Reference $F1_Read $R1_Read $F2_Read $R2_Read $F3_Read $R3_Read $OutDir
    done
```


# 2. Pre SNP calling cleanup


## 2.1 Rename input mapping files in each folder by prefixing with the strain ID

```bash
  for File in $(ls analysis/genome_alignment/bowtie/*/*/vs_414/414_v2_contigs_unmasked.fa_aligned.sam | grep -v '10300'); do
    Strain=$(echo $File | rev | cut -f3 -d '/' | rev)
    Organism=$(echo $File | rev | cut -f4 -d '/' | rev)
    echo $Strain
    echo $Organism
    OutDir=analysis/popgen/$Organism/$Strain
    CurDir=$PWD
    mkdir -p $OutDir
    cd $OutDir
    cp -s $CurDir/$File "$Strain"_vs_414_v2_aligned.sam
    cd $CurDir
  done
```

## 2.2 Remove multimapping reads, discordant reads. PCR and optical duplicates, and add read group and sample name to each mapped read (preferably, the shortest ID possible)

Convention used:
qsub $ProgDir/sub_pre_snp_calling.sh <INPUT SAM FILE> <SAMPLE_ID>

```bash
  for Sam in $(ls $PWD/analysis/popgen/*/*/*_vs_414_v2_aligned.sam | grep -v '10300' | tail -n+2); do
    Strain=$(echo $Sam | rev | cut -f2 -d '/' | rev)
    Organism=$(echo $Sam | rev | cut -f3 -d '/' | rev)
    CurDir=$PWD
    OutDir=$(dirname $Sam)
    cd $OutDir
    ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/snp
    qsub $ProgDir/sub_pre_snp_calling.sh $Sam $Strain
    cd $CurDir
  done
```

<!-- ##Copy outputs from cleanup to alignment folder

```bash
for Strain in A4 Bc1 Bc23 Nov27 Nov5 Nov71 Nov77 Nov9 ONT3 SCRP245_v2 SCRP249 SCRP324 SCRP333
do
    Bam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.bam
    rgBam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam
    Bai="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam.bai
    Txt="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.txt
    Directory=analysis/genome_alignment/bowtie/*/$Strain/vs_Bc16_unmasked_max1200/
    mv $Bam $Directory
    mv $rgBam $Directory
    mv $Bai $Directory
    mv $Txt $Directory
done
Strain=Bc16
Bam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.bam
rgBam="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam
Bai="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup_rg.bam.bai
Txt="$Strain"_95m_contigs_unmasked.fa_aligned_nomulti_proper_sorted_nodup.txt
Directory=analysis/genome_alignment/bowtie/*/$Strain/vs_Bc16_unmasked_max1200_SNP/
mv $Bam $Directory
mv $rgBam $Directory
mv $Bai $Directory
mv $Txt $Directory
``` -->

# 3. Run SNP calling

#Runs a SNP calling script from Maria in order to be able to draw up a phylogeny
To change in each analysis:

```bash
input=/home/groups/harrisonlab/project_files/phytophthora_fragariae/analysis/genome_alignment/bowtie
reference=repeat_masked/P.fragariae/Bc16/filtered_contigs_repmask/95m_contigs_unmasked.fa

filename=$(basename "$reference")
output="${filename%.*}.dict"
```

##Prepare genome reference indexes required by GATK

```bash
Reference=$(ls repeat_masked/P.cactorum/414_v2/filtered_contigs_repmask/414_v2_contigs_unmasked.fa)
OutDir=$(dirname $Reference)
mkdir -p $OutDir
ProgDir=/home/sobczm/bin/picard-tools-2.5.0
java -jar $ProgDir/picard.jar CreateSequenceDictionary R=$Reference O=$OutDir/414_v2_contigs_unmasked.dict
samtools faidx $Reference
```

###Copy index file to same folder as BAM alignments

```bash
Reference=$(ls repeat_masked/P.cactorum/414_v2/filtered_contigs_repmask/414_v2_contigs_unmasked.fa)
for AlignDir in $(ls -d analysis/popgen/P.*/*/); do
    Index="$Reference".dict
    Directory=analysis/genome_alignment/bowtie/*/$Strain/vs_Bc16_unmasked_max1200/
    cp $Index $AlignDir/.
done
```

Move to the directory where the output of SNP calling should be placed. Then
Start SNP calling with GATK.
The submission script required need to be custom-prepared for each analysis,
depending on what samples are being analysed. See inside the submission script
below:

```bash
CurDir=$PWD
OutDir=analysis/popgen/SNP_calling
mkdir -p $OutDir
cd $OutDir
ProgDir=/home/armita/git_repos/emr_repos/ProgDir/phytophthora/Pcac_popgen
qsub $ProgDir/sub_SNP_calling_multithreaded.sh
cd $CurDir
```

## Filter SNPs based on this region being present in all isolates

Only retain biallelic high-quality SNPS with no missing data (for any individual) for genetic analyses below (in some cases, may allow some missing data in order to retain more SNPs, or first remove poorly sequenced individuals with too much missing data and then filter the SNPs).

```bash
cp analysis/popgen/SNP_calling/414_v2_contigs_unmasked_temp.vcf analysis/popgen/SNP_calling/414_v2_contigs_unmasked.vcf
Vcf=$(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked.vcf)
ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/snp
# mq=40
# qual=30
# dp=10
# gq=30
# na=0.95
# indel=Y
# $VcfLib/vcffilter -f "QUAL > $qual & MQ > $mq"
qsub $ProgDir/sub_vcf_parser.sh $Vcf 40 30 10 30 1 N

ProgDir=/home/adamst/git_repos/scripts/popgen/snp
qsub $ProgDir/sub_vcf_parser.sh $Vcf

```

```bash
mv 414_v2_contigs_unmasked_filtered.vcf analysis/popgen/SNP_calling/414_v2_contigs_unmasked_filtered.vcf
```

<!--
In some organisms, may want to thin (subsample) SNPs in high linkage diseqilibrium down to
1 SNP  per e.g. 10 kbp just for the population structure analyses.
```bash
VcfTools=/home/sobczm/bin/vcftools/bin
$VcfTools/vcftools --vcf $input_vcf --thin 10000 --recode --out ${input_vcf%.vcf}_thinned
```
-->

## Collect VCF stats

General VCF stats (remember that vcftools needs to have the PERL library exported)

```bash
  VcfTools=/home/sobczm/bin/vcftools/bin
  export PERL5LIB="$VcfTools:$PERL5LIB"
  Vcf=$(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked.vcf)
  Stats=$(echo $Vcf | sed 's/.vcf/.stat/g')
  perl $VcfTools/vcf-stats $Vcf > $Stats
  VcfFiltered=$(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked_filtered.vcf)
  Stats=$(echo $VcfFiltered | sed 's/.vcf/.stat/g')
  perl $VcfTools/vcf-stats $VcfFiltered > $Stats
```

Calculate the index for percentage of shared SNP alleles between the individuals.

```bash
  for Vcf in $(ls analysis/popgen/SNP_calling/*_filtered.vcf); do
      ProgDir=/home/armita/git_repos/emr_repos/scripts/popgen/snp
      $ProgDir/similarity_percentage.py $Vcf
  done
```

# Visualise the output as heatmap and clustering dendrogram
```bash
for Log in $(ls analysis/popgen/SNP_calling/*distance.log); do
  ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/snp
  Rscript --vanilla $ProgDir/distance_matrix.R $Log
  mv Rplots.pdf analysis/popgen/SNP_calling/.
done
```

<!-- Remove monomorphic sites (minor allele count minimum 1). Argument --vcf is the filtered VCF file, and --out is the suffix to be used for the output file.

```bash
for Vcf in $(ls analysis/popgen/SNP_calling/*_filtered.vcf); do
echo $Vcf
Out=$(basename $Vcf .vcf)
echo $Out
VcfTools=/home/sobczm/bin/vcftools/bin
$VcfTools/VcfTools --vcf $Vcf --mac 1 --recode --out analysis/popgen/SNP_calling/$Out
done
``` -->

## Carry out PCA and plot the results

This step could not be carried out due to problems installing dependancies
<!--
```bash
for Vcf in $(ls analysis/popgen/SNP_calling/*_filtered.vcf); do
    echo $Vcf
    ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/snp
    # Out=$(basename $Vcf)
    Out=analysis/popgen/SNP_calling
    echo $Out
    Rscript --vanilla $ProgDir/pca.R $Vcf $Out/PCA.pdf
done
``` -->


## Calculate an NJ tree

based on all the SNPs. Outputs a basic display of the tree, plus a Newick file to be used for displaying the tree in FigTree and beautifying it.

```bash
for Vcf in $(ls analysis/popgen/SNP_calling/*_filtered.vcf); do
    echo $Vcf
    Ploidy=2
    ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/snp
    $ProgDir/nj_tree.sh $Vcf $Ploidy
    mv Rplots.pdf analysis/popgen/SNP_calling/NJ_tree.pdf
done
```

```bash
for VcfFiltered in $(ls analysis/popgen/SNP_calling/*_filtered.vcf); do
Stats=$(echo $VcfFiltered | sed 's/.vcf/.stat/g')
VcfTools=/home/sobczm/bin/vcftools/bin
perl $VcfTools/vcf-stats $VcfFiltered > $Stats
done
```


# Identify SNPs in gene models:

Create custom SnpEff genome database

```bash
SnpEff=/home/sobczm/bin/snpEff
nano $SnpEff/snpEff.config
```


Add the following lines to the section with databases:

```
#---
# EMR Databases
#----
# Fus2 genome
Fus2v1.0.genome : Fus2
# Bc16 genome
Bc16v1.0.genome: BC-16
# P414 genome
P414v1.0.genome: 414
```

Collect input files

```bash
Reference=$(ls repeat_masked/P.cactorum/414_v2/filtered_contigs_repmask/414_v2_contigs_unmasked.fa)
Gff=$(ls gene_pred/final_ncbi/P.cactorum/414_v2/final_ncbi/414_v2_genes_incl_ORFeffectors_renamed.gff3)
SnpEff=/home/sobczm/bin/snpEff
mkdir $SnpEff/data/P414v1.0
cp $Reference $SnpEff/data/P414v1.0/sequences.fa
cp $Gff $SnpEff/data/P414v1.0/genes.gff

#Build database using GFF3 annotation
java -jar $SnpEff/snpEff.jar build -gff3 -v P414v1.0
```


## Annotate VCF files
```bash
CurDir=/home/groups/harrisonlab/project_files/idris
cd $CurDir
for a in $(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked_filtered.vcf); do
    echo $a
    filename=$(basename "$a")
    SnpEff=/home/sobczm/bin/snpEff
    java -Xmx4g -jar $SnpEff/snpEff.jar -v -ud 0 P414v1.0 $a > ${filename%.vcf}_annotated.vcf
    mv snpEff_genes.txt analysis/popgen/SNP_calling/snpEff_genes_${filename%.vcf}.txt
    mv snpEff_summary.html analysis/popgen/SNP_calling/snpEff_summary_${filename%.vcf}.html
    mv *_filtered* analysis/popgen/SNP_calling/.
done
```



# 3.1 P. idaei vs P414

```bash
  Prefix=Pi_vs_P414
  OutDir=analysis/popgen/SNP_calling/$Prefix
  mkdir -p $OutDir

  Vcf=$(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked.vcf)
  ExcludeList="12420 15_13 15_7 2003_3 4032 404 414 415 416  62471 PC13_15 P295 R36_14"
  VcfLib=/home/sobczm/bin/vcflib/bin
  $VcfLib/vcfremovesamples $Vcf $ExcludeList > $OutDir/$Prefix.vcf
  cat $OutDir/$Prefix.vcf | awk -F "\t" '$1 ~ "#" || $10 ~ "1/1" || $11 ~ "1/1" || $12 ~ "1/1" || $10 ~ "0/1" || $11 ~ "0/1" || $12 ~ "0/1" { print}' > $OutDir/"$Prefix"_filtered.vcf

  VcfTools=/home/sobczm/bin/vcftools/bin
  $VcfTools/vcftools --vcf $OutDir/"$Prefix"_filtered.vcf --remove-indels --recode --out $OutDir/"$Prefix"_filtered_no_indels
  # mq=40
  # qual=30
  # dp=10
  # gq=30
  # na=0.95
  # indel=Y
  # $VcfLib/vcffilter -f "QUAL > $qual & MQ > $mq" $OutDir/"$Prefix"_ed.vcf | $VcfLib/vcffilter -g "DP > $dp & GQ > $gq" > $OutDir/temp.vcf
  # VcfTools=/home/sobczm/bin/vcftools/bin
  # $VcfTools/vcftools --vcf $OutDir/temp.vcf --remove-indels --mac 1 --recode --out $OutDir/"$Prefix"_filtered

  for Vcf in $(ls $OutDir/"$Prefix"_filtered_no_indels.recode.vcf); do
      echo $Vcf
      ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/summary_stats
      $ProgDir/annotate_snps_genome.sh $Vcf P414v1.0

      filename=$(basename "$Vcf")
      Prefix=$(echo $filename | sed 's/.vcf//g')
      SnpEff=/home/sobczm/bin/snpEff
      java -Xmx4g -jar $SnpEff/snpEff.jar -v -ud 0 P414v1.0 $Vcf > $OutDir/"$Prefix"_annotated.vcf
      mv snpEff_genes.txt $OutDir/snpEff_genes_$Prefix.txt
      mv snpEff_summary.html $OutDir/snpEff_summary_$Prefix.html

      #Create subsamples of SNPs containing those in a given category

      #genic (includes 5', 3' UTRs)
      java -jar $SnpEff/SnpSift.jar filter "(ANN[*].EFFECT has 'missense_variant') || (ANN[*].EFFECT has 'nonsense_variant') || (ANN[*].EFFECT has 'synonymous_variant') || (ANN[*].EFFECT has 'intron_variant') || (ANN[*].EFFECT has '5_prime_UTR_variant') || (ANN[*].EFFECT has '3_prime_UTR_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_gene.vcf
      #coding
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant') || (ANN[0].EFFECT has 'synonymous_variant')" $OutDir/${filename%.vcf}_annotated.vcf > $OutDir/"$Prefix"_coding.vcf
      #non-synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_nonsyn.vcf
      #synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'synonymous_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_syn.vcf
      #Four-fold degenrate sites (output file suffix: 4fd)
      ProgDir=/home/sobczm/bin/popgen/summary_stats
      python $ProgDir/parse_snpeff_synonymous.py $OutDir/"$Prefix"_syn.vcf
  done
```

# 3.2 P. cactorum ex. apple vs P414

```bash
  Prefix=Pc_apple_vs_P414
  OutDir=analysis/popgen/SNP_calling/$Prefix
  mkdir -p $OutDir

  Vcf=$(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked.vcf)
  ExcludeList="12420 15_13 15_7 2003_3 4032 4040 404 414 415 416 62471 371 SCRP370 SCRP376"
  VcfLib=/home/sobczm/bin/vcflib/bin
  $VcfLib/vcfremovesamples $Vcf $ExcludeList > $OutDir/$Prefix.vcf
  cat $OutDir/$Prefix.vcf | awk -F "\t" '$1 ~ "#" || $10 ~ "1/1" || $11 ~ "1/1" || $12 ~ "1/1" || $10 ~ "0/1" || $11 ~ "0/1" || $12 ~ "0/1" { print}' > $OutDir/"$Prefix"_filtered.vcf

  VcfTools=/home/sobczm/bin/vcftools/bin
  $VcfTools/vcftools --vcf $OutDir/"$Prefix"_filtered.vcf --remove-indels --recode --out $OutDir/"$Prefix"_filtered_no_indels
  # mq=40
  # qual=30
  # dp=10
  # gq=30
  # na=0.95
  # indel=Y
  # $VcfLib/vcffilter -f "QUAL > $qual & MQ > $mq" $OutDir/"$Prefix"_ed.vcf | $VcfLib/vcffilter -g "DP > $dp & GQ > $gq" > $OutDir/temp.vcf
  # VcfTools=/home/sobczm/bin/vcftools/bin
  # $VcfTools/vcftools --vcf $OutDir/temp.vcf --remove-indels --mac 1 --recode --out $OutDir/"$Prefix"_filtered

  for Vcf in $(ls $OutDir/"$Prefix"_filtered_no_indels.recode.vcf); do
      echo $Vcf
      ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/summary_stats
      $ProgDir/annotate_snps_genome.sh $Vcf P414v1.0

      filename=$(basename "$Vcf")
      Prefix=$(echo $filename | sed 's/.vcf//g')
      SnpEff=/home/sobczm/bin/snpEff
      java -Xmx4g -jar $SnpEff/snpEff.jar -v -ud 0 P414v1.0 $Vcf > $OutDir/"$Prefix"_annotated.vcf
      mv snpEff_genes.txt $OutDir/snpEff_genes_$Prefix.txt
      mv snpEff_summary.html $OutDir/snpEff_summary_$Prefix.html

      #Create subsamples of SNPs containing those in a given category

      #genic (includes 5', 3' UTRs)
      java -jar $SnpEff/SnpSift.jar filter "(ANN[*].EFFECT has 'missense_variant') || (ANN[*].EFFECT has 'nonsense_variant') || (ANN[*].EFFECT has 'synonymous_variant') || (ANN[*].EFFECT has 'intron_variant') || (ANN[*].EFFECT has '5_prime_UTR_variant') || (ANN[*].EFFECT has '3_prime_UTR_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_gene.vcf
      #coding
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant') || (ANN[0].EFFECT has 'synonymous_variant')" $OutDir/${filename%.vcf}_annotated.vcf > $OutDir/"$Prefix"_coding.vcf
      #non-synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_nonsyn.vcf
      #synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'synonymous_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_syn.vcf
      #Four-fold degenrate sites (output file suffix: 4fd)
      ProgDir=/home/sobczm/bin/popgen/summary_stats
      python $ProgDir/parse_snpeff_synonymous.py $OutDir/"$Prefix"_syn.vcf
  done
```

# 3.3 P. cactorum ex. strawberry vs P414

```bash
  Prefix=Pc_strawberry_vs_P414
  OutDir=analysis/popgen/SNP_calling/$Prefix
  mkdir -p $OutDir

  Vcf=$(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked.vcf)
  ExcludeList="PC13_15 P295 R36_14 371 SCRP370 SCRP376"
  VcfLib=/home/sobczm/bin/vcflib/bin
  $VcfLib/vcfremovesamples $Vcf $ExcludeList > $OutDir/$Prefix.vcf
  cat $OutDir/$Prefix.vcf | awk -F "\t" '$1 ~ "#" || $10 ~ "1/1" || $11 ~ "1/1" || $12 ~ "1/1" || $10 ~ "0/1" || $11 ~ "0/1" || $12 ~ "0/1" { print}' > $OutDir/"$Prefix"_filtered.vcf

  VcfTools=/home/sobczm/bin/vcftools/bin
  $VcfTools/vcftools --vcf $OutDir/"$Prefix"_filtered.vcf --remove-indels --recode --out $OutDir/"$Prefix"_filtered_no_indels
  # mq=40
  # qual=30
  # dp=10
  # gq=30
  # na=0.95
  # indel=Y
  # $VcfLib/vcffilter -f "QUAL > $qual & MQ > $mq" $OutDir/"$Prefix"_ed.vcf | $VcfLib/vcffilter -g "DP > $dp & GQ > $gq" > $OutDir/temp.vcf
  # VcfTools=/home/sobczm/bin/vcftools/bin
  # $VcfTools/vcftools --vcf $OutDir/temp.vcf --remove-indels --mac 1 --recode --out $OutDir/"$Prefix"_filtered

  for Vcf in $(ls $OutDir/"$Prefix"_filtered_no_indels.recode.vcf); do
      echo $Vcf
      ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/summary_stats
      $ProgDir/annotate_snps_genome.sh $Vcf P414v1.0

      filename=$(basename "$Vcf")
      Prefix=$(echo $filename | sed 's/.vcf//g')
      SnpEff=/home/sobczm/bin/snpEff
      java -Xmx4g -jar $SnpEff/snpEff.jar -v -ud 0 P414v1.0 $Vcf > $OutDir/"$Prefix"_annotated.vcf
      mv snpEff_genes.txt $OutDir/snpEff_genes_$Prefix.txt
      mv snpEff_summary.html $OutDir/snpEff_summary_$Prefix.html

      #Create subsamples of SNPs containing those in a given category

      #genic (includes 5', 3' UTRs)
      java -jar $SnpEff/SnpSift.jar filter "(ANN[*].EFFECT has 'missense_variant') || (ANN[*].EFFECT has 'nonsense_variant') || (ANN[*].EFFECT has 'synonymous_variant') || (ANN[*].EFFECT has 'intron_variant') || (ANN[*].EFFECT has '5_prime_UTR_variant') || (ANN[*].EFFECT has '3_prime_UTR_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_gene.vcf
      #coding
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant') || (ANN[0].EFFECT has 'synonymous_variant')" $OutDir/${filename%.vcf}_annotated.vcf > $OutDir/"$Prefix"_coding.vcf
      #non-synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_nonsyn.vcf
      #synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'synonymous_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_syn.vcf
      #Four-fold degenrate sites (output file suffix: 4fd)
      ProgDir=/home/sobczm/bin/popgen/summary_stats
      python $ProgDir/parse_snpeff_synonymous.py $OutDir/"$Prefix"_syn.vcf
  done
```


# 3.4 P414 vs P414

```bash
  Prefix=P414_vs_P414
  OutDir=analysis/popgen/SNP_calling/$Prefix
  mkdir -p $OutDir

  Vcf=$(ls analysis/popgen/SNP_calling/414_v2_contigs_unmasked.vcf)
  ExcludeList="12420 15_13 15_7 2003_3 4032 404 415 416 PC13_15 62471 P295 R36_14 371 SCRP370 SCRP376"
  VcfLib=/home/sobczm/bin/vcflib/bin
  $VcfLib/vcfremovesamples $Vcf $ExcludeList > $OutDir/$Prefix.vcf
  cat $OutDir/$Prefix.vcf | awk -F "\t" '$1 ~ "#" || $10 ~ "1/1" || $11 ~ "1/1" || $12 ~ "1/1" || $10 ~ "0/1" || $11 ~ "0/1" || $12 ~ "0/1" { print}' > $OutDir/"$Prefix"_filtered.vcf

  VcfTools=/home/sobczm/bin/vcftools/bin
  $VcfTools/vcftools --vcf $OutDir/"$Prefix"_filtered.vcf --remove-indels --recode --out $OutDir/"$Prefix"_filtered_no_indels
  # mq=40
  # qual=30
  # dp=10
  # gq=30
  # na=0.95
  # indel=Y
  # $VcfLib/vcffilter -f "QUAL > $qual & MQ > $mq" $OutDir/"$Prefix"_ed.vcf | $VcfLib/vcffilter -g "DP > $dp & GQ > $gq" > $OutDir/temp.vcf
  # VcfTools=/home/sobczm/bin/vcftools/bin
  # $VcfTools/vcftools --vcf $OutDir/temp.vcf --remove-indels --mac 1 --recode --out $OutDir/"$Prefix"_filtered

  for Vcf in $(ls $OutDir/"$Prefix"_filtered_no_indels.recode.vcf); do
      echo $Vcf
      ProgDir=/home/armita/git_repos/emr_repos/ProgDir/popgen/summary_stats
      $ProgDir/annotate_snps_genome.sh $Vcf P414v1.0

      filename=$(basename "$Vcf")
      Prefix=$(echo $filename | sed 's/.vcf//g')
      SnpEff=/home/sobczm/bin/snpEff
      java -Xmx4g -jar $SnpEff/snpEff.jar -v -ud 0 P414v1.0 $Vcf > $OutDir/"$Prefix"_annotated.vcf
      mv snpEff_genes.txt $OutDir/snpEff_genes_$Prefix.txt
      mv snpEff_summary.html $OutDir/snpEff_summary_$Prefix.html

      #Create subsamples of SNPs containing those in a given category

      #genic (includes 5', 3' UTRs)
      java -jar $SnpEff/SnpSift.jar filter "(ANN[*].EFFECT has 'missense_variant') || (ANN[*].EFFECT has 'nonsense_variant') || (ANN[*].EFFECT has 'synonymous_variant') || (ANN[*].EFFECT has 'intron_variant') || (ANN[*].EFFECT has '5_prime_UTR_variant') || (ANN[*].EFFECT has '3_prime_UTR_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_gene.vcf
      #coding
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant') || (ANN[0].EFFECT has 'synonymous_variant')" $OutDir/${filename%.vcf}_annotated.vcf > $OutDir/"$Prefix"_coding.vcf
      #non-synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'missense_variant') || (ANN[0].EFFECT has 'nonsense_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_nonsyn.vcf
      #synonymous
      java -jar $SnpEff/SnpSift.jar filter "(ANN[0].EFFECT has 'synonymous_variant')" $OutDir/"$Prefix"_annotated.vcf > $OutDir/"$Prefix"_syn.vcf
      #Four-fold degenrate sites (output file suffix: 4fd)
      ProgDir=/home/sobczm/bin/popgen/summary_stats
      python $ProgDir/parse_snpeff_synonymous.py $OutDir/"$Prefix"_syn.vcf
  done
```


## Summarise SNP effects

```bash
AnnotaTable=$(ls gene_pred/annotation/P.cactorum/414_v2/414_v2_gene_table_incl_exp.tsv)
RxLR="gene_pred/annotation/P.cactorum/414_v2/renamed_RxLR.txt"
CRN=$(ls analysis/CRN_effectors/hmmer_CRN/P.cactorum/414_v2/414_v2_final_CRN_ID.txt)
cat $AnnotaTable | cut -f1,12 | tail -n+2 | grep 'Yes' | cut -f1 > $RxLR
cat $AnnotaTable | cut -f1,13 | tail -n+2 | grep 'Yes' | cut -f1 > $CRN

for Folder in $(ls -d analysis/popgen/SNP_calling/*_vs_P414); do
  Comparison=$(echo $Folder | rev | cut -f1 -d '/' | rev)
  AllSnps=$(cat $Folder/*_annotated.vcf | grep -v '#' | wc -l)
  GeneSnps=$(cat $Folder/*_no_indels.recode_gene.vcf | grep -v '#' | wc -l)
  CdsSnps=$(cat $Folder/*_no_indels.recode_coding.vcf | grep -v '#' | wc -l)
  NonsynSnps=$(cat $Folder/*_no_indels.recode_nonsyn.vcf | grep -v '#' | wc -l)
  SynSnps=$(cat $Folder/*_no_indels.recode_syn.vcf | grep -v '#' | wc -l)
  RxlrOut=$Folder/"$Comparison"_no_indels.recode_syn_RxLR.vcf
  cat $Folder/*_no_indels.recode_nonsyn.vcf | grep -f $RxLR > $RxlrOut
  RxlrNonSynSnps=$(cat $RxlrOut | wc -l)
  CrnOut=$Folder/"$Comparison"_no_indels.recode_syn_CRN.vcf
  cat $Folder/*_no_indels.recode_nonsyn.vcf | grep -f $CRN > $CrnOut
  CrnNonSynSnps=$(cat $CrnOut | wc -l)
  printf "$Comparison\t$AllSnps\t$GeneSnps\t$CdsSnps\t$NonsynSnps\t$SynSnps\t$RxlrNonSynSnps\t$CrnNonSynSnps\n"
done
```

```
P414_vs_P414	875976	2893	2624	1389	1235	30	1
Pc_apple_vs_P414	174273	41621	37118	21284	15834	128	107
Pc_strawberry_vs_P414	118237	4561	4121	2278	1843	32	5
Pi_vs_P414	699603	317567	283950	154884	129066	936	795
```