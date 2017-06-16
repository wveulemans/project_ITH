#!/usr/bin/python
import csv
from collections import OrderedDict as OD

def mk_info_file(short2, text_file, info_file):
	"""
		Input: 	'/home/shared_data_core/COLON/subclonality/paired_samples_nele_purity_all_runs_short.txt' & 
			'/home/shared_data_core/COLON/subclonality/Klinischegegegeven_patienten_ITH_20151110.csv'
		----------
	    	Function: makes new file (info_file.txt), with extra information about sample
		----------
		Output: '/home/shared_data_core/COLON/subclonality/info_file.txt'

	"""

	r_sample = open(text_file, 'rb')
	next(r_sample) # skip header

	w = open(info_file, 'wb')
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
