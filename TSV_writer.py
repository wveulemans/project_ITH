#! /usr/bin/python

def tsv_writer(variant_info, file_writer):
	"""
		Input: dictionary variant_info, contains information about mutation
		----------
	    	Function: write in file
		----------
		Output: '/home/shared_data_core/COLON/subclonality/patient_name/pyclone...vcf.tsv'

	"""

	a11 = variant_info.keys()

	for ele in a11[0:9]:
		#print ele
		file_writer.write(str(variant_info[ele])+'\t')
	file_writer.write('\n')




