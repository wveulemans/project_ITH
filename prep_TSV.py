#!/usr/bin/python

from collections import OrderedDict as OD

def prep_tsv(name,files):
	"""
		Input: 
		----------
	    	Function: makes a TSV file per sample for 
		----------
		Output: TSV file per sample

	"""

	parts = []		
	parts = files.split("/")[6]
	#print parts

	
	file_writer = open('/home/shared_data_core/COLON/subclonality/%s/pyclone_%s.tsv'% (name,parts.lower()),'w+')
	file_writer.write('mutation_id\tref_counts\tvar_counts\tnormal_cn\tminor_cn\tmajor_cn\tvariant_case\tvariant_freq\tgenotype\n')	# add header to outfile

	global variant_info
	variant_info = OD([
		('mutation_id', str()),		# unique id for every mutation
		('ref_counts', int()),		# number of reads covering the mutation which contain the reference (genome) allele
		('var_counts', int()),		# number of reads covering the mutation which contain the variant allele
		('normal_cn', int()),		# copy number of the cells in the normal population. For autosomal chromosomes this will be 2 and for sex chromosomes it could be either 1 or 2
		('minor_cn', int()),		# minor copy number of the cancer cells. Usually this value will be predicted from WGSS or array data
		('major_cn', str()), 		# major copy number of the cancer cells. Usually this value will be predicted from WGSS or array data
		('variant_case', str(name)),	# patient_name
		('variant_freq', float()),	# 1 - (ref_counts/(ref_counts + var_counts))
		('genotype', str()),		# genotype of the mutation
		('nr', int()), 			# count per mutation
		('chr', str()), 		# chromosome where mutations lies
		('pos', int()),			# position on chromosome
		('REF', str()), 		# reference genome
		('ALT', str()),			# alternative, mutation genome
		('origin',str())		# pt = primary tumor or m = metases
	])

	return variant_info,file_writer
