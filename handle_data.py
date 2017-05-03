#! /usr/bin/python
import os
import csv
import glob
import shutil
import vcf
import time
import logging
from collections import OrderedDict as OD

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
def makedir(name):
	PATH = '/home/shared_data_core/COLON/subclonality/'
	if not os.path.exists(os.path.join(PATH,name)):
		os.mkdir(os.path.join(PATH,name))
		print "Directory: %s is created!"% name
	else:
		print "Directory: %s already exist!"% name


##copy .vcf files to patientdirectory
def copyfile_VCF_TXT(name):
	source = glob.glob('/home/shared_data_core/COLON/ITH_nele_VCFs_amplicon_filter/VCF_filter1/*%s/*.vcf'% name)
	#print source
	destination = '/home/shared_data_core/COLON/subclonality/%s/'% name		
	#print destination	
	for files in source:
		if  files.endswith('.vcf'):
			#if not os.path.isfiles('/home/shared_data_core/COLON/subclonality/%s/')):
			shutil.copy2(os.path.abspath(files),destination)
	print "All VCF's copied for %s!"% name
	
	
	source1 = glob.glob('/home/shared_data_core/COLON/subclonality/CNV/*%s*.txt'% name)		#be carefull with glob.glob, elements in list!
	#print source1
	destination1 = '/home/shared_data_core/COLON/subclonality/%s/'% name
	#print destination1
	
	global cnv_file	
	cnv_file = 0

	try:		
		shutil.copy2(os.path.abspath(source1[0]),os.path.abspath(destination1))
		print "Transferring CNV file"
		cnv_file = 1

	except IndexError, e:
		print "No CNV file. %s" % e
		cnv_file = 0

	#print cnv_file 
	return cnv_file
		
				

##move .bam and .bai files to patientdirectory
def copyfile_BAM(name):
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
def prep_tsv(name):

	source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/*.vcf'% name)
		
	for files in source:
		parts = []			
		parts = files.split("/")[6]
		
		vcf_reader = vcf.Reader(open('%s'% files, 'r'))
		#print vcf_reader
		#add header to outfile
		tsv_out = open('/home/shared_data_core/COLON/subclonality/%s/pyclone_%s.tsv'% (name,parts),'w+')
		file_writer = csv.writer(tsv_out, delimiter='\t')
		file_writer.writerow(['mutation_id','ref_counts','var_counts','normal_cn','minor_cn','major_cn','variant_case','variant_freq','genotype'])

		variant_info = OD({

			'mutation_id': {'chr': str(), 'pos':int(), 'name':str()}, 
			'ref_counts': int(), 
			'var_counts': int(),
			'normal_cn': int(),
			'minor_cn': int(),
			'major_cn': int(), 
			'variant_case': str(name),
			'variant_freq': float(),
			'genotype': str(),
			'gene_id': str()
		})
		variant_number = 0
		return variant_info

def read_vcf(variant_info):
		for record in vcf_reader:
			print variant_number
			variant_info[variant_number]['mutation_id']['chr'] = record.CHROM
			variant_info['mutation_id']['pos'] = record.POS
			variant_info['mutation_id']['name'] = name
			#print variant_info['mutation_id']['pos']
			
			variant_info['ref_counts'] = record.samples[1]['RD']
			variant_info['var_counts'] = record.samples[1]['AD']
			#print variant_info['ref_counts']
			#print variant_info['var_counts']

			variant_info['normal_cn'] = int('2')
			#print variant_info['normal_cn']
			
			binary_GT = record.samples[1]['GT'].replace('|', '/').split('/')
			#print binary_GT
			if binary_GT[0] != binary_GT[1]:
				variant_info['genotype'] = str('AB')
			if binary_GT[0] == binary_GT[1]:
				variant_info['genotype'] = str('BB')
			#print variant_info['genotype']
			variant_number =+ 1
			return variant_info

def read_cnv(cnv_file):
		if cnv_file == 'test':
			#source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/*.vcf'% name)
			#print source
			os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
			present = open('X.home.shared_data_core.ITH_Nele.ith_analysis_ploidy2.Results.ith_run3_%s.ith_run3_%s.real.recal.summary.txt'% (name,name), 'r')
			next(present) #skip header
		
			range_pos = OD({
				'gene': str(),
				'begin': int(),
				'end': int()
			})			
		
			for line in present:
				range_pos['gene'] = line.split('\t')[0]
				range_pos['begin'] = line.split('\t')[2]
				range_pos['end'] = line.split('\t')[3]
				#print range_pos['gene']
				print range_pos['begin']
				if range_pos['begin'] < variant_info['mutation_id']['pos'] < range_pos['end']:			
					print "mutation lies in gene"			
		#print variant_info['mutation_id']['pos']

#def compare_cnv():
						

##controllable
def main():
	text_file = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'

	to_lower(text_file)
	changepath(text_file)
	names = sample_names(text_file)
	
	for name in names:
		makedir(name)
		copyfile_VCF_TXT(name)
		#copyfile_BAM(name)
		prep_tsv(name, cnv_file)
		read_vcf
		read_cnv
		compare_cnv

	

	

if __name__ == "__main__":
	main()

print("--- %s seconds ---" % (time.time() - start_time))
