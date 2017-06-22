#! /usr/bin/python

import glob
import os
from collections import OrderedDict as OD

def names(info):
	all_patients = []	
	
	r = open(info, 'rb')
	next(r)
	for lines in r:
		all_patients.append((lines.split('\t')[1]).split('_')[2])

	#print all_patients

	global patients
	patients = []
	for patient in all_patients:
		if not patient in patients:
			patients.append(patient)
	return patients

def input_file_citup(patient, pat_dir):

	source = glob.glob('*')
	for files in source:
		if 'PyClone_table' in files:
			r = open(files, 'rb')
			w = open('citup_input_'+patient+'.tsv', 'wb')
			# make r more iterable than 1 time
			data = list(r)
		
			samples = []
			for lines in data:
				if not 'sample_id' in lines:
					samples.append(lines.split('\t')[1])
			sample = set(samples)
			print sample
		
			#############logic mutation id, cell_prev1, cell_prev_std1, cell_prev2, cell_prev_std2,..., clu_id
		

			input_cit = OD([
				('mutation_id', str()),			# all mutations from table file
				('sample_id', str()),			# all samples from patient
				('cell_prev', str()),			# cellular prevalence & cellular prevalence std 
				('clu_id', str()),			# cluster id
			])

			# Mutation_id
			###################################################################
			mutation_id = []
			for line in data:
				if not 'mutation_id' in line:
					mutation_id.append(line.split('\t')[0])

			cor_mutation_id = []
			for i in mutation_id:
				if i not in cor_mutation_id:
					cor_mutation_id.append(i)

			input_cit['mutation_id'] = cor_mutation_id
			#print input_cit['mutation_id']

			# Samples
			###################################################################
			sample_id = []
			for line in data:
				if not 'sample_id' in line:
					sample_id.append(line.split('\t')[1])

			cor_sample_id = []
			for i in sample_id:
				if i not in cor_sample_id:
					cor_sample_id.append(i)

			cor_sample_id.sort()
			input_cit['sample_id'] = cor_sample_id
			#print input_cit['sample_id']
		
			# cell_prev
			###################################################################
			cell_prev = []
			for line in data:
				if not 'cellular_prevalence' in line:
					cell_prev.append(line.split('\t')[3])

		
			input_cit['cell_prev'] = cell_prev
			#print input_cit['cell_prev']

			# Clusters
			###################################################################
			clu_id = []
			for line in data:
				if not 'cluster_id' in line:
					clu_id.append(line.split('\t')[2])

			input_cit['clu_id'] = clu_id
			#print input_cit['clu_id']
			w.close	

			# count samples
			###################################################################
			samples = 0
			for sam in input_cit['sample_id']:
				samples += 1
			#print samples


			cp_min = 0
			cp_max = (samples*1)
			clu_id = 0
		
			#print input_cit
		
			for mutat in input_cit['mutation_id']:
				for i in input_cit['cell_prev'][cp_min : cp_max]:
					w.write(str(i)+'\t')
				cp_min += samples*2
				cp_max += samples*2
			
				w.write('\n')
				clu_id += samples
	

def main():
	info_file = '/home/shared_data_core/COLON/subclonality/info_file.txt'

	names(info_file)
	for patient in patients:
		print patient
		pat_dir = '/home/shared_data_core/COLON/subclonality/'+patient+'/'
		os.chdir(pat_dir)
		
		input_file_citup(patient, pat_dir)

if __name__ == "__main__":
	main()
