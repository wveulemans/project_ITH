#!/usr/bin/python

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
