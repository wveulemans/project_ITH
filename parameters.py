#!/usr/bin/python

import logging
from collections import OrderedDict as OD
import os

def parameters(name):
	"""
		Input: SupraHex_input_patient_name.tsv
		----------
	    	Function: Calculate:	- overall cellular prevalence
					- overall cellular prevalence standard deviation
					- cluster cellular prevalence
					- cluster cellular prevalence standard deviation
		----------
		Output: file with calculations

	"""
	
	if os.path.exists("/home/shared_data_core/COLON/subclonality/%s/supraHex_input_%s.tsv"% (name, name)):
		w = open("/home/shared_data_core/COLON/subclonality/%s/parameters_%s.tsv"% (name, name), "wb")
		r = open('/home/shared_data_core/COLON/subclonality/%s/PyClone_table_%s.tsv'% (name, name), 'rb')
		next(r)

		# make r more iterable than 1 time
		data = list(r)

		prev_VAF = OD([
			('clu_id', str()),			# cluster id
			('sample_id', str()),			# sample id
			('cell_prev', str()),			# cellular prevalence
			('cell_prev_std', str()),		# cellular prevalence standard deviation
			('cell_prev_overall', str()),		# overall cellular prevalence
			('cell_prev_std_overall', str()), 	# overall cellular prevalence standard deviation
			('VAF', str()),				# variant allele frequency
			('VAF_overall', str()),			# overall variant allele frequency
		])
	
		# Clusters
		###################################################################
		clu_id = []
		for line in data:
			clu_id.append(line.split('\t')[2])

		cor_clu_id = []
		for i in clu_id:
			if i not in cor_clu_id:
				cor_clu_id.append(i)

		cor_clu_id.sort()
		prev_VAF['clu_id'] = cor_clu_id
		#print prev_VAF['clu_id']
	
		# Samples
		###################################################################
		sample_id = []
		for line in data:
			sample_id.append(line.split('\t')[1])

		cor_sample_id = []
		for i in sample_id:
			if i not in cor_sample_id:
				cor_sample_id.append(i)

		cor_sample_id.sort()
		prev_VAF['sample_id'] = cor_sample_id
		#print prev_VAF['sample_id']

		# Cell prevalence
		###################################################################
		r_cell_prev = []
		for i in prev_VAF['clu_id']:
			#print i
			for o in prev_VAF['sample_id']:
				#print o
				cell_prev = []
				for line in data:
					if i == line.split('\t')[2] and o == line.split('\t')[1]:
						cell_prev.append(line.split('\t')[3])

				cell_prev = map(float, cell_prev)
				#print cell_prev

				# count amount of numbers
				count = 0
				for p in cell_prev:
					count += 1
				#print count
	
				# calculate average
				#print (sum(cell_prev)/count)
				r_cell_prev.append(format((sum(cell_prev)/count), '.4f'))

		prev_VAF['cell_prev'] =  r_cell_prev
		

		
		
		# Cell prevalence std
		###################################################################
		r_cell_prev_std = []
		for i in prev_VAF['clu_id']:
			#print i
			for o in prev_VAF['sample_id']:
				#print o
				cell_prev_std = []
				for line in data:
					if i == line.split('\t')[2] and o == line.split('\t')[1]:
						cell_prev_std.append(line.split('\t')[4])

				cell_prev_std = map(float, cell_prev_std)
				#print cell_prev

				# count amount of numbers
				count = 0
				for p in cell_prev_std:
					count += 1
				#print count
	
				# calculate average
				#print (sum(cell_prev_std)/count)
				r_cell_prev_std.append(format((sum(cell_prev_std)/count), '.4f'))

		prev_VAF['cell_prev_std'] = r_cell_prev_std

		# Overall cell prevalence
		###################################################################
		cell_prev = []
			
		for line in data:
			cell_prev.append(line.split('\t')[3])
		cell_prev = map(float, cell_prev)
		#print sum(cell_prev)

		# count amount of numbers
		count = 0
		for i in cell_prev:
			count += 1
		#print count

		# calculate average
		#print (sum(cell_prev)/count)
		prev_VAF['cell_prev_overall'] = format((sum(cell_prev)/count), '.4f')

		# Overall cell prevalence std
		###################################################################
		cell_prev_std = []
			
		for line in data:
			cell_prev_std.append(line.split('\t')[4])
		cell_prev_std = map(float, cell_prev_std)
		#print sum(cell_prev_std)

		# count amount of numbers
		count = 0
		for i in cell_prev_std:
			count += 1
		#print count

		# calculate average
		#print (sum(cell_prev_std)/count)
		prev_VAF['cell_prev_std_overall'] = format((sum(cell_prev_std)/count), '.4f')
	
		# Variant allele frequency
		###################################################################
		r_VAF = []
		for i in prev_VAF['clu_id']:
			#print i
			for o in prev_VAF['sample_id']:
				#print o
				VAF = []
				for line in data:
					if i == line.split('\t')[2] and o == line.split('\t')[1]:
						VAF.append(float((line.split('\t')[5]).split('\n')[0]))
				
				#print VAF
				VAF = map(float, VAF)
				#print VAF

				# count amount of numbers
				count = 0
				for p in VAF:
					count += 1
				#print count
	
				# calculate average
				#print (sum(cell_prev_std)/count)
				r_VAF.append(format((sum(VAF)/count), '.4f'))
		
		prev_VAF['VAF'] = r_VAF

		# Overall variant allele frequency
		###################################################################
		VAF_overall = []
			
		for line in data:
			VAF_overall.append((line.split('\t')[5]).split('\n')[0])

		VAF_overall = map(float, VAF_overall)
		#print sum(VAF_overall)

		# count amount of numbers
		count = 0
		for i in VAF_overall:
			count += 1
		#print count

		# calculate average
		#print (sum(VAF_overall)/count)
		prev_VAF['VAF_overall'] = format((sum(VAF_overall)/count), '.4f')
		
		#print prev_VAF
		
		# write to file
		###################################################################
		for k,v in prev_VAF.iteritems():
			w.write(k+'\t')
		w.write('\n')

		count = 0
		for cluster in prev_VAF['clu_id']:
			for sample in prev_VAF['sample_id']:
				w.write(cluster+'\t'+sample+'\t'+str(prev_VAF['cell_prev'][count])+'\t'+str(prev_VAF['cell_prev_std'][count])+'\t'+str(prev_VAF['cell_prev_overall'])+'\t'+str(prev_VAF['cell_prev_std_overall'])+'\t'+str(prev_VAF['VAF'][count])+'\t'+str(prev_VAF['VAF_overall']) )
				count += 1
				w.write('\n')
		logging.info('parameter file created for %s'% name)

