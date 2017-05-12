#! /usr/bin/python
import os, sys
import csv	#knows where it has stopped
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


##add gender to file
def mk_info_file(short2, text_file):

	r_sample = open(text_file, 'rb')
	next(r_sample)

	w = open('info_file.txt', 'wb')
	w.write('normal_sample_name\ttumor_sample_name\tanalysis_type\tsample_file_directory\tsample_label\tsomatic_callers\tnormal_fraction\ttumor_fraction\tgender\tdate_of_birth\tamount_PT\tage_sample_taken\n')

	patient_info = OD([
			('normal_sample_name', str()),
			('tumor_sample_name', str()),
			('analysis_type', str()),
			('sample_file_directory', str('/home/shared_data_core/COLON/ITH_nele_VCFs_amplicon_filter/VCF_filter1/')),
			('sample_label', str()),
			('somatic_callers', str()),
			('normal_fraction', str()),
			('tumor_fraction', str()),
			('gender', str()),
			('date_of_birth', str()),
			('amount_PT', str()),
			('age_sample_taken', str())
			])    	
	
	for line in r_sample:
		patient_info['normal_sample_name'] = line.split()[0]
		patient_info['tumor_sample_name'] = line.split()[1]
		patient_info['analysis_type'] = line.split()[2]		
		patient_info['sample_file_directory'] = line.split()[3]
		patient_info['sample_label'] = line.split()[4]
		patient_info['somatic_callers'] = line.split()[5]
		patient_info['normal_fraction'] = line.split()[6]
		patient_info['tumor_fraction'] = line.split()[7]

		r_info = open(short2, 'rb')
		reader = csv.reader(r_info, delimiter=',')
		next(reader)
		for line in reader:
			#print "PATIENT :: ",patient_info['normal_sample_name'].split('_')[2], line[0]
			if line[0] == patient_info['normal_sample_name'].split('_')[2]:
				patient_info['gender'] = line[6]
				patient_info['date_of_birth'] = line[3]
				patient_info['amount_PT'] = line[8]
				patient_info['age_sample_taken'] = line[9]
				for x in patient_info:
					#print patient_info[x]
					w.write(str(patient_info[x])+'\t')
				w.write('\n')
	w.close


##mkdir per patient
def sample_names(short2):
	result=[]

	sample = open(short2, 'r')
	next(sample)

	for line in sample:
		parts = line.split()		
		if len(parts) > 0:   		
		    result.append(parts[4])

	#print result
	names = []

	for name in result:
		if name.split('_')[2] not in names:
			names.append(name.split('_')[2])
			
	
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
		logging.info("Directory: %s already exist!"% name)


##copy .vcf files to patientdirectory
def copyfile_VCF_TXT(name):
	source = glob.glob('/home/shared_data_core/COLON/ITH_nele_VCFs_amplicon_filter/VCF_filter1/*_%s_*/*filter*.vcf'% name)
	#print source
	destination = '/home/shared_data_core/COLON/subclonality/%s/'% name		
	#print destination	
	for files in source:
		if  files.endswith('.vcf'):
			if not os.path.exists(os.path.join(destination,files.split('/')[7])):
				shutil.copy2(os.path.abspath(files),destination)
#			else:
#				logging.info("File: "+files.split('/')[7]+" already exist!")

	print "All VCF's copied for %s!"% name
	
	
	source1 = glob.glob('/home/shared_data_core/COLON/subclonality/CNV/*_%s_*.txt'% name)
	#print source1	
		
	destination1 = '/home/shared_data_core/COLON/subclonality/%s/'% name
	#print destination1
	
	global cnv_file	
	cnv_file = 0

	try:	
		for files in source1:	
			shutil.copy2(os.path.abspath(files),os.path.abspath(destination1))
			print "Transferring CNV file"
			cnv_file = 1


	except IndexError,e:
		print "No CNV file. %s"% e
		logging.error("No CNV file present!!!")
		cnv_file = 0

	if cnv_file == 0:
		print "No CNV file."
		logging.error("CNV file missing for :"+files.split('/')[7]+"!!!")
		cnv_file = 0

	return cnv_file
		
				

##move .bam and .bai files to patientdirectory
def copyfile_BAM(name):
	BAMS = glob.glob('/home/shared_data_core/COLON/ITH_nele_BAMs/*_%s_*.bam'%name)
	BAIS = glob.glob('/home/shared_data_core/COLON/ITH_nele_BAMs/*_%s_*.bam.bai'%name)	
	#print BAMS, '\n'
	#print BAIS, '\n'
	destination = '/home/shared_data_core/COLON/subclonality/%s/'% name
	for BAM in BAMS:
		if BAM.endswith('.bam'):
			if not os.path.exists(os.path.join(destination,BAM.split('/')[5])):
				shutil.copy2(os.path.abspath(BAM),destination)
#			else:
#				logging.info("File: "+BAM.split('/')[5]+" already exist!")

	print "All BAM's copied for %s!"% name
	
	for BAI in BAIS:
		if BAI.endswith('.bai'):
			if not os.path.exists(os.path.join(destination,BAI.split('/')[5])):
				shutil.copy2(os.path.abspath(BAI),destination)
#			else:
#				logging.info("File: "+BAI.split('/')[5]+" already exist!")
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
		('pos', int()),
		('origin',str())	#pt = primary tumor or m = metases
	])
	return variant_info,file_writer

def read_vcf(variant_info,files,cnv_file,name,file_writer,short2,info_file):
	variant_number = 0

	file_name = files.split('/')[6]
	#print file_name
	char1 = file_name.split('_')[3]
	char2 = file_name.split('_')[4] 
	origin_tum = file_name.split('_')[5]
	#print origin_tum
	#if origin_tum.count('.') > 0:
	#	variant_info['origin'] = origin_tum.split('.')[0]
	#else:
	#	variant_info['origin'] = name+'_'+char1+'_'+char2+':'+origin_tum
	variant_info['origin'] = name+'_'+char1+'_'+char2+'_'+origin_tum	
	
	vcf_reader = vcf.Reader(open('%s'% files, 'r'))
	for record in vcf_reader:
		#print record
		
		variant_info['nr'] = variant_number
		variant_info['chr'] = record.CHROM
		variant_info['pos'] = int(record.POS)
				
		variant_info['ref_counts'] = record.samples[1]['RD']
		variant_info['var_counts'] = record.samples[1]['AD']
		if record.samples[1]['AD'] == list():
			print '\nMULTI_ALLELIC !!!! ADJUST LOGIC :: ', record.samples[1]['AD'], '\n'
			sys.exit(0)
		#print variant_info['ref_counts']
		#print variant_info['var_counts']
		if variant_info['chr'] == 'chrX' or variant_info['chr'] == 'chrY':			##ATTENTION: sex chromosomes have different copynumber!!!
			r = open(info_file, 'rb')
			next(r)

			for row in r:
				#print row.split()[8]
				if row.split()[8] == 'm':
					variant_info['normal_cn'] = int('1')
					#print '1, because male and sex chr'						
				#else:
					#print '2, female'
			r.close()
			
		else:
			variant_info['normal_cn'] = int('2')
		#print variant_info['normal_cn']
		variant_info['variant_freq'] = format((1 - (float(record.samples[1]['RD'])/(record.samples[1]['RD'] + record.samples[1]['AD']))), '.12f')
		#print variant_info['variant_freq']
		
		variant_info['minor_CN'] = 0
		#print variant_info['major_CN'] = record.samples[4]

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
		range_pos_all = read_cnv(cnv_file, name, variant_info)
		compare(range_pos_all, variant_info, file_writer, name)
		
		
		

def read_cnv(cnv_file, name, variant_info):
	range_pos_all = list()	
	range_pos = dict()
	if cnv_file == True:
		#os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
		source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/X.home.*%s*'% (name, variant_info['origin']))
		for files in source:
			#print files
			present = open(files, 'rb')			
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
				#if range_pos['cnv_state'] == '55':
				#	print 'SHITTTT', line, present
				range_pos_all.append(range_pos)
				#print range_pos['gene_id']+'\t'+range_pos['begin']+'\t'+range_pos['end']#{str(line.split('\t' )[0]): dict()}

	return range_pos_all

def compare(range_pos_all,variant_info, file_writer, name):
	for gene_dict in range_pos_all:
		#print gene_dict, type(gene_dict['begin'])
		if gene_dict['begin'] <= variant_info['pos'] and variant_info['pos'] <= gene_dict['end'] and variant_info['chr'] == gene_dict['chr']:	
			variant_info['major_cn'] = gene_dict['cnv_state']		
			#print "Mutation lies in %s"% gene_dict['gene_id'] 
			variant_info['mutation_id'] = name+':'+variant_info['genotype']+':'+gene_dict['gene_id']+':'+variant_info['chr']+':'+str(variant_info['pos'])+':'+str(variant_info['origin'])
			tsv_writer(variant_info, file_writer)


def tsv_writer(variant_info, file_writer):
#	file_writer.write(str(variant_info['mutation_id']+'\t'+variant_info['ref_counts']+'\t'+variant_info['var_counts']+'\t'+variant_info['normal_cn']+'\t'+variant_info['minor_cn']+'\t'+variant_info['major_cn']+'\t'+variant_info['variant_case']+'\t'+variant_info['variant_freq']+'\t'+variant_info['genotype']+'\n'))

	for ele in variant_info:
		#print ele
		file_writer.write(str(variant_info[ele])+'\t')
	file_writer.write('\n')


def input_pyclone(patient_map, name):
	source = glob.glob(patient_map+'pyclone*')
	w = open('/home/shared_data_core/COLON/subclonality/%s/PYCLONE_input_%s.tsv'% (name, name), 'wb')
	w.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')
	for files in source:
		#print files
		r = open(files, 'rb')
		next(r)
		for line in r:
			w.write(line)
	print "File: PYCLONE_input_%s.tsv \t \t READY!"% name
	w.close()
			

	
				

##controllable
def main():
	logging.basicConfig(filename=os.path.dirname(os.path.realpath(__file__))+'/log.txt',
                    filemode='w',
                    format='%(asctime)s \t-\t %(name)s \t-\t %(levelname)s \t-\t %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    level=logging.NOTSET)
	stderrLogger = logging.StreamHandler()
	stderrLogger.setFormatter(logging.Formatter('%(asctime)s \t-\t %(name)s \t-\t %(levelname)s \t-\t %(message)s'))
	logging.getLogger().addHandler(stderrLogger)
	logging.debug('Log initiated')

	text_file = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
	short2 = '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
	info_file = '/home/shared_data_core/COLON/subclonality/info_file.txt'
	
	to_lower(text_file)
	to_lower(short2)
	mk_info_file(short2, text_file)
	names = sample_names(text_file)
	
	for name in names:
		makedir(name)
		copyfile_VCF_TXT(name)
		copyfile_BAM(name)
		patient_map = '/home/shared_data_core/COLON/subclonality/%s/'% name
		source = glob.glob(patient_map+'*.vcf')
		for files in source:
			variant_info,file_writer = prep_tsv(name,files)
			read_vcf(variant_info,files,cnv_file,name,file_writer,short2,info_file)

		file_writer.close()
		input_pyclone(patient_map, name)
	  	
   	logging.info('Finished')
	

if __name__ == "__main__":
	main()

print("--- %s seconds ---" % (time.time() - start_time))
