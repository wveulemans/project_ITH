#! /usr/bin/python
import os
import csv
import glob
import shutil
from pysam import VariantFile
import vcf
import time

start_time = time.time()

##upper --> all lower case
def to_lower(short):
	f = open(short, 'rw+')
	lines = [line.lower() for line in f]

	with open(short, 'w') as out:
     		out.writelines(lines)
	f.close()


##change path to correct one
def changepath(short1):
	tsv = open(short1, 'rw+')
	replaced = [row.replace("/home/shared_data_core/ith_nele_bams/","/home/shared_data_core/COLON/ITH_nele_VCFs_amplicon_filter/VCF_filter1/") for row in tsv]
	
	with open(short1, 'w') as out:
     		out.writelines(replaced)
	tsv.close()


##mkdir per patient
def sample_names(short2):
	result=[]

	sample = open(short2, 'r')
	next(sample)

	for line in sample:
		parts = line.split()		
		if len(parts) > 0:   		
		    result.append(parts[4])	# print column 4

	#print result
	names = []

	for name in result:
		names.append(name.split('_',2)[2])

	#print names
	return names


##make patientdirectory
def makedir(names):
	PATH = '/home/shared_data_core/COLON/subclonality/'

	for name in names:
		if not os.path.exists(os.path.join(PATH,name)):
			os.mkdir(os.path.join(PATH,name))
			print "Directory: %s is created!"% name
		else:
			print "Directory: %s already exist!"% name


##move .vcf files to patientdirectory
def copyfile_VCF(names):
	for name in names:
		source = glob.glob('/home/shared_data_core/COLON/ITH_nele_VCFs_amplicon_filter/VCF_filter1/*%s/*.vcf'% name)
		destination = '/home/shared_data_core/COLON/subclonality/%s/'% name		
		for files in source:
			if  files.endswith('.vcf'):
				#if not os.path.isfiles('/home/shared_data_core/COLON/subclonality/%s/')):
				shutil.copy2(os.path.abspath(files),destination)
		print "All VCF's copied for %s!"% name
	

				

##move .bam and .bai files to patientdirectory
def copyfile_BAM(names):
	for name in names:
		BAMS = glob.glob('/home/shared_data_core/COLON/ITH_nele_BAMs/*%s*.bam'%name)
		BAIS = glob.glob('/home/shared_data_core/COLON/ITH_nele_BAMs/*%s*.bam.bai'%name)	
		#print BAMS, '\n'
		#print BAIS, '\n'
		destination = '/home/shared_data_core/COLON/subclonality/%s/'% name
		for BAM in BAMS:
			if BAM.endswith('.bam'):
				shutil.copy2(os.path.abspath(BAM),destination)
		print "All BAM's copied for %s!"% name
		
		for BAI in BAIS:
			if BAI.endswith('.bai'):
				shutil.copy2(os.path.abspath(BAI),destination)
		print "All BAI's copied for %s!"% name


##prepare .tsv file for PyClone
def prep_tsv(txt):
	vcf_reader = VariantFile(txt, 'r'))
	
	# add header to outfile
	tsv_out = open('pyclone_name.tsv','w+')
	file_writer = csv.writer(tsv_out, delimiter='\t')
	file_writer.writerow(['mutation_id','ref_counts','var_counts','normal_cn','minor_cn','major_cn','variant_case','variant_freq','genotype'])


	#record = next(vcf_reader)
	
	mutation_id = []
	ref_counts = []
	var_counts = []
	normal_cn = []
	minor_cn = []
	major_cn = []
	variant_case = []
	variant_freq = []
	genotype = []
	for record in vcf_reader:
		print record
##controllable
def main():
	text_file = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'

	to_lower(text_file)
	changepath(text_file)
	names = sample_names(text_file)
	makedir(names)
	#copyfile_VCF(names)
	#copyfile_BAM(names)
	prep_tsv('/home/shared_data_core/COLON/subclonality/a_1_3_pt/ith_run3_a_1_3_pt_filter1_indel.vcf')
	

if __name__ == "__main__":
	main()

print("--- %s seconds ---" % (time.time() - start_time))
