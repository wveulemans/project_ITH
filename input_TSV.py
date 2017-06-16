#!/usr/bin/python

def input_tsv(patient_dir, name, patient_name, vcf_files):
	"""
		Input: list with input files for the actual mutation_informationfile.tsv
		----------
	    	Function: make actual mutation_informationfile.tsv
		----------
		Output: PYCLONE....tsv, ready for PyClone

	"""

	#if not os.path.exists(os.path.join(patient_dir+'PYCLONE_input_%s.tsv'% patient_name)):
	if pyclone_file == True:
		if '%s'% name in patient_name:
			if not '.tsv' in patient_name:
				w = open('/home/shared_data_core/COLON/subclonality/%s/PYCLONE_input_%s.tsv'% (name, patient_name), 'wb')
				w.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')
				for f in vcf_files:
					for i in f:
						r = open(i, 'rb')
						next(r)	#skip header
						for line in r:
							w.write(line)
				print "File: PYCLONE_input_%s.tsv \t READY!"% patient_name
				w.close()

