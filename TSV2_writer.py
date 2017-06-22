#! /usr/bin/python

def tsv2_writer(patient_variant_dict, distinct_samples, name):
	"""
		Input: dictionary variant_info, contains information about mutation
		----------
	    	Function: write in file
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone._sample_vcf.tsv'

	"""


	for sample in distinct_samples:
		w = open('/home/shared_data_core/COLON/subclonality/'+name+'/pyclone_'+sample+'.vcf.tsv', 'wb')
		w.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')

		for var_id in patient_variant_dict:
			for sample_var_id in patient_variant_dict[var_id]:
				#print sample_var_id.keys()[0]
				if sample == sample_var_id.keys()[0]:
					#print sample_var_id
					for key, value in sample_var_id.items():
						#print var_id
   						#print('{}: {}'.format(key, value))
						#print value
						w.write(var_id+'\t'+str(value.get('ref_cnt'))+'\t'+str(value.get('var_cnt'))+'\t'+str(value.get('normal_cn'))+'\t'+str(value.get('minor_cn'))+'\t'+str(value.get('major_cn'))+'\t'+str(value.get('var_case'))+'\t'+str(value.get('var_freq'))+'\t'+str(value.get('geno')+'\n'))
							
		w.close()				
					



def uniq(name, distinct_samples):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone._sample_vcf.tsv'
		----------
	    	Function: 
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone._sample_vcf.tsv'

	"""
	for sample in distinct_samples:
		uniqlines = set(open('/home/shared_data_core/COLON/subclonality/'+name+'/pyclone_'+sample+'.vcf.tsv').readlines())

		#this will give you the list of unique lines.
		#writing that back to some file would be as easy as:

		bar = open('/home/shared_data_core/COLON/subclonality/'+name+'/PYCLONE_input_'+sample+'.tsv', 'wb')
		bar.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')

		for line in set(uniqlines):
			if not 'mutation_id' in line:
				bar.write(line)

######################################################################################################################################################
def tsv2_writer_all(patient_variant_dict, distinct_samples, name, ALL):
	"""
		Input: dictionary variant_info, contains information about mutation
		----------
	    	Function: write in file
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone._sample_vcf.tsv'

	"""


	for sample in distinct_samples:
		w = open('/home/shared_data_core/COLON/subclonality/'+ALL+'/pyclone_'+sample+'.vcf.tsv', 'wb')
		w.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')

		for var_id in patient_variant_dict:
			for sample_var_id in patient_variant_dict[var_id]:
				#print sample_var_id.keys()[0]
				if sample == sample_var_id.keys()[0]:
					#print sample_var_id
					for key, value in sample_var_id.items():
						#print var_id
   						#print('{}: {}'.format(key, value))
						#print value
						w.write(var_id+'\t'+str(value.get('ref_cnt'))+'\t'+str(value.get('var_cnt'))+'\t'+str(value.get('normal_cn'))+'\t'+str(value.get('minor_cn'))+'\t'+str(value.get('major_cn'))+'\t'+str(value.get('var_case'))+'\t'+str(value.get('var_freq'))+'\t'+str(value.get('geno')+'\n'))
							
		w.close()				
					



def uniq_all(name, distinct_samples, ALL):
	"""
		Input: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone._sample_vcf.tsv'
		----------
	    	Function: 
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone._sample_vcf.tsv'

	"""
	for sample in distinct_samples:
		uniqlines = set(open('/home/shared_data_core/COLON/subclonality/'+ALL+'/pyclone_'+sample+'.vcf.tsv').readlines())

		#this will give you the list of unique lines.
		#writing that back to some file would be as easy as:

		bar = open('/home/shared_data_core/COLON/subclonality/'+ALL+'/PYCLONE_input_'+sample+'.tsv', 'wb')
		bar.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')

		for line in set(uniqlines):
			if not 'mutation_id' in line:
				bar.write(line)


