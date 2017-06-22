#!/usr/bin/python

import os, glob

def input_files(patient_dir, name, files, distinct_samples):
	"""
		Input: all files from patient_directory
		----------
	    	Function: make a list with correct TSV for PyClone input 
		----------
		Output: list with correct TSV files

	"""

	patient_name = ('_'.join(os.path.basename(files).split('_')[2:6])).split('.')[0]
	print patient_name
	
	source = glob.glob(patient_dir+'/*')
	
	vcf_files = list()
	for files in source:
		if 'PYCLONE' in files and patient_name in files:
			#print files
			vcf_files.append(files)
	#print vcf_files


	return patient_name, vcf_files

######################################################################################################################
def input_files_all(patient_dir_all, files):
	"""
		Input: all files from patient_directory
		----------
	    	Function: make a list with correct TSV for PyClone input 
		----------
		Output: list with correct TSV files

	"""

	patient_name = ('_'.join(os.path.basename(files).split('_')[2:6])).split('.')[0]
	#print patient_name
	
	source = glob.glob(patient_dir_all+'/*')
	
	vcf_files = list()
	for files in source:
		if 'PYCLONE' in files and patient_name in files:
			#print files
			vcf_files.append(files)
	print vcf_files


	return patient_name, vcf_files
