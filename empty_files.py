#!/usr/bin/python

import logging

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
			logging.info("Patient %s: file: "% name +files.split('/', 6)[6]+" empty!")
	
	return pyclone_file
