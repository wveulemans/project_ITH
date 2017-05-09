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


##add gender to file
def add_gender(short2, text_file):
	r = open(short2, 'rb')
	w = open(text_file, 'rw+')
	
    	reader = csv.reader(r, delimiter=',')

	patient_info = OD({
			'id': str(),
			'sex': str()
			})    	
	next(reader)
	for row in reader:
		if not row[0] == '':
			patient_info['id'] = row[0]
			patient_info['sex'] = row[6]
			print patient_info

		
		for line in w:
			sample = line.split()
			ids = sample[0].split('_')
			print ids[2]
		if ids[2] == patient_info['id']:
			w.write(line.rstrip('\n')+'\t'+patient_info['sex'])
		else:
			print 'Nothing found'


##mkdir per patient
def sample_names(short2):
	result=[]

	sample = open(short2, 'r')
	next(sample)

	for line in sample:
		parts = line.split()		
		if len(parts) > 0:   		
		    result.append(parts[4])	#print column 4

	#print result
	items = []

	for name in result:
		items.append(name.split('_')[2])

	
	names = ['_'+x+'_' for x in items]


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
def prep_tsv(name,files):
	parts = []			
	parts = files.split("/")[6]
	
	#add header to outfile
	file_writer = open('/home/shared_data_core/COLON/subclonality/%s/pyclone_%s.tsv'% (name,parts),'w+')
	file_writer.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')

	global variant_info
	variant_info = OD([
		('mutation_id', str()),
		('ref_counts', int()), 
		('var_counts', int()),
		('normal_cn', int()),
		('minor_cn', int()),
		('major_cn', str()), 
		('variant_case', str(name)),
		('variant_freq', float()),
		('genotype', str()),
		('nr', int()), 
		('chr', str()), 
		('pos', int())
	])
	return variant_info,file_writer

def read_vcf(variant_info,files,cnv_file,name,file_writer):
	variant_number = 0
	vcf_reader = vcf.Reader(open('%s'% files, 'r'))
	for record in vcf_reader:
		
		variant_info['nr'] = variant_number
		variant_info['chr'] = record.CHROM
		variant_info['pos'] = int(record.POS)
				
		variant_info['ref_counts'] = record.samples[1]['RD']
		variant_info['var_counts'] = record.samples[1]['AD']
		#print variant_info['ref_counts']
		#print variant_info['var_counts']
		if variant_info['chr'] == 'chrX' or variant_info['chr'] == 'chrY':			##ATTENTION: sex chromosomes have different copynumber!!!
			print 'sex chr!!!'
		else:
			variant_info['normal_cn'] = int('2')
		#print variant_info['normal_cn']
		variant_info['variant_freq'] = (1 - (float(record.samples[1]['RD'])/(record.samples[1]['RD'] + record.samples[1]['AD'])))
		#print variant_info['variant_freq']
		
		variant_info['minor_CN'] = 0
		#variant_info['major_CN'] = record.samples[4]

		binary_GT = record.samples[1]['GT'].replace('|', '/').split('/')
		#print binary_GT
		if binary_GT[0] != binary_GT[1]:
			variant_info['genotype'] = str('AB')
		if binary_GT[0] == binary_GT[1]:
			variant_info['genotype'] = str('BB')
		#print variant_info['genotype']
		variant_number += 1
		#print variant_info
		range_pos_all = list()	
		range_pos = dict()
		range_pos_all = read_cnv(cnv_file, name)
		compare(range_pos_all, variant_info, file_writer, name)
		
		

def read_cnv(cnv_file, name):
	range_pos_all = list()	
	range_pos = dict()
	if cnv_file == True:
		os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
		present = open('X.home.shared_data_core.ITH_Nele.ith_analysis_ploidy2.Results.ith_run3_%s.ith_run3_%s.real.recal.summary.txt'% (name,name), 'r')
		next(present) #skip header
			
		for line in present:
			range_pos = OD([
				('gene_id', str()),
				('chr', str()),
				('begin', int()),
				('end', int()),
				('cnv_state', str())
				])						
			range_pos['gene_id'] = str(line.split('\t')[0])
			range_pos['chr'] = str(line.split('\t')[1])
			range_pos['begin'] = int(line.split('\t')[2])
			range_pos['end'] = int(line.split('\t')[3])
			range_pos['cnv_state'] = str(line.split('\t')[4])
			if range_pos['cnv_state'] == '55':
				print 'SHITTTT', line, present
			range_pos_all.append(range_pos)
			#print range_pos['gene_id']+'\t'+range_pos['begin']+'\t'+range_pos['end']#{str(line.split('\t' )[0]): dict()}

	return range_pos_all

def compare(range_pos_all,variant_info, file_writer, name):
	for gene_dict in range_pos_all:
		#print gene_dict, type(gene_dict['begin'])
		if gene_dict['begin'] <= variant_info['pos'] and variant_info['pos'] <= gene_dict['end'] and variant_info['chr'] == gene_dict['chr']:	
			variant_info['major_cn'] = gene_dict['cnv_state']		
			print "Mutation lies in %s" % 	gene_dict['gene_id'] 
			variant_info['mutation_id'] = name+':'+variant_info['genotype']+':'+gene_dict['gene_id']+':'+variant_info['chr']+':'+str(variant_info['pos'])
			tsv_writer(variant_info, file_writer)


def tsv_writer(variant_info, file_writer):
	for ele in variant_info:
		#print ele
		file_writer.write(str(variant_info[ele])+'\t')
	file_writer.write('\n')
	file_writer.close()
				

##controllable
def main():
	text_file = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
	short2 = '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'

	to_lower(text_file)
	changepath(text_file)
	to_lower(short2)
	add_gender(short2, text_file)
	names = sample_names(text_file)
	
	#for name in names:
		#makedir(name)
		#copyfile_VCF_TXT(name)
		#copyfile_BAM(name)
		#source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/*.vcf'% name)
		#for files in source:
			#variant_info,file_writer = prep_tsv(name,files)
			#read_vcf(variant_info,files,cnv_file,name,file_writer)

		#file_writer.close()
			

	

if __name__ == "__main__":
	main()

print("--- %s seconds ---" % (time.time() - start_time))
