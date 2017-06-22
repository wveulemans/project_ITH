#! /usr/bin/python

#load python dependencies
import os, sys
import csv	# knows where it has stopped in file
import glob
import shutil
import vcf
import time
import stat
import subprocess
from collections import OrderedDict as OD

import log_system, to_lower, information_file, patientnames, make_directory, copy_VCF, copy_CNV, prep_config, execute, rights, convert_PDF, empty_files, parameters, prep_SupraHex, prep_bash, input_TSV, input_files, prep_TSV, read_VCF, read_CNV, compare, prep_TSV2, TSV_writer, TSV2_writer, prep_table

start_time = time.time()	

def main():

	# Initiate logging systems
	debug_mode = 0
	logging = log_system.initiate_log(debug_mode)
	logging.debug('Log initiated')

	info_file = '/home/shared_data_core/COLON/subclonality/info_file.txt'
	short2 = '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
	text_file_all = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short_all.txt'
	info_file2 = '/home/shared_data_core/COLON/subclonality/info_file2.txt'
	ALL = 'ALL'

#	to_lower.to_lower(text_file_all)
#	to_lower.to_lower(info_file2)
#	information_file.mk_info_file(short2, text_file_all, info_file2)
#	
#	names_all = patientnames.sample_names(text_file_all)
#	print names_all
#	make_directory.makedir(ALL)

#	for name in names_all:
#		# copy VCF's and CNV's	
#		copy_VCF.copyfile_VCF_all(name, ALL)
#		copy_CNV.copyfile_CNV_all(name, ALL)
#
	global patient_dir_all
	patient_dir_all = '/home/shared_data_core/COLON/subclonality/'+ALL+'/'
#		source = glob.glob(patient_dir_all+'*.vcf')
#
#		var_types = ['snp','indel']
#		for var_type in var_types:
#			file_type = glob.glob(patient_dir_all+'*'+var_type+'*.vcf')
#			#print 'FOUND :: ', file_type
#
#		for files in source:
#			if '_'+name+'_' in files:
#				# check for empty VCF_files
#				if not os.path.getsize(files) == 2970:
#					variant_info,file_writer = prep_TSV.prep_tsv_all(name,files,ALL)
#					range_pos_all = read_VCF.read_vcf_all(variant_info,files,name,file_writer,short2,info_file, ALL)
#				else:
#					logging.info('File:'+files+' is empty!')
#					print 'file: '+files+' is empty!!!!!!!!!!!'
#
#	patient_variant_dict, distinct_samples = prep_TSV2.prep_tsv2_all(name, range_pos_all, ALL)
#
#	TSV2_writer.tsv2_writer_all(patient_variant_dict, distinct_samples, name, ALL)
#	TSV2_writer.uniq_all(name, distinct_samples, ALL)
#	file_writer.close()
#
#
	source = glob.glob('/home/shared_data_core/COLON/subclonality/'+ALL+'/*.tsv')
	for files in source:
		if 'PYCLONE' in files:
			patient_name, vcf_files = input_files.input_files_all(patient_dir_all, files)

	prep_config.prep_config_file_all(patient_name, patient_dir_all, ALL)
	prep_bash.prep_bash_all(ALL)
	execute.exe_bash_all(ALL)

	prep_table.prep_pyclone_table_all(patient_dir_all, ALL)
		
	prep_SupraHex.prep_supraHex_all(ALL)
	execute.exe_supraHex_all(R_script, ALL)
	parameters.parameters(ALL)
		
	rights.rights(patient_dir_all)
	convert_PDF.convert_pdf_images(ALL)

	execute.exe_patient_report(report_script)

   	logging.info('Finished')
	
if __name__ == "__main__":
	main()

print("--- %s seconds ---" % (time.time() - start_time))
