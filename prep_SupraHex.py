#!/usr/bin/python

import os
from collections import OrderedDict as OD

def prep_supraHex(name):
	"""
		Input: table_file from PyClone
		----------
	    	Function: make inputfile for supraHex
		----------
		Output: inputfile for supraHex

	"""

	os.chdir('/home/shared_data_core/COLON/subclonality/%s/'% name)

	if os.path.exists('PyClone_table_%s.tsv'% name):
		r = open('PyClone_table_%s.tsv'% name, 'rb')
		w = open('supraHex_input_%s.tsv'% name, 'wb')
	
		# make r more iterable than 1 time
		data = list(r)
		
		samples = []
		for lines in data:
			if not 'sample_id' in lines:
				samples.append(lines.split('\t')[1])
		sample = set(samples)
		print sample

		w.write('mutation_id'+'\t')
		for i in sample:
			#print i
			w.write(i+'\t'+i+'_std'+'\t')

		w.write('cluster_id'+'\n')
		
		#############logic mutation id, cell_prev1, cell_prev_std1, cell_prev2, cell_prev_std2,..., clu_id
		

		input_sup = OD([
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

		input_sup['mutation_id'] = cor_mutation_id
		#print input_sup['mutation_id']

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
		input_sup['sample_id'] = cor_sample_id
		#print input_sup['sample_id']
		
		# cell_prev
		###################################################################
		cell_prev = []
		for line in data:
			if not 'cellular_prevalence' in line:
				cell_prev.append(line.split('\t')[3])
				cell_prev.append(line.split('\t')[4])

		
		input_sup['cell_prev'] = cell_prev
		#print input_sup['cell_prev']

		# Clusters
		###################################################################
		clu_id = []
		for line in data:
			if not 'cluster_id' in line:
				clu_id.append(line.split('\t')[2])

		input_sup['clu_id'] = clu_id
		#print input_sup['clu_id']
		w.close	

		# count samples
		###################################################################
		samples = 0
		for sam in input_sup['sample_id']:
			samples += 1
		#print samples


		cp_min = 0
		cp_max = (samples*2)
		clu_id = 0
		
		#print input_sup
		
		for mutat in input_sup['mutation_id']:
			w.write(mutat+'\t')
			for i in input_sup['cell_prev'][cp_min : cp_max]:
				w.write(str(i)+'\t')
			cp_min += samples*2
			cp_max += samples*2
			
			w.write(str(input_sup['clu_id'][clu_id])+'\n')
			clu_id += samples


##############################################################################################################################################
def prep_supraHex_all(ALL):
	"""
		Input: table_file from PyClone
		----------
	    	Function: make inputfile for supraHex
		----------
		Output: inputfile for supraHex

	"""

	os.chdir('/home/shared_data_core/COLON/subclonality/'+ALL+'/')

	if os.path.exists('PyClone_table_'+ALL+'.tsv'):
		r = open('PyClone_table_'+ALL+'.tsv', 'rb')
		w = open('supraHex_input_'+ALL+'.tsv', 'wb')
	
		# make r more iterable than 1 time
		data = list(r)
		
		samples = []
		for lines in data:
			if not 'sample_id' in lines:
				samples.append(lines.split('\t')[1])
		sample = set(samples)
		print sample

		w.write('mutation_id'+'\t')
		for i in sample:
			#print i
			w.write(i+'\t'+i+'_std'+'\t')

		w.write('cluster_id'+'\n')
		
		#############logic mutation id, cell_prev1, cell_prev_std1, cell_prev2, cell_prev_std2,..., clu_id
		

		input_sup = OD([
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

		input_sup['mutation_id'] = cor_mutation_id
		#print input_sup['mutation_id']

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
		input_sup['sample_id'] = cor_sample_id
		#print input_sup['sample_id']
		
		# cell_prev
		###################################################################
		cell_prev = []
		for line in data:
			if not 'cellular_prevalence' in line:
				cell_prev.append(line.split('\t')[3])
				cell_prev.append(line.split('\t')[4])

		
		input_sup['cell_prev'] = cell_prev
		#print input_sup['cell_prev']

		# Clusters
		###################################################################
		clu_id = []
		for line in data:
			if not 'cluster_id' in line:
				clu_id.append(line.split('\t')[2])

		input_sup['clu_id'] = clu_id
		#print input_sup['clu_id']
		w.close	

		# count samples
		###################################################################
		samples = 0
		for sam in input_sup['sample_id']:
			samples += 1
		#print samples


		cp_min = 0
		cp_max = (samples*2)
		clu_id = 0
		
		#print input_sup
		
		for mutat in input_sup['mutation_id']:
			w.write(mutat+'\t')
			for i in input_sup['cell_prev'][cp_min : cp_max]:
				w.write(str(i)+'\t')
			cp_min += samples*2
			cp_max += samples*2
			
			w.write(str(input_sup['clu_id'][clu_id])+'\n')
			clu_id += samples
