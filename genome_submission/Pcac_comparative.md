# Submission Commands

Submisison of annotations with an assembly appears to be a complex process.
If a genome is to be submitted without annotation then all that is needed is the
fasta file containing the assembled contigs. If an annotated genome is to be
submitted then a number of processing steps are required before submission. The
fasta file of contigs and the gff file of annotations must be combined to form a
.asn file. The program that does this conversion (tbl2asn) requires the fasta
files and gff files to be formatted correctly. In the case of the gff file, this
means parsing it to a .tbl file.

The commands used to parse these files and prepare the F. oxysporum f. sp.
cepae genome for submisson are shown below.


# SRA archive

A Bioproject and biosample number was prepared for the genome submission at:
https://submit.ncbi.nlm.nih.gov
Following this a metadata file was created for the dataset. This was copied
into the following folder:

```bash
mkdir -p genome_submission/P.cac_comparative
ls genome_submission/P.cac_comparative/Pc_Pi_SRA_metadata_acc.txt
```

read data was copied to this location in preperation for submission to ncbi:

```bash
screen -a
OutDir=/data/scratch/armita/idris/genome_submission/P.cac_comparative/SRA
mkdir -p $OutDir
for File in $(ls raw_dna/paired/P.cactorum/*/*/*.fastq.gz | grep -v '414'); do
 cp $File $OutDir/.
done
for File in $(ls raw_dna/paired/P.idaei/*/*/*.fastq.gz); do
 cp $File $OutDir/.
done
cd /data/scratch/armita/idris/genome_submission/P.cac_comparative
tar -cz -f Pc_SRA.tar.gz SRA
```

FTP upload of data

```bash
cd /data/scratch/armita/idris/genome_submission/P.cac_comparative
ftp ftp-private.ncbi.nlm.nih.gov
# User is: subftp
# Password is given in the FTP upload instrucitons during SRA submission
cd uploads/andrew.armitage@emr.ac.uk_6L2oakBI
mkdir Pcac_comparative_PRJNA391273
cd Pcac_comparative_PRJNA391273
put Pc_SRA.tar.gz
```


# Preliminary submission

A Bioproject and biosample number was prepared for the genome submission at:
https://submit.ncbi.nlm.nih.gov

A preliminary submission was made for the .fasta assembly to check if
any contigs needed to be split. This step was performed early in the annotation
process (prior to gene prediction) to ensure that annotation did not have to
be repeated at the end of the project.


The following note was provided in the WGS submission page on NCBI in the box
labeled "Private comments to NCBI staff":

```
I have been advised to submit my assemblies to NCBI early in my submission process to ensure that my contigs pass the contamination screen. This assembly will be revised as appropriate, including renaming of contigs where needed. Please allow me to modify this submission at a later date, including upload of the final gene models.

'For future submissions, you could send us the fasta files early
in the submission process so we can run them through our foreign
contamination screen. We will let you know if we find any
sequences to exclude or trim before you generate your final
WGS submission.'...'*IMPORTANT* Include a comment that you are submitting
the fasta files to be screened by the contamination screen
prior to creating your final annotated submission.'
```

<!--
# Submission of sequence data to SRA

Reads were submitted to the SRA at https://submit.ncbi.nlm.nih.gov/subs/sra/ .
To do this, a metadata file was provided detailing each of the files in the
bioproject. The file was downloaded in excel format and edited manually. A copy
of the edited file and the final .tsv file is present at:

```bash
  # For genmic reads:
  ls genome_submission/SRA_metadata_acc.txt genome_submission/SRA_metadata_acc.xlsx
  # For RNAseq reads:
  ls genome_submission/SRA_metadata_acc.txt genome_submission/RNAseq_SRA_metadata_acc.txt
```

As these files included a file > 500 Mb, a presubmission folder was requested.
This aids submission of large data files. This file was created on the ftp server
at ftp-private.ncbi.nlm.nih.gov, with a private folder named
uploads/andrew.armitage@emr.ac.uk_6L2oakBI. Ncbi provided a username a password.
Files were uploaded into a folder created within my preload folder using ftp.

For genomic reads:
```bash
  # Bioproject="PRJNA338236"
  SubFolder="FoC_PRJNA338256"
  mkdir $SubFolder
  for Read in $(ls raw_dna/paired/F.*/*/*/*.fastq.gz | grep -w -e '125' -e 'A23' -e 'A13' -e 'A28' -e 'CB3' -e 'PG' -e 'A8' -e 'Fus2' | grep -v s_6_*_sequence.fastq.gz); do
    echo $Read;
    cp $Read $SubFolder/.
  done
  cp raw_dna/pacbio/F.oxysporum_fsp_cepae/Fus2/extracted/concatenated_pacbio.fastq $SubFolder/.
  cd $SubFolder
  gzip concatenated_pacbio.fastq
  ftp ftp-private.ncbi.nlm.nih.gov
  cd uploads/andrew.armitage@emr.ac.uk_6L2oakBI
  mkdir FoC_PRJNA338256_2
  cd FoC_PRJNA338256_2
  # put FoN_PRJNA338236
  prompt
  mput *
  bye
  cd ../
  rm -r $SubFolder
```

For RNAseq Reads:
```bash
  SubFolder="FoC_RNAseq_PRJNA338256"
  mkdir $SubFolder
  for Read in $(ls qc_rna/paired/F.*/*/*/*_trim.fq.gz); do
    echo $Read;
    cp $Read $SubFolder/.
  done
  cd $SubFolder
  ftp ftp-private.ncbi.nlm.nih.gov
  cd uploads/andrew.armitage@emr.ac.uk_6L2oakBI
  mkdir FoC_RNAseq_PRJNA338256
  cd FoC_RNAseq_PRJNA338256
  prompt
  mput *
  bye
  cd ../
  rm -r $SubFolder
``` -->

## Making a table for locus tags:

locus tags were provided by ncbi when the bioproject was registered.

A table detailing their relationship to the strain was made manually. This could
be searched later to extract locus tags for particular strains.

```bash
mkdir -p genome_submission/
printf \
"PC111 SAMN07267854 12420
PC112 SAMN07267855 15_13
PC113 SAMN07267856 15_7
PC114 SAMN07267857 2003_3
PC115 SAMN07267858 4032
PC116 SAMN07267859 404
PC117 SAMN07267860 4040
PC118 SAMN07267861 415
PC119 SAMN07267862 416
PC120 SAMN07267863 62471
PC121 SAMN07267864 P295
PC122 SAMN07267865 PC13_15
PC123 SAMN07267866 R36_14
PI124 SAMN07267867 371
PI125 SAMN07267868 SCRP370
PI126 SAMN07267869 SCRP376
PC127 SAMN08638078 11-40
PC128 SAMN08638079 17-21
PC129 SAMN08638080 P421
" \
> genome_submission/Pcac_PRJNA391273_locus_tags.txt
```

# Final Submission

These commands were used in the final submission of the Pcac genomes:


## Output directory
An output and working directory was made for genome submission:

```bash
for Assembly in $(ls repeat_masked/P.*/*/filtered_contigs_repmask/*_contigs_unmasked.fa | grep -e 'P.cactorum' -e 'P.idaei' | grep -v -e '414' -e '10300' -e 'D-1' | grep -v '11-40' | grep -v 'D-1'); do
  Organism=$(echo $Assembly | rev | cut -d '/' -f4 | rev)
  Strain=$(echo $Assembly | rev | cut -d '/' -f3 | rev | sed 's/_v2//g')
  echo "$Organism - $Strain"
  ProjDir=/home/groups/harrisonlab/project_files/idris
  cd $ProjDir
  OutDir="genome_submission/$Organism/$Strain"
  mkdir -p $OutDir
done
```

## SbtFile
The genbank submission template tool was used at:
http://www.ncbi.nlm.nih.gov/WebSub/template.cgi
This produce a template file detailing the submission.

## Setting varibales
Vairables containing locations of files and options for scripts were set:

```bash
# Program locations:
AnnieDir="/home/armita/prog/annie/genomeannotation-annie-c1e848b"
ProgDir="/home/armita/git_repos/emr_repos/tools/genbank_submission"
# File locations:
SbtFile=$(ls /home/groups/harrisonlab/project_files/idris/genome_submission/P.cactorum/414_v2/template.sbt)
LabID="ArmitageEMR"
```

## Generating .tbl file (GAG)

The Genome Annotation Generator (GAG.py) can be used to convert gff files into
.tbl format, for use by tbl2asn.

It can also add annotations to features as provided by Annie the Annotation
extractor.

### Extracting annotations (Annie)

Interproscan and Swissprot annotations were extracted using annie, the
ANNotation Information Extractor. The output of Annie was filtered to
keep only annotations with references to ncbi approved databases.
Note - It is important that transcripts have been re-labelled as mRNA by this
point.

```bash
export PYTHONPATH="/home/armita/.local/lib/python3.5/site-packages"
for Assembly in $(ls repeat_masked/P.*/*/filtered_contigs_repmask/*_contigs_unmasked.fa | grep -e 'P.cactorum' -e 'P.idaei' | grep -v -e '414' -e '10300' -e 'D-1' | grep -v '11-40' | grep -w '4032'); do
  Organism=$(echo $Assembly | rev | cut -d '/' -f4 | rev)
  Strain=$(echo $Assembly| rev | cut -d '/' -f3 | rev | sed 's/_v2//g')
  echo "$Organism - $Strain"
  OutDir="genome_submission/$Organism/$Strain"
  GffFile=$(ls gene_pred/final_incl_ORF/$Organism/"$Strain"/final_genes_genes_incl_ORFeffectors_renamed.gff3)

  InterProTab=$(ls gene_pred/interproscan/$Organism/"$Strain"/"$Strain"_interproscan.tsv)
  SwissProtBlast=$(ls gene_pred/swissprot/$Organism/"$Strain"/swissprot_vMar2018_tophit_parsed.tbl)
  SwissProtFasta=$(ls /home/groups/harrisonlab/uniprot/swissprot/uniprot_sprot.fasta)
  python3 $AnnieDir/annie.py -ipr $InterProTab -g $GffFile -b $SwissProtBlast -db $SwissProtFasta -o $OutDir/annie_output.csv --fix_bad_products
  ProgDir=/home/armita/git_repos/emr_repos/tools/genbank_submission
  $ProgDir/edit_tbl_file/annie_corrector.py --inp_csv $OutDir/annie_output.csv --out_csv $OutDir/annie_corrected_output.csv
done
```

### Running GAG

Gag was run using the modified gff file as well as the annie annotation file.
Gag was noted to output database references incorrectly, so these were modified.

```bash
for Assembly in $(ls repeat_masked/P.*/*/filtered_contigs_repmask/*_contigs_unmasked.fa | grep -e 'P.cactorum' -e 'P.idaei' | grep -v -e '414' -e '10300' -e 'D-1' | grep -w '404'); do
Organism=$(echo $Assembly | rev | cut -d '/' -f4 | rev)
Strain=$(echo $Assembly| rev | cut -d '/' -f3 | rev | sed 's/_v2//g')
echo "$Organism - $Strain"
OutDir="genome_submission/$Organism/$Strain"
# GffFile=$(ls gene_pred/final_incl_ORF/$Organism/"$Strain"/final_genes_genes_incl_ORFeffectors_renamed.gff3)
GffFile=$(ls gene_pred/final_incl_ORF/$Organism/"$Strain"/final_genes_genes_incl_ORFeffectors_renamed_corrected.gff3)
mkdir -p $OutDir/gag/round1
gag.py -f $Assembly -g $GffFile -a $OutDir/annie_corrected_output.csv --fix_start_stop -o $OutDir/gag/round1 2>&1 | tee $OutDir/gag_log1.txt
sed -i 's/Dbxref/db_xref/g' $OutDir/gag/round1/genome.tbl
done
```

<!-- ## manual edits

The gene NS_04463 was found to use the same start and stop codon as predicted
gene CUFF_4598_1_205. Both of these genes were predicted by codingquary. Neither
of these genes were predicted as having alternative splicing. As such the gene
NS_04463 was removed. The same was found for genes CUFF_11067_2_85 and
CUFF_11065_1_82 and as a result CUFF_11067_2_85 was removed.

```bash
  nano $OutDir/gag/round1/genome.tbl
``` -->

## tbl2asn round 1

tbl2asn was run an initial time to collect error reports on the current
formatting of the .tbl file.
Note - all input files for tbl2asn need to be in the same directory and have the
same basename.

```bash
for Assembly in $(ls repeat_masked/P.*/*/filtered_contigs_repmask/*_contigs_unmasked.fa | grep -e 'P.cactorum' -e 'P.idaei' | grep -v -e '414' -e '10300' | grep -v '11-40' | grep -v 'D-1' | grep -w '404'); do
Organism=$(echo $Assembly | rev | cut -d '/' -f4 | rev)
Strain=$(echo $Assembly| rev | cut -d '/' -f3 | rev | sed 's/_v2//g')
echo "$Organism - $Strain"
OrganismSbt=$(echo $Organism | sed 's/P./Phytophthora /g')
OutDir="genome_submission/$Organism/$Strain"

cp $Assembly $OutDir/gag/round1/genome.fsa
SbtFile=$(ls /home/groups/harrisonlab/project_files/idris/genome_submission/P.cactorum/414_v2/template.sbt)
SRA_metadata=$(ls genome_submission/Pcac_PRJNA391273_locus_tags.txt)
BioSample=$(cat $SRA_metadata | grep "$Strain" | cut -f2 -d ' ' | head -n1)
SRA_metadata=$(ls genome_submission/Pcac_PRJNA391273_locus_tags.txt)
cat $SbtFile | sed 's/PRJNA383548//g'| sed "s/SAMN06766401/$BioSample/g" > $OutDir/gag/round1/genome.sbt
mkdir -p $OutDir/tbl2asn/round1
tbl2asn -p $OutDir/gag/round1/. -t $OutDir/gag/round1/genome.sbt -r $OutDir/tbl2asn/round1 -M n -X E -Z $OutDir/gag/round1/discrep.txt -j "[organism=$OrganismSbt] [strain=$Strain]"
done
```

## Editing .tbl file

The tbl2asn .val output files were observed and errors corrected. This was done
with an in house script. The .val file indicated that some cds had premature
stops, so these were marked as pseudogenes ('pseudo' - SEQ_FEAT.InternalStop)
and that some genes had cds coordinates that did not match the end of the gene
if the protein was hanging off a contig ('stop' - SEQ_FEAT.NoStop).
Furthermore a number of other edits were made to bring the .tbl file in line
with ncbi guidelines. This included: Marking the source of gene
predictions and annotations ('add_inference'); Correcting locus_tags to use the
given ncbi_id ('locus_tag'); Correcting the protein and transcript_ids to
include the locus_tag and reference to submitter/lab id ('lab_id'), removal of
annotated names of genes if you don't have high confidence in their validity
(--gene_id 'remove'). If 5'-UTR and 3'-UTR were not predicted during gene
annotation then genes, mRNA and exon features need to reflect this by marking
them as incomplete ('unknown_UTR').

```bash
for Assembly in $(ls repeat_masked/P.*/*/filtered_contigs_repmask/*_contigs_unmasked.fa | grep -e 'P.cactorum' -e 'P.idaei' | grep -v -e '414' -e '10300' | grep -v '11-40' | grep -v 'D-1'); do
Organism=$(echo $Assembly | rev | cut -d '/' -f4 | rev)
Strain=$(echo $Assembly| rev | cut -d '/' -f3 | rev | sed 's/_v2//g')
echo "$Organism - $Strain"
OutDir="genome_submission/$Organism/$Strain"
LocusTag=$(cat genome_submission/Pcac_PRJNA391273_locus_tags.txt | grep -w "$Strain" | cut -f1 -d ' ')
echo $LocusTag
mkdir -p $OutDir/gag/edited
ProgDir=/home/armita/git_repos/emr_repos/tools/genbank_submission
$ProgDir/edit_tbl_file/ncbi_tbl_corrector.py --inp_tbl $OutDir/gag/round1/genome.tbl --inp_val $OutDir/tbl2asn/round1/genome.val --locus_tag $LocusTag --lab_id $LabID --gene_id "remove" --edits stop pseudo unknown_UTR correct_partial --remove_product_locus_tags "True" --del_name_from_prod "True" --out_tbl $OutDir/gag/edited/genome.tbl
done > log.txt
```


## Generating a structured comment detailing annotation methods

```bash
  for Assembly in $(ls repeat_masked/P.*/*/filtered_contigs_repmask/*_contigs_unmasked.fa | grep -e 'P.cactorum' -e 'P.idaei' | grep -v -e '414' -e '10300' | grep -v '11-40' | grep -v 'D-1' | grep -w '4032'); do
    Organism=$(echo $Assembly | rev | cut -d '/' -f4 | rev)
    Strain=$(echo $Assembly| rev | cut -d '/' -f3 | rev | sed 's/_v2//g')
    echo "$Organism - $Strain"
    OutDir="genome_submission/$Organism/$Strain"
    printf "StructuredCommentPrefix\t##Genome-Annotation-Data-START##
    Annotation Provider\tHarrison Lab NIAB-EMR
    Annotation Date\tAUG-2017
    Annotation Version\tRelease 1.01
    Annotation Method\tAb initio gene prediction: Braker 1.9 and CodingQuary 2.0; Functional annotation: Swissprot (March 2018 release) and Interproscan 5.18-57.0" \
    > $OutDir/gag/edited/annotation_methods.strcmt.txt
  done
```

## Final run of tbl2asn

Following correction of the GAG .tbl file, tbl2asn was re-run to provide the
final genbank submission file.

The options -l paired-ends -a r10k inform how to handle runs of Ns in the
sequence, these options show that paired-ends have been used to estimate gaps
and that runs of N's longer than 10 bp should be labelled as gaps.

```bash
for Assembly in $(ls repeat_masked/P.*/*/filtered_contigs_repmask/*_contigs_unmasked.fa | grep -e 'P.cactorum' -e 'P.idaei' | grep -v -e '414' -e '10300' | grep -v '11-40' | grep -v 'D-1'); do
  Strain=$(echo $Assembly| rev | cut -d '/' -f3 | rev | sed 's/_v2//g')
  Organism=$(echo $Assembly | rev | cut -d '/' -f4 | rev)
  echo "$Organism - $Strain"
  OutDir="genome_submission/$Organism/$Strain"
  FinalName="$Organism"_"$Strain"_Armitage_2017
  cp $Assembly $OutDir/gag/edited/genome.fsa
  # SbtFile=$(ls /home/groups/harrisonlab/project_files/idris/genome_submission/P.cactorum/414_v2/template.sbt)
  # SRA_metadata=$(ls genome_submission/Pcac_PRJNA391273_locus_tags.txt)
  # BioSample=$(cat $SRA_metadata | grep -w "$Strain" | cut -f2 -d ' ' | head -n1)
  # cat $SbtFile | sed "s/SAMN06766401/$BioSample/g" > $OutDir/gag/edited/genome.sbt
  cp $OutDir/gag/round1/genome.sbt $OutDir/gag/edited/genome.sbt
  mkdir $OutDir/tbl2asn/final
  tbl2asn -p $OutDir/gag/edited/. -t $OutDir/gag/edited/genome.sbt -r $OutDir/tbl2asn/final -M n -X E -Z $OutDir/tbl2asn/final/discrep.txt -j "[organism=$Organism] [strain=$Strain]" -l paired-ends -a r10k -w $OutDir/gag/edited/annotation_methods.strcmt.txt
  cat $OutDir/tbl2asn/final/genome.sqn | sed 's/_pilon//g' | sed "s/Saccharopine dehydrogenase \[NAD\S*\w/Saccharopine dehydrogenase/g" | sed 's/aldolase_/aldolase/g' > $OutDir/tbl2asn/final/$FinalName.sqn
  ls $PWD/$OutDir/tbl2asn/final/$FinalName.sqn
done
```

```bash
mkdir -p genome_submission/for_transfer
for Sqn in $(ls genome_submission/*/*/tbl2asn/final/*_Armitage_2017.sqn | grep -v -e '11-40' -e '10300'); do
SubName=$(basename $Sqn .sqn)
echo $SubName
# mkdir -p genome_submission/for_transfer/$SubName
# cp $Sqn genome_submission/for_transfer/$SubName/.
cp $Sqn genome_submission/for_transfer/.
done
# cd genome_submission/for_transfer
# tar -cz -f submissions_Armitage_2017.tar.gz *_Armitage_2017
```

```bash
cd genome_submission/for_transfer
ftp ftp-private.ncbi.nlm.nih.gov
cd uploads/andrew.armitage@emr.ac.uk_6L2oakBI
mkdir P.cactorum_4032_Armitage_2017
cd P.cactorum_4032_Armitage_2017
put P.cactorum_4032_Armitage_2017.sqn
cd ../
#
# mkdir P.cactorum_P421_Armitage_2017
# cd P.cactorum_P421_Armitage_2017
# put P.cactorum_P421_Armitage_2017.sqn
# cd ../
#
# mkdir P.cactorum_11-40_Armitage_2017
# cd P.cactorum_11-40_Armitage_2017
# put P.cactorum_11-40_Armitage_2017.sqn
# cd ../

mkdir P.cactorum_4040_Armitage_2017
cd P.cactorum_4040_Armitage_2017
put P.cactorum_4040_Armitage_2017.sqn
cd ../

mkdir P.cactorum_PC13_15_Armitage_2017
cd P.cactorum_PC13_15_Armitage_2017
put P.cactorum_PC13_15_Armitage_2017.sqn
cd ../

mkdir P.cactorum_12420_Armitage_2017
cd P.cactorum_12420_Armitage_2017
put P.cactorum_12420_Armitage_2017.sqn
cd ../

mkdir P.cactorum_404_Armitage_2017
cd P.cactorum_404_Armitage_2017
put P.cactorum_404_Armitage_2017.sqn
cd ../

mkdir P.cactorum_R36_14_Armitage_2017
cd P.cactorum_R36_14_Armitage_2017
put P.cactorum_R36_14_Armitage_2017.sqn
cd ../

mkdir P.cactorum_15_13_Armitage_2017
cd P.cactorum_15_13_Armitage_2017
put P.cactorum_15_13_Armitage_2017.sqn
cd ../

mkdir P.cactorum_415_Armitage_2017
cd P.cactorum_415_Armitage_2017
put P.cactorum_415_Armitage_2017.sqn
cd ../

mkdir P.idaei_371_Armitage_2017
cd P.idaei_371_Armitage_2017
put P.idaei_371_Armitage_2017.sqn
cd ../

mkdir P.cactorum_15_7_Armitage_2017
cd P.cactorum_15_7_Armitage_2017
put P.cactorum_15_7_Armitage_2017.sqn
cd ../

mkdir P.cactorum_416_Armitage_2017
cd P.cactorum_416_Armitage_2017
put P.cactorum_416_Armitage_2017.sqn
cd ../
#
# mkdir P.idaei_SCRP370_Armitage_2017
# cd P.idaei_SCRP370_Armitage_2017
# put P.idaei_SCRP370_Armitage_2017.sqn
# cd ../

mkdir P.cactorum_17-21_Armitage_2017
cd P.cactorum_17-21_Armitage_2017
put P.cactorum_17-21_Armitage_2017.sqn
cd ../

mkdir P.cactorum_62471_Armitage_2017
cd P.cactorum_62471_Armitage_2017
put P.cactorum_62471_Armitage_2017.sqn
cd ../

mkdir P.idaei_SCRP376_Armitage_2017
cd P.idaei_SCRP376_Armitage_2017
put P.idaei_SCRP376_Armitage_2017.sqn
cd ../

mkdir P.cactorum_2003_3_Armitage_2017
cd P.cactorum_2003_3_Armitage_2017
put P.cactorum_2003_3_Armitage_2017.sqn
cd ../
#
# mkdir P.cactorum_P295_Armitage_2017
# cd P.cactorum_P295_Armitage_2017
# put P.cactorum_P295_Armitage_2017.sqn
# cd ../
```

Commands to generate discrepancy files in the format they’ll see at NCBI, will label fatal errors etc.

Add this line to profile to use asndisc

```bash
PATH=${PATH}:/home/adamst/prog/ncbi_asndisc

for sqn_dir in $(ls -d genome_submission/P.*/*/tbl2asn/final | grep '11-40')
do
  # Sqn=$(basename $sqn_dir/*Armitage_2017.sqn)
    asndisc -p $sqn_dir -x Armitage_2017.sqn -o $sqn_dir/discrep.val -X ALL -P t
done
```



# Edit Gff to remove genes predicted by CodingQuary to start beyond the end of a contig.

```bash
for InpGff in $(ls gene_pred/final_incl_ORF/*/*/final_genes_genes_incl_ORFeffectors_renamed.gff3); do
Organism=$(echo $InpGff | rev | cut -d '/' -f3 | rev)
Strain=$(echo $InpGff| rev | cut -d '/' -f2 | rev )
echo "$Organism - $Strain"
Assembly=$(ls repeat_masked/$Organism/$Strain/filtered_contigs_repmask/${Strain}_contigs_unmasked.fa)
# OutDir=$(dirname $Assembly)
OutFile=$(echo $InpGff | sed 's/.gff3/_corrected.gff3/g')
ProgDir=/home/armita/git_repos/emr_repos/tools/gene_prediction/codingquary
$ProgDir/correct_genes_beyond_contigs.py --inp_gff $InpGff --inp_fasta $Assembly > $OutFile
done

```
