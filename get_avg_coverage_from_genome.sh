#!/bin/bash

# activate mamba env that contains samtools, seqkit and bowtie2 first using
# mamba activate /vol/local/conda_envs/mapping/

mkdir -p bowtie2_indexes
mkdir -p SAM_outputs
mkdir -p BAM_outputs

MAX_JOBS=3
counter=0

dir_reads="PUT YOUR DIR HERE"

printf "BAM_FILE\tASSEMBLY_FILE\tAVERAGE_COVERAGE\n" > average_coverages.tsv

cat list_genomes_to_map | while read line; do

	metagenome=$(echo $line | cut -d" " -f1)
	assembly=$(echo $line | cut -d" " -f2)

	mkdir -p bowtie2_indexes/$assembly

	process_genome() {

		bowtie2-build -f --seed 108 --threads 16 \
		$assembly.fna bowtie2_indexes/$assembly/$assembly

		bowtie2 -p 16 -x bowtie2_indexes/$assembly/$assembly \
		-1 $dir_reads/${metagenome}_R1_ok.fq.gz \
		-2 $dir_reads/${metagenome}_R2_ok.fq.gz \
		-U $dir_reads/${metagenome}_R_unpaired_ok.fq.gz \
		--local -S SAM_outputs/$assembly.sam

		samtools view -bS SAM_outputs/$assembly.sam | samtools sort -o BAM_outputs/$assembly.sorted.bam
		pigz -p 16 SAM_outputs/$assembly.sam

		#Calculating the coverage and putting it into the table 
		samtools depth "BAM_outputs/$assembly.sorted.bam" > coverage.tmp
		GENOME_SIZE=$(seqkit stats "$assembly.fna" | awk 'NR>1 {print $5}' | sed 's/,//g')
		TOTAL_COVERAGE=$(awk '{sum += $3} END {print sum}' coverage.tmp)
		AVERAGE_COVERAGE=$(echo "$TOTAL_COVERAGE / $GENOME_SIZE" | bc -l)
		printf "%s\t%s\t%s\n" "$assembly.sorted.bam" "$assembly.fna" "$AVERAGE_COVERAGE" >> average_coverages.tsv
	}

	process_genome &

	((counter++))


	#This part makes sure that there are always 3 job running at the same time
	if [[ $counter -ge $MAX_JOBS ]]; then
		wait -n
		((counter--))
	fi

rm coverage.tmp

done