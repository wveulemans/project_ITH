#!/usr/bin/python


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
