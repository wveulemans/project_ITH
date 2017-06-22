#!/usr/bin/python

import vcf, read_CNV, compare

def read_vcf(variant_info,files,name,file_writer,short2,info_file):
	"""
		Input: VCF file 
		----------
	    	Function: extract parameters out of VCF file
		----------
		Output: fills the dictionnary in, in the def above

	"""

	
	variant_number = 0

	file_name = files.split('/')[6].lower()
	#print file_name
	char1 = file_name.split('_')[3]
	#print char1
	char2 = file_name.split('_')[4]
	#print char2
	origin_tum = (file_name.split('_')[5]).split('.')[0]
	#print origin_tum	

	variant_info['origin'] = name+'_'+char1+'_'+char2+'_'+origin_tum	
	#print variant_info['origin']
	vcf_reader = vcf.Reader(open('%s'% files, 'r'))
	cnt_var = 0

	range_pos_all = list()
	for record in vcf_reader:
		#cnt_var += 1 
		#print record
		filter_id_pass_list = ['AmpPass','MatchAmpPass']
		var_filter_id = record.FILTER[0]
		## Added somatic state (SS) from INFO field, removing reference and germline calls from the analysis. Check VCF header for more information
		## 2 = somatic; 3 = LOH and 5 = unknown variant type
		#print var_filter_id
		if var_filter_id in filter_id_pass_list:
			variant_info['nr'] = variant_number
			variant_info['chr'] = record.CHROM
			variant_info['pos'] = int(record.POS)
			variant_info['REF'] = record.REF
			variant_info['ALT'] = record.ALT
				
			variant_info['ref_counts'] = record.samples[1]['RD']
			variant_info['var_counts'] = record.samples[1]['AD']
			if record.samples[1]['AD'] == list():
				print '\nMULTI_ALLELIC !!!! ADJUST LOGIC :: ', record.samples[1]['AD'], '\n'
				sys.exit(0)
			#print variant_info['ref_counts']
			#print variant_info['var_counts']
			if variant_info['chr'] == 'chrX' or variant_info['chr'] == 'chrY':			# Checks if sexchromosome then check the gender
				r = open(info_file, 'rb')
				next(r)	#skip header

				for row in r:
					#print row.split()[8]
					if row.split()[8] == 'm':
						variant_info['normal_cn'] = int('1')
						#print '1, because male and sex chr'						
					#else:
						#print '2, female'
				r.close()
			
			else:
				variant_info['normal_cn'] = int('2')
			#print variant_info['normal_cn']
			variant_info['variant_freq'] = format((1 - (float(record.samples[1]['RD'])/(record.samples[1]['RD'] + record.samples[1]['AD']))), '.12f')
			#print variant_info['variant_freq']
			#print variant_info['variant_freq']
		
			variant_info['minor_CN'] = 0
			#print variant_info['major_CN'] = record.samples[4]

			binary_GT = record.samples[1]['GT'].replace('|', '/').split('/')
			#print binary_GT
			if binary_GT[0] != binary_GT[1]:
				variant_info['genotype'] = str('AB')
			if binary_GT[0] == binary_GT[1]:
				variant_info['genotype'] = str('BB')
			#print variant_info['genotype']
			variant_number += 1
			#print variant_info
			range_pos_all = list()	
			range_pos = dict()
			range_pos_all = read_CNV.read_cnv(name, variant_info)
			#print range_pos_all
			compare.compare(range_pos_all, variant_info, file_writer, name)
		else:
			range_pos_all = list()
	return range_pos_all

##########################################################################################################################################################################

def read_vcf_all(variant_info,files,name,file_writer,short2,info_file, ALL):
	"""
		Input: VCF file 
		----------
	    	Function: extract parameters out of VCF file
		----------
		Output: fills the dictionnary in, in the def above

	"""

	
	variant_number = 0

	file_name = files.split('/')[6].lower()
	#print file_name
	char1 = file_name.split('_')[3]
	#print char1
	char2 = file_name.split('_')[4]
	#print char2
	origin_tum = (file_name.split('_')[5]).split('.')[0]
	#print origin_tum	

	variant_info['origin'] = name+'_'+char1+'_'+char2+'_'+origin_tum	
	#print variant_info['origin']
	vcf_reader = vcf.Reader(open('%s'% files, 'r'))
	cnt_var = 0
	for record in vcf_reader:
		#cnt_var += 1 
		#print record
		filter_id_pass_list = ['AmpPass','MatchAmpPass']
		var_filter_id = record.FILTER[0]
		## Added somatic state (SS) from INFO field, removing reference and germline calls from the analysis. Check VCF header for more information
		## 2 = somatic; 3 = LOH and 5 = unknown variant type
		if var_filter_id in filter_id_pass_list:
			variant_info['nr'] = variant_number
			variant_info['chr'] = record.CHROM
			variant_info['pos'] = int(record.POS)
			variant_info['REF'] = record.REF
			variant_info['ALT'] = record.ALT
				
			variant_info['ref_counts'] = record.samples[1]['RD']
			variant_info['var_counts'] = record.samples[1]['AD']
			if record.samples[1]['AD'] == list():
				print '\nMULTI_ALLELIC !!!! ADJUST LOGIC :: ', record.samples[1]['AD'], '\n'
				sys.exit(0)
			#print variant_info['ref_counts']
			#print variant_info['var_counts']
			if variant_info['chr'] == 'chrX' or variant_info['chr'] == 'chrY':			# Checks if sexchromosome then check the gender
				r = open(info_file, 'rb')
				next(r)	#skip header

				for row in r:
					#print row.split()[8]
					if row.split()[8] == 'm':
						variant_info['normal_cn'] = int('1')
						#print '1, because male and sex chr'						
					#else:
						#print '2, female'
				r.close()
			
			else:
				variant_info['normal_cn'] = int('2')
			#print variant_info['normal_cn']
			variant_info['variant_freq'] = format((1 - (float(record.samples[1]['RD'])/(record.samples[1]['RD'] + record.samples[1]['AD']))), '.12f')
			#print variant_info['variant_freq']
			#print variant_info['variant_freq']
		
			variant_info['minor_CN'] = 0
			#print variant_info['major_CN'] = record.samples[4]

			binary_GT = record.samples[1]['GT'].replace('|', '/').split('/')
			#print binary_GT
			if binary_GT[0] != binary_GT[1]:
				variant_info['genotype'] = str('AB')
			if binary_GT[0] == binary_GT[1]:
				variant_info['genotype'] = str('BB')
			#print variant_info['genotype']
			variant_number += 1
			#print variant_info
			range_pos_all = list()	
			range_pos = dict()
			range_pos_all = read_CNV.read_cnv_all(name, variant_info, ALL)
			compare.compare(range_pos_all, variant_info, file_writer, name)
		else:
			range_pos_all = list()	

	return range_pos_all
