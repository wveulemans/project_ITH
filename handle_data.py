#! /usr/bin/python
import os, sys
import csv	# knows where it has stopped in file
import glob
import shutil
import vcf
import time
import stat
import subprocess
import logging
from collections import OrderedDict as OD

start_time = time.time()


def to_lower(short):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt' & '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
		----------
	    	Function: set all characters to lowercase
		----------
		Output: same file as infile

	"""

	f = open(short, 'rw+')
	lines = [line.lower() for line in f]

	with open(short, 'w') as out:
     		out.writelines(lines)
	f.close()



def mk_info_file(short2, text_file):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
		----------
	    	Function: makes new file (info_file.txt), with extra information about sample
		----------
		Output: '/home/shared_data_core/COLON/subclonality/info_file.txt'

	"""

	r_sample = open(text_file, 'rb')
	next(r_sample) # skip header

	w = open('info_file.txt', 'wb')
	w.write('normal_sample_name\ttumor_sample_name\tanalysis_type\tsample_file_directory\tsample_label\tsomatic_callers\tnormal_fraction\ttumor_fraction\tgender\tdate_of_birth\tamount_PT\tage_sample_taken\ttumor_fraction\n')

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
			('age_sample_taken', str()),
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
		next(reader)	# skip header
		for line in reader:
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


def sample_names(paired_samples):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
		----------
	    	Function: makes a list with every patient_name
		----------
		Output: list with all patient_names

	"""

	result=[]

	sample = open(paired_samples, 'r')
	next(sample) # skip header

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



def makedir(name):
	"""
		Input: every patient_name
		----------
	    	Function: makes for every patient_name a directory ('/home/shared_data_core/COLON/subclonality/patientname')
		----------
		Output: patientdirectory is made

	"""

	PATH = '/home/shared_data_core/COLON/subclonality/'
	if not os.path.exists(os.path.join(PATH,name)):
		os.mkdir(os.path.join(PATH,name))
		print "Directory: %s is created!"% name
	else:
		print "Directory: %s already exist!"% name
		logging.info("Directory: %s already exist!"% name)



def copyfile_VCF_TXT(name):
	"""
		Input: every patient_name
		----------
	    	Function: copies all VCF's per patient_name
		----------
		Output: VCF's are in correct patient_directory

	"""

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
		
				

def copyfile_BAM(name):
	"""
		Input: every patientname
		----------
	    	Function: copies all BAM's & BAI's per patient_name
		----------
		Output: BAM's & BAI's are in correct patient_directory

	"""

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
#				logging.debug("File: "+BAM.split('/')[5]+" already exist!")

	print "All BAM's copied for %s!"% name
	
	for BAI in BAIS:
		if BAI.endswith('.bai'):
			if not os.path.exists(os.path.join(destination,BAI.split('/')[5])):
				shutil.copy2(os.path.abspath(BAI),destination)
#			else:
#				logging.debug("File: "+BAI.split('/')[5]+" already exist!")
	print "All BAI's copied for %s!"% name



def prep_tsv(name,files):
	"""
		Input: 
		----------
	    	Function: makes a TSV file per sample for 
		----------
		Output: TSV file per sample

	"""

	parts = []		
	parts = files.split("/")[6]
	#print parts

	
	file_writer = open('/home/shared_data_core/COLON/subclonality/%s/pyclone_%s.tsv'% (name,parts),'w+')
	file_writer.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')	# add header to outfile

	global variant_info
	variant_info = OD([
		('mutation_id', str()),		# unique id for every mutation
		('ref_counts', int()),		# number of reads covering the mutation which contain the reference (genome) allele
		('var_counts', int()),		# number of reads covering the mutation which contain the variant allele
		('normal_cn', int()),		# copy number of the cells in the normal population. For autosomal chromosomes this will be 2 and for sex chromosomes it could be either 1 or 2
		('minor_cn', int()),		# minor copy number of the cancer cells. Usually this value will be predicted from WGSS or array data
		('major_cn', str()), 		# major copy number of the cancer cells. Usually this value will be predicted from WGSS or array data
		('variant_case', str(name)),	# patient_name
		('variant_freq', float()),	# 1 - (ref_counts/(ref_counts + var_counts))
		('genotype', str()),		# genotype of the mutation
		('nr', int()), 			# count per mutation
		('chr', str()), 		# chromosome where mutations lies
		('pos', int()),			# position on chromosome
		('origin',str())		# pt = primary tumor or m = metases
	])

	return variant_info,file_writer

def read_vcf(variant_info,files,cnv_file,name,file_writer,short2,info_file):
	"""
		Input: VCF file 
		----------
	    	Function: extract parameters out of VCF file
		----------
		Output: fills the dictionnary in, in the def above

	"""

	variant_number = 0

	file_name = files.split('/')[6]
	#print file_name
	char1 = file_name.split('_')[3]
	char2 = file_name.split('_')[4] 
	origin_tum = file_name.split('_')[5]
	
	variant_info['origin'] = name+'_'+char1+'_'+char2+'_'+origin_tum	
	#print variant_info['origin']
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
		if variant_info['chr'] == 'chrX' or variant_info['chr'] == 'chrY':			# Checks if sexchromosome then check the gender
			r = open(info_file, 'rb')
			next(r)	#skip header

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
	"""
		Input: CNV files
		----------
	    	Function: extract parameters out of CNV file
		----------
		Output: fills the dictionnary in, 2 def's above

	"""

	range_pos_all = list()	
	range_pos = dict()
	if cnv_file == True:
		source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/X.home.*%s*'% (name, variant_info['origin']))
		for files in source:
			#print files
			present = open(files, 'rb')			
			next(present)	# skip header

			for line in present:
				if float(line.split('\t')[4]) <= 6:
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
					if '.' in line.split('\t')[4]:
						if line.split('\t')[4] < "2":
							range_pos['cnv_state'] = (line.split('\t')[4]).split('.')[0]
							range_pos_all.append(range_pos)
						else:
							cn_one = str(1 + float(line.split('\t')[4]))
							range_pos['cnv_state'] = (cn_one).split('.')[0]
							range_pos_all.append(range_pos)
					else:
						range_pos['cnv_state'] = str(line.split('\t')[4])
						range_pos_all.append(range_pos)
				else:
					logging.warning("major_cn: "+line.split('\t')[4]+" !ARTEFACT!-----"+str(line.split('\t')[0:5]))

	return range_pos_all



def compare(range_pos_all,variant_info, file_writer, name):
	"""
		Input: parameters from CNV file
		----------
	    	Function: see of the position of the mutation lays in the gene 
		----------
		Output: fills the dictionnary in, 2 def's above (variant_info[mutation_id])

	"""

	for gene_dict in range_pos_all:
		if gene_dict['begin'] <= variant_info['pos'] and variant_info['pos'] <= gene_dict['end'] and variant_info['chr'] == gene_dict['chr']:	
			variant_info['major_cn'] = gene_dict['cnv_state']		
			#print "Mutation lies in %s"% gene_dict['gene_id'] 
			variant_info['mutation_id'] = name+':'+variant_info['genotype']+':'+gene_dict['gene_id']+':'+variant_info['chr']+':'+str(variant_info['pos'])
			tsv_writer(variant_info, file_writer)


def tsv_writer(variant_info, file_writer):
	"""
		Input: dictionary variant_info, contains information about mutation
		----------
	    	Function: write in file
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone...vcf.tsv'

	"""

	a11 = variant_info.keys()

	for ele in a11[0:9]:
		#print ele
		file_writer.write(str(variant_info[ele])+'\t')
	file_writer.write('\n')



def empty_files(name, files):
	"""
		Input: preprocessed pyclone files (ex: pyclone_ith_run3_a_1_3_pt_filter1_indel.vcf.tsv)
		----------
	    	Function: check if files are empty and write log
		----------
		Output: if file empty ==> state = False

	"""

	global pyclone_file
	pyclone_file = 1
	
	# find all preprocessed pyclone files
	if 'pyclone_ith' in files:
		r = open(files, 'rb')
		# amount of bytes if only header is present in file
		EOH = r.seek(97)

		if len(r.read()) == 0:
			pyclone_file = 0
			logging.info("File: "+files.split('/', 6)[6]+" empty!")
	
	return pyclone_file
		


def input_files(patient_dir, name, files):
	"""
		Input: all files from patient_directory
		----------
	    	Function: make a list with correct TSV for PyClone input 
		----------
		Output: list with correct TSV files

	"""

	patient_name = '_'.join(os.path.basename(files).split('_')[3:7])
	
	variant_types = ['snp','indel']
	vcf_files = list()
	for variant_type in variant_types:
		vcf_files.append(glob.glob(patient_dir+'*'+patient_name+'*'+variant_type+'*.vcf.tsv'))
	
	return patient_name, vcf_files

		

def input_tsv(patient_dir, name, patient_name, vcf_files):
	"""
		Input: list with input files for the actual mutation_informationfile.tsv
		----------
	    	Function: make actual mutation_informationfile.tsv
		----------
		Output: PYCLONE....tsv, ready for PyClone

	"""

	#if not os.path.exists(os.path.join(patient_dir+'PYCLONE_input_%s.tsv'% patient_name)):
	if pyclone_file == True:
		if '%s'% name in patient_name:
			if not '.tsv' in patient_name:
				w = open('/home/shared_data_core/COLON/subclonality/%s/PYCLONE_input_%s.tsv'% (name, patient_name), 'wb')
				w.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')
				for f in vcf_files:
					for i in f:
						r = open(i, 'rb')
						next(r)	#skip header
						for line in r:
							w.write(line)
				print "File: PYCLONE_input_%s.tsv \t READY!"% patient_name
				w.close()


def prep_config_file(name, patient_name, patient_dir):
	"""
	    	Function: makes a configuration_file for every patient_name 
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/config_file_patient_name' 

	"""

	w = open('/home/shared_data_core/COLON/subclonality/%s/config_file_%s.yaml'% (name,name), 'wb')	
	#w.write('# Specifies working directory for analysis. All paths in the rest of the file are relative to this.\n')
	w.write('working_dir: /home/shared_data_core/COLON/subclonality/\n\n')
	
	#w.write('\n# Where the trace (output) from the PyClone MCMC analysis will be written.\n')
	w.write('trace_dir: %s/\n\n'% name)

	#w.write('\n# Specifies which density will be used to model read counts. Most people will want pyclone_beta_binomial or pyclone_binomial\n')
	w.write('density: pyclone_beta_binomial\n\n')

	#w.write('\n# Number of iterations of the MCMC chain.\n')
	w.write('num_iters: 1000\n\n')

	#w.write('\n# Specifies parameters in Beta base measure for DP. Most people will want the values below.\n')
	w.write('base_measure_params:\n')
	w.write('  alpha: 1\n')
	w.write('  beta: 1\n\n')

	#w.write('\n# Specifies initial values and prior parameters for the prior on the concentration (alpha) parameter in the DP. If the prior node is not set the concentration will not be estimated and the specified value will be used.\n')
	w.write('concentration:\n')
	
	#w.write('# Initial value if prior is set, or fixed value otherwise for concentration parameter.\n\t')
	w.write('  value: 1.0 \n\n')
	
	#w.write('\n# Specifies the parameters in the Gamma prior over the concentration parameter\n')
	w.write('  prior:\n    shape: 1.0\n    rate: 0.001\n\n')

	#w.write('# Beta-Binomial precision (alpha + beta) prior')
	w.write('beta_binomial_precision_params:\n')
	#w.write('# Starting value')
	w.write('  value: 1000\n\n')

	#w.write('# Parameters for Gamma prior distribution')
	w.write('  prior:\n')
	w.write('    shape: 1.0\n')
	w.write('    rate: 0.0001\n\n')

	#w.write('# Precision of Gamma proposal function for MH step')
	w.write('  proposal:\n')
	w.write('    precision: 0.01\n\n')

	#w.write('\n# Specify the samples for the analysis.\n')
	w.write('samples:\n')

##########################################################################################################for loop

	source = glob.glob(patient_dir+'*')
	for files in source:
		if 'PYCLONE' in files:
			sample_name = (('_'.join(files.split('_')[4:8])).split('.')[0])
			
			#w.write('\t# Unique sample ID.\n')
			w.write('  %s: \n'% sample_name)

			#w.write('\t\t# Path where tsv formatted mutations file for the sample is placed.\n')
			w.write('    mutations_file: PYCLONE_input_%s.tsv.yaml\n\n'% sample_name)
			
			w.write('    tumour_content:\n')
			#w.write('\t\t\t# The predicted tumour content for the sample. If you have no estimate set this to 1.0.\n')
			r = open('/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt')
			next(r)
			for line in r:
				if (line.split('\t')[1]).split('_', 2)[2] == sample_name:
					w.write('      value: '+line.split('\t')[7].split('\n')[0]+'\n\n')
					#w.write('\t\t# Expected sequencing error rate for sample.\n')
					w.write('    error_rate: 0.001\n\n')	

	w.close
	

def prep_bash(name):
	"""
	    	Function: makes a bash_file for every patient_name 
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone_bash_patient_name.sh'

	"""
	
	# check if bash file for patient exist
	if os.path.exists('/home/shared_data_core/COLON/subclonality/%s/pyclone_bash_%s.sh'% (name,name)):
		logging.info("Bash_file: pyclone_bash_%s.sh already exist!"% name)
	
	# if bash not exists, make bash with all necessary lines
	else:				
		w = open('/home/shared_data_core/COLON/subclonality/%s/pyclone_bash_%s.sh'% (name,name), 'wb')
		w.write('#!/bin/bash\n')
		w.write('#WVeulemans\n\n')
		w.write('WORKING_DIR= "/home/shared_data_core/COLON/subclonality/%s/"\n\n'% name)
		w.write('echo -e "#!/bin/bash\n#PBS -X\t\t\t\t\t\tThe -x option allows the script to be executed in the interactive job and then the job completes\n#PBS -N PyClone$tumor_sample_name\t\tDeclares a name for the job\n#PBS -l nodes=1:ppn=8,mem=4g,walltime=01:00:00\tDefines the resources that are required by the job and establishes a limit to the amount of resource that can be consumed\n#PBS -m ea\t\t\t\t\tmail_options\n#PBS -M ward.veulemans@student.howest.be\tDeclares the list of users to whom mail is sent\n#PBS -q scattergather\t\t\t\tDefines the destination of the job\n#PBS -A onco\t\t\t\t\tDefines the account string associated with the job\n"\n\n')


		w.write('echo "Building yaml files"\n')
		source = glob.glob('/home/shared_data_core/COLON/subclonality/%s/*'% name)
		for files in source:
			inputs = files.split('/')[6]
			if 'PYCLONE_input' in inputs:
				w.write('echo `PyClone build_mutations_file --in_file '+inputs+' --out_file '+inputs+'.yaml`\n')

		w.write('echo "Running pipeline analysis"\n')
		w.write('\necho `PyClone run_analysis --config_file config_file_%s.yaml`\n'% name)
		w.close()
	
	global bash_file
	bash_file = '/home/shared_data_core/COLON/subclonality/%s/pyclone_bash_%s.sh'% (name,name)

	return 	bash_file



def run_bash(bash_file, name):
	"""
	    	Function: executes bash_file per patient_name (converts TSV to YAML and runs PyClone)
		----------
		Output:	- converted TSV '/home/shared_data_core/COLON/subclonality/patient_name/PYCLONE_input_patient_sample.tsv.yaml'
			- outfile '...'

	"""

	os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)
	# change rights from bash file
	os.chmod('pyclone_bash_%s.sh'% name, 0755)
	subprocess.call('./pyclone_bash_%s.sh'% name)
	os.stat('pyclone_bash_%s.sh'% name)




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
		patient_dir = '/home/shared_data_core/COLON/subclonality/%s/'% name
		source = glob.glob(patient_dir+'*.vcf')
		for files in source:
			variant_info,file_writer = prep_tsv(name,files)
			read_vcf(variant_info,files,cnv_file,name,file_writer,short2,info_file)

		file_writer.close()
		source = source = glob.glob(patient_dir+'*.tsv') 
		for files in source:
			empty_files(name, files)
			patient_name, vcf_files = input_files(patient_dir, name, files)
			input_tsv(patient_dir, name, patient_name, vcf_files)
		prep_config_file(name, patient_name, patient_dir)
		prep_bash(name)
		run_bash(bash_file, name)
		print "Patient: "+name+" is analyzed!"
	 	
	
   	logging.info('Finished')
	

if __name__ == "__main__":
	main()

print("--- %s seconds ---" % (time.time() - start_time))
