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

#load script dependencies
import log_system, to_lower, information_file, patientnames, make_directory, copy_VCF, copy_CNV, prep_config, execute, rights, convert_PDF, empty_files, parameters, prep_SupraHex, prep_bash, input_TSV, input_files, prep_TSV, read_VCF, read_CNV, compare, prep_TSV2, TSV_writer, TSV2_writer, prep_table

start_time = time.time()


def main():

	# Initiate logging systems
	debug_mode = 0
	logging = log_system.initiate_log(debug_mode)
	logging.debug('Log initiated')

	text_file = '/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt'
	short2 = '/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
	global info_file
	info_file = '/home/shared_data_core/COLON/subclonality/info_file.txt'
	R_script = '/home/shared_data_core/COLON/subclonality/supraHex_script.R'
	report_script = '/home/shared_data_core/COLON/subclonality/report.py'
	
	# set characters to lowercase
	to_lower.to_lower(text_file)
	to_lower.to_lower(short2)

	# make general info_file
	information_file.mk_info_file(short2, text_file, info_file)

	# make list with all patients
	names = patientnames.sample_names(text_file)

	for name in names:

		# make directory per patient
		make_directory.makedir(name)
		
		# copy VCF's and CNV's	
		copy_VCF.copyfile_VCF(name)
		copy_CNV.copyfile_CNV(name)

		global patient_dir
		patient_dir = '/home/shared_data_core/COLON/subclonality/%s/'% name
		source = glob.glob(patient_dir+'*.vcf')

		var_types = ['snp','indel']
		for var_type in var_types:
			file_type = glob.glob(patient_dir+'*'+var_type+'*.vcf')
			#print 'FOUND :: ', file_type

		for files in source:
			variant_info,file_writer = prep_TSV.prep_tsv(name,files)
			range_pos_all = read_VCF.read_vcf(variant_info,files,name,file_writer,short2,info_file)

		patient_variant_dict, distinct_samples = prep_TSV2.prep_tsv2(name, range_pos_all)

		TSV2_writer.tsv2_writer(patient_variant_dict, distinct_samples, name)
		TSV2_writer.uniq(name, distinct_samples)
		file_writer.close()

		source = glob.glob(patient_dir+'*.tsv') 
		for files in source:
			empty_files.empty_files(name, files)
			if 'PYCLONE' in files:
				patient_name, vcf_files = input_files.input_files(patient_dir, name, files, distinct_samples)
		
				
		prep_config.prep_config_file(name, patient_name, patient_dir)
		prep_bash.prep_bash(name)
		#execute.exe_bash(name)

		prep_table.prep_pyclone_table(patient_dir, name)
		
		prep_SupraHex.prep_supraHex(name)
		execute.exe_supraHex(name, R_script)
		parameters.parameters(name)
		
		rights.rights(patient_dir)
		convert_PDF.convert_pdf_images(name)	

	#execute.exe_patient_report(report_script)



   	logging.info('Finished')
	
if __name__ == "__main__":
	main()

print("--- %s seconds ---" % (time.time() - start_time))
